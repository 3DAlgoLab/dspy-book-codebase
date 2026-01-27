import dspy

gemini = dspy.LM(model="gemini/gemini-2.5-pro")
dspy.configure(lm=gemini)

def check_server_status(server_id: str) -> str:
    print("called check_server_status")
    return (f"Error: Server '{server_id}' returned 503 Service Unavailable. "
            f"Packet loss detected. Suggested Action: Retry connection immediately.")

class ServerHealthCheck(dspy.Signature):
    """Diagnose server issues and report status."""
    task_description = dspy.InputField(desc="The server maintenance task")
    status_report = dspy.OutputField(desc="Final status of the server")

react_agent = dspy.ReAct(
    signature=ServerHealthCheck,
    tools=[check_server_status],
    max_iters=3 # <1>
)

if __name__ == "__main__":    
    try:
        result = react_agent(
            task_description="Check the status of Server-Alpha-9. If it fails, keep trying until you get a stable connection."
        )
        print(f"Final Agent Result: {result.status_report}")
    except Exception as e:
        print(f"\nHIT ITERATION LIMIT or Agent Error: {e}")
