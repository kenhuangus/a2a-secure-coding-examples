"""
Mitigation Example 8: Continuous Auditing & Credential Hygiene (A2A + Google GenAI + CrewAI)
Shows how to rotate credentials and maintain secure authentication info.
"""
import os
import secrets
from samples.python.common.types import AuthenticationInfo
from crewai import Agent, Crew, LLM, Task
from crewai.process import Process
from dotenv import load_dotenv
from google import genai
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("credential_hygiene")

def get_api_key():
    load_dotenv()
    return os.getenv("GOOGLE_API_KEY")

def rotate_credential(key: str):
    new_value = secrets.token_hex(16)
    os.environ[key] = new_value
    return new_value

def audit_credential(key: str):
    val = os.environ.get(key)
    if not val:
        raise EnvironmentError(f"Credential {key} missing!")
    return val

class CredentialHygieneAgent:
    def __init__(self):
        self.llm = LLM(model="gemini/gemini-2.0-flash", api_key=get_api_key())
        self.agent = Agent(
            role="Credential Auditor",
            goal="Rotate and audit credentials for secure authentication.",
            backstory="You are a security agent that manages credential hygiene.",
            verbose=False,
            allow_delegation=False,
            tools=[],
            llm=self.llm,
        )
        self.task = Task(
            description="Rotate and audit credentials for secure operations.",
            expected_output="Credentials are rotated and validated.",
            agent=self.agent,
        )
        self.crew = Crew(
            agents=[self.agent],
            tasks=[self.task],
            process=Process.sequential,
            verbose=False,
        )
    def hygiene(self, key):
        old = rotate_credential(key)
        assert audit_credential(key) == old
        new = rotate_credential(key)
        assert audit_credential(key) == new
        logger.info("Credential rotated and audited for %s", key)
        return True

def test_credential_hygiene_agent():
    agent = CredentialHygieneAgent()
    assert agent.hygiene("A2A_TOKEN")

if __name__ == "__main__":
    test_credential_hygiene_agent()
    print("Credential hygiene (A2A + GenAI + CrewAI) example ran successfully.")
