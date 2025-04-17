"""
7. Logging & Observability (A2A Task/Audit Events)
Mitigates: Insider Threats, Cross-Layer Attacks
MAESTRO Layers: 5 (Evaluation & Observability), 6 (Security & Compliance)
"""
import logging
from common.types import TaskStatus, TaskState, Message, TextPart

def log_task_status(task_status: TaskStatus):
    """Log task status safely, preventing log injection from Message parts."""
    msg = task_status.message.parts[0].text if task_status.message and task_status.message.parts else ""
    if "\n" in msg or "\r" in msg:
        raise ValueError("Log injection detected")
    logging.info(f"Task {task_status.state}: {msg}")

# Example usage:
if __name__ == "__main__":
    status = TaskStatus(state=TaskState.WORKING, message=Message(role="agent", parts=[TextPart(text="Processing")]))
    log_task_status(status)
