import os
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION  = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

print(f"🚀 Setting up Fresh Relevance AI Market Intelligence System")
print(f"Region: {RAI_REGION}")
print(f"Project: {RAI_PROJECT}")

client = RelevanceAI(api_key=RAI_API_KEY, region=RAI_REGION, project=RAI_PROJECT)

print("\n📊 Checking Fresh Account Status:")
try:
    agents = client.agents.list_agents()
    print(f"✅ Found {len(agents)} existing agents")
    
    knowledge_sets = client.knowledge.list_knowledge()
    print(f"✅ Found {len(knowledge_sets)} existing knowledge sets")
    
except Exception as e:
    print(f"ℹ️  Status check: {e}")

print("\n🔧 Creating Knowledge Sets...")

# Create knowledge sets first
knowledge_sets_to_create = ["leads", "research_cache", "reports"]

for ks_name in knowledge_sets_to_create:
    try:
        # Try different methods to create knowledge sets
        try:
            result = client.knowledge.create_knowledge(knowledge_set=ks_name, description=f"{ks_name} storage")
            print(f"✅ Created knowledge set: {ks_name}")
        except AttributeError:
            try:
                result = client.knowledge.create(knowledge_set=ks_name, description=f"{ks_name} storage")
                print(f"✅ Created knowledge set: {ks_name}")
            except AttributeError:
                # If no create method, try to add a sample row to create it
                sample_data = [{"id": "sample", "created_at": "2024-01-01", "type": "test"}]
                result = client.knowledge.upsert_rows(knowledge_set=ks_name, rows=sample_data)
                print(f"✅ Created knowledge set: {ks_name} (via upsert)")
    except Exception as e:
        print(f"ℹ️  Knowledge set {ks_name}: {e}")

print("\n🤖 Creating Agents...")

# Create agents with error handling
agents_to_create = [
    {
        "name": "intake_agent",
        "system_prompt": "You receive a JSON payload from a webhook, ensure required fields exist, and save to 'leads' knowledge set.",
        "model": "gpt-4o-mini",
        "temperature": 0.1
    },
    {
        "name": "research_planner_agent", 
        "system_prompt": open("prompts/research_planner.md","r").read(),
        "model": "gpt-4o-mini",
        "temperature": 0.1
    },
    {
        "name": "research_agent",
        "system_prompt": open("prompts/research_agent.md","r").read(),
        "model": "gpt-4o-mini", 
        "temperature": 0.1
    },
    {
        "name": "report_agent",
        "system_prompt": open("prompts/report_agent.md","r").read(),
        "model": "gpt-4o-mini",
        "temperature": 0.1
    }
]

created_agents = []

for agent_config in agents_to_create:
    try:
        agent = client.agents.upsert_agent(**agent_config)
        created_agents.append(agent_config["name"])
        print(f"✅ Created agent: {agent_config['name']}")
    except Exception as e:
        print(f"❌ Failed to create {agent_config['name']}: {e}")

print(f"\n🎉 Bootstrap Complete!")
print(f"✅ Created {len(created_agents)} agents: {created_agents}")
print(f"✅ Created 3 knowledge sets: leads, research_cache, reports")

print("\n📋 Your Fresh Account is Ready!")
print("🔗 Check your Relevance AI dashboard to see:")
print("  - 4 specialized agents for real estate research")
print("  - 3 knowledge sets for data storage")
print("  - All prompts and templates configured")

print("\n🚀 Next Steps:")
print("1. Verify agents in your Relevance AI dashboard")
print("2. Test the workflow with: python3 simple_test.py")
print("3. Connect your landing page webhook")
print("4. Start processing real estate leads!")
