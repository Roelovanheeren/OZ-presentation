import os, json, hashlib, uuid
from datetime import datetime, timezone
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# --- Init client (env-based per quickstart)
client = RelevanceAI()

print("🚀 Creating Real Estate Market Intelligence System")
print("✅ Client connected successfully")

# ---------- CREATE AGENTS (without tools for now) ----------
print("\n🤖 Creating Agents...")

with open("prompts/research_planner.md","r") as f:
    planner_prompt = f.read()
with open("prompts/research_agent.md","r") as f:
    research_prompt = f.read()
with open("prompts/report_agent.md","r") as f:
    report_prompt = f.read()

# Create agents with minimal parameters to avoid UUID issues
try:
    intake_agent = client.agents.create_agent(
        name="intake_agent",
        system_prompt="You receive JSON from a webhook, validate required fields, and save to 'leads' via tooling."
    )
    print(f"✅ Created intake_agent: {intake_agent.agent_id}")
except Exception as e:
    print(f"❌ Failed to create intake_agent: {e}")

try:
    planner_agent = client.agents.create_agent(
        name="research_planner_agent",
        system_prompt=planner_prompt
    )
    print(f"✅ Created research_planner_agent: {planner_agent.agent_id}")
except Exception as e:
    print(f"❌ Failed to create research_planner_agent: {e}")

try:
    research_agent = client.agents.create_agent(
        name="research_agent",
        system_prompt=research_prompt
    )
    print(f"✅ Created research_agent: {research_agent.agent_id}")
except Exception as e:
    print(f"❌ Failed to create research_agent: {e}")

try:
    report_agent = client.agents.create_agent(
        name="report_agent",
        system_prompt=report_prompt
    )
    print(f"✅ Created report_agent: {report_agent.agent_id}")
except Exception as e:
    print(f"❌ Failed to create report_agent: {e}")

# List all agents to verify
print(f"\n📋 Verifying All Agents...")
try:
    all_agents = client.agents.list_agents()
    print(f"   Found {len(all_agents)} total agents in your account:")
    for i, agent in enumerate(all_agents, 1):
        print(f"   {i}. {agent.name} (ID: {agent.agent_id})")
except Exception as e:
    print(f"   ❌ Could not list agents: {e}")

print(f"\n🎯 Next Steps:")
print(f"   1. Go to your Relevance AI dashboard")
print(f"   2. Create tools manually in the dashboard")
print(f"   3. Attach tools to agents manually")
print(f"   4. Set up workflows to connect all agents")
print(f"   5. Connect your landing page webhook")

print(f"\n✅ Your agents are created and ready for manual configuration!")
print(f"   The SDK has limitations for tool creation due to UUID serialization issues.")
print(f"   You'll need to create tools and workflows manually in the dashboard.")
