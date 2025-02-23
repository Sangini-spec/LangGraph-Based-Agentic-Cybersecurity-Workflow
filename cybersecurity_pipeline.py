import os
import subprocess
import time
import streamlit as st
from langchain.schema import AgentAction, AgentFinish
from langgraph.graph import StateGraph

# Security Pipeline State Class
class SecurityPipelineState:
    def __init__(self):
        self.tasks = []
        self.results = []
        self.logs = []
        self.allowed_scope = []

# Task Breakdown from Instructions
def parse_instructions(instruction):
    tasks = []
    if "Scan" in instruction and "open ports" in instruction:
        tasks.append("nmap")
    if "discover directories" in instruction:
        tasks.append("gobuster")
    if "test for SQL injection" in instruction:
        tasks.append("sqlmap")
    return tasks

# Task Scheduler
def task_scheduler(state: SecurityPipelineState):
    if state.tasks:
        task = state.tasks.pop(0)
        return {"task": task}
    return {"task": None}

# Enforce Scope Constraints
def enforce_scope(state):
    task = state.get("task")
    if any(domain in task for domain in state["allowed_scope"]):
        return {"task": task}
    return {"task": None}  # Block tasks outside scope

# Execute Cybersecurity Scans
def execute_task(state):
    task = state.get("task")
    command_map = {
        "nmap": f"nmap -Pn -p 80,443 {task.split()[-1]}",
        "gobuster": f"gobuster dir -u http://{task.split()[-1]} -w common.txt",
        "ffuf": f"ffuf -u http://{task.split()[-1]}/FUZZ -w common.txt",
        "sqlmap": f"sqlmap -u http://{task.split()[-1]} --batch"
    }
    tool = task.split()[0]
    
    if tool in command_map:
        try:
            output = subprocess.check_output(command_map[tool], shell=True, text=True)
            return {"results": output}
        except subprocess.CalledProcessError as e:
            return {"error": str(e)}
    return {"error": "Unknown tool"}

# Task Monitoring and Logging
def update_logs(state):
    if "results" in state:
        state.logs.append(f"[SUCCESS] {state['task']}: {state['results']}")
    elif "error" in state:
        state.logs.append(f"[ERROR] {state['task']}: {state['error']}")
    return state.__dict__

# Build LangGraph Workflow
workflow = StateGraph(SecurityPipelineState)
workflow.add_node("schedule", task_scheduler)
workflow.add_node("scope_check", enforce_scope)
workflow.add_node("execute", execute_task)
workflow.add_node("log", update_logs)
workflow.add_edge("schedule", "scope_check")
workflow.add_edge("scope_check", "execute")
workflow.add_edge("execute", "log")
workflow.set_entry_point("schedule")

def run_pipeline(instruction, allowed_scope):
    state = SecurityPipelineState()
    state.tasks = parse_instructions(instruction)
    state.allowed_scope = allowed_scope

    compiled_workflow = workflow.compile()
    state_dict = state.__dict__  

    while state.tasks:
        result = compiled_workflow.invoke(state_dict) 

        if result.get("error"):
            print(f"Error: {result['error']}")

        state_dict.update(result)  

    return state.logs

# Streamlit Dashboard
def streamlit_dashboard():
    st.title("Cybersecurity Agentic Pipeline")
    
    instruction = st.text_area("Enter security instruction")
    scope = st.text_input("Allowed scope (comma-separated domains/IPs)")
    
    if st.button("Run Scan"):
        logs = run_pipeline(instruction, scope.split(","))
        
        st.subheader("Execution Logs")
        for log in logs:
            st.write(log)

if __name__ == "__main__":
    streamlit_dashboard()
