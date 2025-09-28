import os
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION  = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

print(f"🚀 Setting up Relevance AI Market Intelligence System")
print(f"Region: {RAI_REGION}")
print(f"Project: {RAI_PROJECT}")

client = RelevanceAI(api_key=RAI_API_KEY, region=RAI_REGION, project=RAI_PROJECT)

print("\n📊 Current Status:")
try:
    agents = client.agents.list_agents()
    print(f"✅ Found {len(agents)} existing agents")
    
    knowledge_sets = client.knowledge.list_knowledge()
    print(f"✅ Found {len(knowledge_sets)} knowledge sets")
    
    # Show existing agents
    print("\n🤖 Existing Agents:")
    for agent in agents:
        print(f"  - {agent.get('name', 'Unknown')}: {agent.get('id', 'No ID')}")
        
except Exception as e:
    print(f"❌ Error getting status: {e}")

print("\n🔧 Creating/Updating Agents...")

# Create agents - the upsert_agent method should work
agents_created = []

try:
    intake_agent = client.agents.upsert_agent(
        name="intake_agent",
        system_prompt="You receive a JSON payload from a webhook, ensure required fields exist, and save to 'leads' knowledge set.",
        model="gpt-4o-mini",
        temperature=0.1
    )
    agents_created.append(("intake_agent", intake_agent))
    print("✅ Intake agent created/updated")
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
    agents_created.append(("research_planner_agent", planner_agent))
    print("✅ Research planner agent created/updated")
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
    agents_created.append(("research_agent", research_agent))
    print("✅ Research agent created/updated")
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
    agents_created.append(("report_agent", report_agent))
    print("✅ Report agent created/updated")
except Exception as e:
    print(f"❌ Failed to create report agent: {e}")

print(f"\n🎉 Bootstrap Complete!")
print(f"✅ Created/Updated {len(agents_created)} agents")
print("\n📋 Next Steps:")
print("1. Check your Relevance AI dashboard to see the agents")
print("2. Run the smoke test: python3 test_smokeworkflow.py")
print("3. Connect your landing page webhook to trigger the workflow")

print("\n🔗 Your agents are ready to process real estate market research requests!")
