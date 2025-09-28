import os
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION  = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

print(f"Setting up Relevance AI with:")
print(f"Region: {RAI_REGION}")
print(f"Project: {RAI_PROJECT}")

client = RelevanceAI(api_key=RAI_API_KEY, region=RAI_REGION, project=RAI_PROJECT)

print("\n🔧 Testing SDK methods...")

# Test different method names
try:
    # Try to get agents
    agents = client.agents.list_agents()
    print(f"✅ Found {len(agents)} existing agents")
except Exception as e:
    print(f"ℹ️  Agents method: {e}")

try:
    # Try to get knowledge sets
    knowledge_sets = client.knowledge.list_knowledge()
    print(f"✅ Found {len(knowledge_sets)} knowledge sets")
except Exception as e:
    print(f"ℹ️  Knowledge method: {e}")

print("\n🚀 Creating agents with correct methods...")

# Create agents using the correct method
try:
    intake_agent = client.agents.upsert_agent(
        name="intake_agent",
        system_prompt="You receive a JSON payload from a webhook, ensure required fields exist, and save to 'leads' knowledge set.",
        model="gpt-4o-mini",
        temperature=0.1
    )
    print(f"✅ Created intake agent: {intake_agent}")
except Exception as e:
    print(f"❌ Failed to create intake agent: {e}")

try:
    planner_prompt = open("prompts/research_planner.md","r").read()
    planner_agent = client.agents.upsert_agent(
        name="research_planner_agent",
        system_prompt=planner_prompt,
        model="gpt-4o-mini",
        temperature=0.1
    )
    print(f"✅ Created planner agent: {planner_agent}")
except Exception as e:
    print(f"❌ Failed to create planner agent: {e}")

try:
    research_prompt = open("prompts/research_agent.md","r").read()
    research_agent = client.agents.upsert_agent(
        name="research_agent",
        system_prompt=research_prompt,
        model="gpt-4o-mini",
        temperature=0.1
    )
    print(f"✅ Created research agent: {research_agent}")
except Exception as e:
    print(f"❌ Failed to create research agent: {e}")

try:
    report_prompt = open("prompts/report_agent.md","r").read()
    report_agent = client.agents.upsert_agent(
        name="report_agent",
        system_prompt=report_prompt,
        model="gpt-4o-mini",
        temperature=0.1
    )
    print(f"✅ Created report agent: {report_agent}")
except Exception as e:
    print(f"❌ Failed to create report agent: {e}")

print("\n🎉 Bootstrap attempt complete!")
print("Check the Relevance AI dashboard to see if agents were created.")
