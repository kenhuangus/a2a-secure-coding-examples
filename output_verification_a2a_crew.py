"""
Mitigation Example 2: Output Verification & Content Filtering (A2A + Google GenAI + CrewAI)
Filters artifacts to prevent leaking sensitive or forbidden content.
"""
from samples.python.common.types import Artifact, TextPart
from crewai import Agent, Crew, LLM, Task
from crewai.process import Process
from dotenv import load_dotenv
import os
from google import genai
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("output_verification")

def get_api_key():
    load_dotenv()
    return os.getenv("GOOGLE_API_KEY")

def filter_artifact_content(artifact: Artifact) -> Artifact:
    forbidden = {"hack", "exploit", "secret"}
    for part in artifact.parts:
        if isinstance(part, TextPart) and any(word in part.text.lower() for word in forbidden):
            raise ValueError("Artifact contains forbidden content")
    return artifact

class OutputVerificationAgent:
    def __init__(self):
        self.llm = LLM(model="gemini/gemini-2.0-flash", api_key=get_api_key())
        self.agent = Agent(
            role="Output Verifier",
            goal="Ensure all outgoing artifacts are free from sensitive or forbidden content.",
            backstory="You are a security-focused AI agent that filters artifacts before sharing.",
            verbose=False,
            allow_delegation=False,
            tools=[],
            llm=self.llm,
        )
        self.task = Task(
            description="Filter the artifact for forbidden content.",
            expected_output="A safe Artifact object or an error if forbidden content is detected.",
            agent=self.agent,
        )
        self.crew = Crew(
            agents=[self.agent],
            tasks=[self.task],
            process=Process.sequential,
            verbose=False,
        )
    def verify(self, artifact: Artifact):
        try:
            filtered = filter_artifact_content(artifact)
            logger.info("Artifact filtered: %s", filtered)
            return filtered
        except ValueError as e:
            logger.error("Filtering failed: %s", e)
            return str(e)

def test_output_verification_agent():
    from samples.python.common.types import TextPart
    agent = OutputVerificationAgent()
    safe = Artifact(parts=[TextPart(text="Safe output")])
    assert isinstance(agent.verify(safe), Artifact)
    forbidden = Artifact(parts=[TextPart(text="This is a hack")])
    result = agent.verify(forbidden)
    assert "forbidden content" in result

if __name__ == "__main__":
    test_output_verification_agent()
    print("Output verification (A2A + GenAI + CrewAI) example ran successfully.")
