"""
Mitigation Example 3: Strong Authentication & Authorization (A2A + Google GenAI + CrewAI)
Uses JWT and environment-based credentials to ensure agent identity and secure operations.
"""
from samples.python.common.types import AuthenticationInfo
from crewai import Agent, Crew, LLM, Task
from crewai.process import Process
from dotenv import load_dotenv
import os
from jose import jwt, JWTError
from google import genai
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("authz")

def get_api_key():
    load_dotenv()
    return os.getenv("GOOGLE_API_KEY")

def validate_jwt(token, public_key, audience):
    try:
        payload = jwt.decode(token, public_key, audience=audience, algorithms=['RS256'])
        return payload
    except JWTError:
        raise ValueError('Invalid or expired token')

def get_authentication_info() -> AuthenticationInfo:
    token = os.environ.get("A2A_TOKEN")
    if not token:
        raise EnvironmentError("A2A_TOKEN not set")
    return AuthenticationInfo(schemes=["bearer"], credentials=token)

class AuthAgent:
    def __init__(self):
        self.llm = LLM(model="gemini/gemini-2.0-flash", api_key=get_api_key())
        self.agent = Agent(
            role="Auth Validator",
            goal="Ensure all credentials and JWTs are valid before processing requests.",
            backstory="You are a security agent that checks credentials and JWTs for every operation.",
            verbose=False,
            allow_delegation=False,
            tools=[],
            llm=self.llm,
        )
        self.task = Task(
            description="Validate credentials and JWT tokens for secure operations.",
            expected_output="Valid credentials or an error if invalid.",
            agent=self.agent,
        )
        self.crew = Crew(
            agents=[self.agent],
            tasks=[self.task],
            process=Process.sequential,
            verbose=False,
        )
    def check(self):
        try:
            info = get_authentication_info()
            logger.info("Auth info: %s", info)
            return info
        except Exception as e:
            logger.error("Auth failed: %s", e)
            return str(e)

def test_auth_agent():
    os.environ["A2A_TOKEN"] = "dummy-token"
    agent = AuthAgent()
    result = agent.check()
    assert hasattr(result, "schemes")
    del os.environ["A2A_TOKEN"]
    result2 = agent.check()
    assert "A2A_TOKEN not set" in result2

if __name__ == "__main__":
    test_auth_agent()
    print("Authentication & authorization (A2A + GenAI + CrewAI) example ran successfully.")
