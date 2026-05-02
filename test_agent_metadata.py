"""Test agent metadata functionality"""
import sys
sys.path.insert(0, 'c:/workspace/ForgeByBob')

from services.orchestration_service.agents.writer_agent import WriterAgent
from services.orchestration_service.agents.publisher_agent import PublisherAgent

print("Agent imports successful")
print("\nWriter Agent Metadata:")
print(WriterAgent.get_metadata())
print("\nPublisher Agent Metadata:")
print(PublisherAgent.get_metadata())

# Made with Bob
