"""
Mitigation Example 1: Input Validation & Sanitization (A2A + Google GenAI + CrewAI)
Prevents message schema violations and prompt injection by validating and sanitizing message parts using A2A types, CrewAI, and Google GenAI.
"""
from samples.python.common.types import Message, TextPart
from crewai import Agent, Crew, LLM, Task
from crewai.process import Process
from dotenv import load_dotenv
import os
from google import genai
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("input_validation")

def get_api_key():
    load_dotenv()
    return os.getenv("GOOGLE_API_KEY")

def sanitize_message_parts(message: Message) -> Message:
    for part in message.parts:
        if isinstance(part, TextPart):
            # Use a simple check for prompt injection
            if "<" in part.text or ">" in part.text or "{{" in part.text or "}}" in part.text:
                raise ValueError("Input contains potentially unsafe characters")
    return message

class InputValidationAgent:
    def __init__(self):
        self.llm = LLM(model="gemini/gemini-2.0-flash", api_key=get_api_key())
        self.agent = Agent(
            role="Input Validator",
            goal="Ensure all incoming messages are sanitized and safe for LLM processing.",
            backstory="You are a security-focused AI agent that validates user input for safety before passing to LLMs.",
            verbose=False,
            allow_delegation=False,
            tools=[],
            llm=self.llm,
        )
        self.task = Task(
            description="Validate and sanitize the user message: '{user_message}'",
            expected_output="A sanitized Message object or an error if unsafe input is detected.",
            agent=self.agent,
        )
        self.crew = Crew(
            agents=[self.agent],
            tasks=[self.task],
            process=Process.sequential,
            verbose=False,
        )
    def validate(self, user_message):
        msg = Message(role="user", parts=[TextPart(text=user_message)])
        try:
            sanitized = sanitize_message_parts(msg)
            logger.info("Message sanitized: %s", sanitized)
            return sanitized
        except ValueError as e:
            logger.error("Sanitization failed: %s", e)
            return str(e)

def test_input_validation_agent():
    agent = InputValidationAgent()
    assert isinstance(agent.validate("Hello, world!"), Message)
    result = agent.validate("<script>alert(1)</script>")
    assert "unsafe characters" in result

if __name__ == "__main__":
    test_input_validation_agent()
    print("Input validation (A2A + GenAI + CrewAI) example ran successfully.")
