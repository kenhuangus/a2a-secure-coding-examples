"""
2. Output Verification & Content Filtering
Mitigates: Artifact Tampering, Data Leakage
MAESTRO Layers: 2 (Data Operations), 3 (Agent Frameworks)
"""
from common.types import Artifact, TextPart

def filter_artifact_content(artifact: Artifact) -> Artifact:
    """Prevent artifacts with forbidden words from being shared across agents."""
    forbidden = {"hack", "exploit"}
    for part in artifact.parts:
        if isinstance(part, TextPart) and any(word in part.text.lower() for word in forbidden):
            raise ValueError("Artifact contains forbidden content")
    return artifact

# Example usage:
if __name__ == "__main__":
    artifact = Artifact(parts=[TextPart(text="Safe output")])
    filter_artifact_content(artifact)
