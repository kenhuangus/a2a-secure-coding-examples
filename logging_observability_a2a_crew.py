"""
Mitigation Example 7: Logging & Observability (A2A + Google GenAI + CrewAI)
Provides safe logging practices to prevent log injection and improve auditability.
"""
import logging
import re
from crewai import Agent, Crew, LLM, Task
from crewai.process import Process
from dotenv import load_dotenv
import os
from google import genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("a2a_observability")

def get_api_key():
    load_dotenv()
    return os.getenv("GOOGLE_API_KEY")

def safe_log(event: str):
    clean = re.sub(r'[\r\n\x00]', '', event)
    logger.info(f"Audit event: {clean}")
    return clean

class LoggingObservabilityAgent:
    def __init__(self):
        self.llm = LLM(model="gemini/gemini-2.0-flash", api_key=get_api_key())
        self.agent = Agent(
            role="Audit Logger",
            goal="Log all events safely and provide observability.",
            backstory="You are a logging agent that ensures safe, auditable logs.",
            verbose=False,
            allow_delegation=False,
            tools=[],
            llm=self.llm,
        )
        self.task = Task(
            description="Log the event in a safe, observable way.",
            expected_output="Event is logged without injection risk.",
            agent=self.agent,
        )
        self.crew = Crew(
            agents=[self.agent],
            tasks=[self.task],
            process=Process.sequential,
            verbose=False,
        )
    def log(self, event):
        return safe_log(event)

def test_logging_observability_agent():
    agent = LoggingObservabilityAgent()
    assert agent.log("user_login") == "user_login"
    assert agent.log("attack\nInjected") == "attackInjected"

if __name__ == "__main__":
    test_logging_observability_agent()
    print("Logging & observability (A2A + GenAI + CrewAI) example ran successfully.")
