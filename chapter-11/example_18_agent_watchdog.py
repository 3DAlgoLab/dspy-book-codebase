import dspy
import mlflow
import litellm
from agent_watchdog import AgentWatchdog

def setup_dspy(): # <1>
    mlflow.dspy.autolog()
    lm = dspy.LM('gemini/gemini-2.5-flash')
    dspy.configure(lm=lm)


def create_watchdog(agent_name="default_agent", max_cost=0.02, max_calls=5, max_time=30): # <2>
    watchdog = AgentWatchdog(agent_name=agent_name, max_cost=max_cost, max_calls=max_calls, max_time=max_time)
    litellm.success_callback = [watchdog]
    return watchdog

def run_agent_safely(agent_module, watchdog, **kwargs): # <3>
    with mlflow.start_run(run_name="Watchdog_Protected_Execution"):
        try:
            print("🚀 Agent started...")
            result = agent_module(**kwargs)
            watchdog.check_if_killed()  # Check if watchdog was triggered during execution
            watchdog.log_final_metrics()
            mlflow.set_tag("status", "SUCCESS")
            return result
        except RuntimeError as e:
            print(f"🛑 RuntimeError: {e}")
            mlflow.set_tag("status", "KILLED")
            raise e
        except Exception as e:
            print(f"💥 Unexpected Error: {e}")
            mlflow.set_tag("status", "ERROR")
            raise e

def search_tool(query: str) -> str: # <4>
    """Simulated search tool that returns dummy results."""
    print("search_tool called")
    return f"Simulated search result for query: {query}"

class SearchAgent(dspy.Module):  # <5>
    def __init__(self, watchdog=None):
        super().__init__()
        self.agent = dspy.ReAct("question -> answer", tools=[search_tool], max_iters=1)
        self.watchdog = watchdog

    def forward(self, question):
        result = self.agent(question=question)
        if self.watchdog:
            self.watchdog.check_if_killed()  # <6>
        return result

def main(): # <7>
    setup_dspy()
    watchdog = create_watchdog(agent_name="search_agent", max_calls=2)
    my_agent = SearchAgent(watchdog=watchdog)

    while True:
        question = input("\n🔍 Enter your question (or 'quit' to exit): ")
        if question.lower() in ('quit', 'exit', 'q'):
            print("👋 Goodbye!")
            break
        
        try:
            response = run_agent_safely(my_agent, watchdog, question=question)
            if response:
                print(f"\n📝 Answer: {response.answer}")
        except RuntimeError as e:
            print(f"\n❌ Agent was terminated: {e}")
            break
            # Continue to next question instead of crashing

if __name__ == "__main__":
    main()

