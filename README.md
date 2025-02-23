# LangGraph-Based-Agentic-Cybersecurity-Workflow



# **Agentic Cybersecurity Pipeline**

## **Overview**
This project implements an **Agentic Cybersecurity Pipeline** using **LangGraph** and **LangChain**, allowing for:
- **Automated security task execution** (e.g., `nmap`, `gobuster`, `ffuf`).
- **Dynamic task management** (sequential execution & retry mechanisms).
- **Scope enforcement** (preventing out-of-scope actions).
- **Real-time logging and reporting**.
- **Streamlit dashboard** for visualization.

## **System Architecture**
### **Components**
1. **LangGraph Workflow**
   - Breaks down high-level security instructions into executable steps.
   - Dynamically schedules tasks based on intermediate results.
   - Handles failures with automatic retries.

2. **Task Execution Layer**
   - Executes security tools like `nmap`, `gobuster`, and `ffuf`.
   - Processes real-time output.
   - Updates task lists dynamically.

3. **Scope Enforcement**
   - Ensures scans are restricted to **user-defined** domains/IPs.
   - Blocks unauthorized tasks.

4. **Monitoring & Logging**
   - Records execution logs.
   - Generates audit reports with security findings.

5. **Streamlit Dashboard**
   - Displays real-time scan execution.
   - Provides task status updates (Pending, Running, Completed, Failed).
   - Visualizes scan results.

---

## **Installation & Setup**
### **Prerequisites**
- Python 3.11+
- `pip` or `Poetry` for dependency management
- Install dependencies:
  ```bash
  pip install langchain langgraph streamlit pytest
  ```

### **Running the Pipeline**
1. **Start the Streamlit Dashboard**
   ```bash
   streamlit run your_script.py
   ```
2. **Enter Tasks** (one per line) and **Scope** (comma-separated domains/IPs).
3. **Monitor Execution** in real-time.
4. **View Logs & Reports** in the dashboard.

---

## **Agent Roles & Responsibilities**
- **Task Scheduler:** Orders & assigns tasks.
- **Scope Enforcer:** Restricts unauthorized scans.
- **Task Executor:** Runs cybersecurity tools.
- **Logger:** Captures execution history.
- **Reporter:** Generates final audit reports.

---

## **Scope Enforcement Strategy**
- The pipeline **only executes tasks within the allowed scope**.
- Any unauthorized scan is blocked and logged.
- Scope is configured at the **start of each session**.

---

## **Unit Testing**
- Uses `pytest` for automated testing:
  ```bash
  pytest your_script.py -v
  ```
- Covers:
  - Task execution flow.
  - Scope enforcement.
  - Failure handling & retries.

---

## **Future Enhancements**
- Add **more security tools** (e.g., `sqlmap`).
- Implement **multi-agent coordination**.
- Enhance reporting with **risk analysis**.

---

## **Contributing**
Feel free to submit issues or pull requests to improve the pipeline!

---


