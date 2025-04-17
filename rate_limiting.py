"""
4. Rate Limiting & Monitoring (A2A Server, Task Manager)
Mitigates: DoS, Task Replay, Insider Threats
MAESTRO Layers: 4 (Deployment & Infrastructure), 3 (Agent Frameworks), 6 (Security & Compliance)
"""
from common.server.task_manager import InMemoryTaskManager
import time

class SecureTaskManager(InMemoryTaskManager):
    def __init__(self):
        super().__init__()
        self._rate_limit = {}
        self._limit = 5
        self._interval = 1.0  # seconds

    def _check_rate_limit(self, user_id: str):
        now = time.time()
        times = self._rate_limit.get(user_id, [])
        times = [t for t in times if now - t < self._interval]
        if len(times) >= self._limit:
            raise Exception("Rate limit exceeded")
        times.append(now)
        self._rate_limit[user_id] = times

    async def on_send_task(self, request):
        user_id = getattr(request, 'user_id', 'default')
        self._check_rate_limit(user_id)
        return await super().on_send_task(request)

# Example usage:
# manager = SecureTaskManager()
# await manager.on_send_task(request)
