import time

import mlflow
from litellm import completion_cost

class AgentWatchdog: # <1>
    def __init__(self, agent_name="default_agent", max_cost=0.05, max_calls=10, max_time=60):
        self.agent_name = agent_name
        self.max_cost = max_cost
        self.max_calls = max_calls
        self.max_time = max_time
        self.reset()

    def reset(self):
        """Reset internal state for a new task/session"""
        print("reset is working")
        self.start_time = time.time()
        self.stats = {
            "total_cost": 0.0,
            "total_calls": 0,
            "total_tokens": 0,
        }
        self.killed = False
        self.kill_reason = None

    def __call__(self, kwargs, completion_response, start_time, end_time):  # <2>
        print("__call__ is working")
        cost = completion_cost(completion_response=completion_response)
        self.stats["total_cost"] += cost
        
        self.stats["total_calls"] += 1
        self.stats["total_tokens"] += completion_response.get("usage", {}).get("total_tokens", 0)

        self._check_breakers()  # <3>
    
    def check_if_killed(self):
        """Check if watchdog has been triggered and raise exception if so"""
        if self.killed:
            raise RuntimeError(f"WATCHDOG TRIGGERED [{self.agent_name}]: {self.kill_reason}")

    def _check_breakers(self):  # <4>
        """Check if any resource limits have been breached and trigger kill if so"""
        print("_check_breakers is working")
        elapsed = time.time() - self.start_time
        if self.stats["total_cost"] > self.max_cost:
            self._trigger_kill(f"Cost Limit Breached: ${self.stats['total_cost']:.5f}")
        print(self.stats["total_calls"], self.max_calls, "total_calls and max_calls")
        if self.stats["total_calls"] > self.max_calls:
            self._trigger_kill(f"Call Limit Breached: {self.stats['total_calls']} calls")
        if elapsed > self.max_time:
            self._trigger_kill(f"Time Limit Breached: {elapsed:.1f}s")

    def _trigger_kill(self, reason):  # <5>
        print("_trigger_kill is working")
        self.killed = True
        self.kill_reason = reason
        mlflow.set_tag("agent_name", self.agent_name)
        mlflow.set_tag("termination_reason", reason)
        mlflow.log_metrics({**self.stats, "elapsed_time": time.time() - self.start_time})
        print(f"⚠️ WATCHDOG KILL FLAG SET: {reason}")

    def log_final_metrics(self):  # <6>
        """Log final stats for successful runs"""
        print("log_final_metrics is working")
        mlflow.set_tag("agent_name", self.agent_name)
        mlflow.log_metrics({
            "final_cost": self.stats["total_cost"],
            "final_calls": self.stats["total_calls"],
            "final_tokens": self.stats["total_tokens"],
            "total_duration": time.time() - self.start_time
        })
