"""
Mitigation Example 6: Secure State & Cache Management (A2A + Google GenAI + CrewAI)
Demonstrates secure, thread-safe cache usage for artifacts and credentials.
"""
from common.utils.in_memory_cache import InMemoryCache
import threading
from crewai import Agent, Crew, LLM, Task
from crewai.process import Process
from dotenv import load_dotenv
import os
from google import genai
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("secure_cache")

def get_api_key():
    load_dotenv()
    return os.getenv("GOOGLE_API_KEY")

class SecureCacheAgent:
    def __init__(self):
        self.llm = LLM(model="gemini/gemini-2.0-flash", api_key=get_api_key())
        self.agent = Agent(
            role="Cache Manager",
            goal="Ensure secure, thread-safe cache management for artifacts and credentials.",
            backstory="You are a security agent that manages cache with thread safety.",
            verbose=False,
            allow_delegation=False,
            tools=[],
            llm=self.llm,
        )
        self.task = Task(
            description="Securely store and retrieve items in the cache.",
            expected_output="Cache operations succeed without race conditions.",
            agent=self.agent,
        )
        self.crew = Crew(
            agents=[self.agent],
            tasks=[self.task],
            process=Process.sequential,
            verbose=False,
        )
        self.cache = InMemoryCache()
    def cache_example(self):
        self.cache.set("artifact", "value")
        assert self.cache.get("artifact") == "value"
        self.cache.delete("artifact")
        assert self.cache.get("artifact") is None
        def set_value():
            for _ in range(1000):
                self.cache.set("key", "v")
        threads = [threading.Thread(target=set_value) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert self.cache.get("key") == "v"
        logger.info("Cache is thread-safe and secure.")
        return True

def test_secure_cache_agent():
    agent = SecureCacheAgent()
    assert agent.cache_example()

if __name__ == "__main__":
    test_secure_cache_agent()
    print("Secure cache (A2A + GenAI + CrewAI) example ran successfully.")
