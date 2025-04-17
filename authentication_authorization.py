"""
3. Strong Authentication & Authorization (A2A AuthenticationInfo, Agent Card)
Mitigates: Agent Card Spoofing, Server Impersonation, Cross-Agent Task Escalation
MAESTRO Layers: 3 (Agent Frameworks), 4 (Deployment & Infrastructure), 7 (Agent Ecosystem)
"""
from jose import jwt, JWTError
from common.types import AuthenticationInfo, AgentCard
import os

def validate_jwt(token, public_key, audience):
    try:
        payload = jwt.decode(token, public_key, audience=audience, algorithms=['RS256'])
        return payload  # contains user identity and claims
    except JWTError:
        raise ValueError('Invalid or expired token')

def get_authentication_info() -> AuthenticationInfo:
    """Retrieve credentials for A2A authentication from environment."""
    token = os.environ.get("A2A_TOKEN")
    if not token:
        raise EnvironmentError("A2A_TOKEN not set")
    return AuthenticationInfo(schemes=["bearer"], credentials=token)

# Example usage:
if __name__ == "__main__":
    auth_info = get_authentication_info()
    # Example AgentCard validation (pseudo):
    # from common.client.card_resolver import A2ACardResolver
    # resolver = A2ACardResolver(base_url)
    # agent_card = resolver.resolve()
    # assert agent_card.url.startswith("https://")
