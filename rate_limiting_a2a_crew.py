"""
Mitigation Example 4: Rate Limiting & Monitoring (A2A + Google GenAI + CrewAI)
Enforces rate limits to protect against DoS and abuse.
"""
import time
from collections import defaultdict
from crewai import Agent, Crew, LLM, Task
from crewai.process import Process
from dotenv import load_dotenv
import os
from google import genai
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rate_limit")

def get_api_key():
    load_dotenv()
    return os.getenv("GOOGLE_API_KEY")

class RateLimiter:
    def __init__(self, max_calls, period_seconds):
        self.max_calls = max_calls
        self.period = period_seconds
        self.calls = defaultdict(list)

    def is_allowed(self, user_id):
        now = time.time()
        calls = self.calls[user_id]
        self.calls[user_id] = [t for t in calls if now - t < self.period]
        if len(self.calls[user_id]) < self.max_calls:
            self.calls[user_id].append(now)
            return True
        return False

class RateLimitAgent:
    def __init__(self):
        self.llm = LLM(model="gemini/gemini-2.0-flash", api_key=get_api_key())
        self.agent = Agent(
            role="Rate Limiter",
            goal="Enforce rate limits and monitor API usage.",
            backstory="You are a security agent that prevents DoS and abuse by enforcing rate limits.",
            verbose=False,
            allow_delegation=False,
            tools=[],
            llm=self.llm,
        )
        self.task = Task(
            description="Enforce rate limits for user actions.",
            expected_output="True if allowed, False if blocked.",
            agent=self.agent,
        )
        self.crew = Crew(
            agents=[self.agent],
            tasks=[self.task],
            process=Process.sequential,
            verbose=False,
        )
        self.limiter = RateLimiter(3, 2)
    def check(self, user_id):
        allowed = self.limiter.is_allowed(user_id)
        logger.info("Rate limit check for %s: %s", user_id, allowed)
        return allowed

def test_rate_limit_agent():
    agent = RateLimitAgent()
    user = "user1"
    assert agent.check(user)
    assert agent.check(user)
    assert agent.check(user)
    assert not agent.check(user)
    time.sleep(2)
    assert agent.check(user)

if __name__ == "__main__":
    test_rate_limit_agent()
    print("Rate limiting (A2A + GenAI + CrewAI) example ran successfully.")
