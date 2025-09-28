import os
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

print(f"🚀 Creating All Relevance AI Agents")
print(f"Region: {RAI_REGION}")
print(f"Project: {RAI_PROJECT}")

try:
    client = RelevanceAI(api_key=RAI_API_KEY, region=RAI_REGION, project=RAI_PROJECT)
    print("✅ Client connected successfully")
    
    # Read the prompt files
    def read_prompt(filename):
        try:
            with open(f"prompts/{filename}", "r") as f:
                return f.read()
        except FileNotFoundError:
            return f"Default prompt for {filename}"
    
    # Create all agents
    agents_to_create = [
        {
            "name": "intake_agent",
            "system_prompt": read_prompt("research_planner.md"),
            "model": "gpt-4o-mini",
            "temperature": 0.1
        },
        {
            "name": "research_planner_agent", 
            "system_prompt": read_prompt("research_planner.md"),
            "model": "gpt-4o-mini",
            "temperature": 0.1
        },
        {
            "name": "research_agent",
            "system_prompt": read_prompt("research_agent.md"), 
            "model": "gpt-4o-mini",
            "temperature": 0.1
        },
        {
            "name": "report_agent",
            "system_prompt": read_prompt("report_agent.md"),
            "model": "gpt-4o-mini", 
            "temperature": 0.1
        }
    ]
    
    created_agents = []
    
    for agent_config in agents_to_create:
        print(f"\n🤖 Creating {agent_config['name']}...")
        try:
            agent = client.agents.upsert_agent(**agent_config)
            print(f"   ✅ Created: {agent.name} (ID: {agent.agent_id})")
            created_agents.append({
                "name": agent.name,
                "id": agent.agent_id,
                "type": agent_config["name"]
            })
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    # Create knowledge sets
    print(f"\n📊 Creating Knowledge Sets...")
    
    knowledge_sets = [
        {"name": "leads", "description": "Real estate leads and contact information"},
        {"name": "research_cache", "description": "Cached research data to avoid duplicates"},
        {"name": "reports", "description": "Generated market research reports"}
    ]
    
    created_knowledge = []
    
    for ks_config in knowledge_sets:
        print(f"   Creating {ks_config['name']}...")
        try:
            # Try to create knowledge set
            knowledge = client.knowledge.upsert_knowledge(
                name=ks_config["name"],
                description=ks_config["description"]
            )
            print(f"   ✅ Created: {ks_config['name']}")
            created_knowledge.append(ks_config["name"])
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    # List all created resources
    print(f"\n🎉 Setup Complete!")
    print(f"✅ Created {len(created_agents)} agents:")
    for agent in created_agents:
        print(f"   - {agent['name']} ({agent['type']})")
    
    print(f"✅ Created {len(created_knowledge)} knowledge sets:")
    for ks in created_knowledge:
        print(f"   - {ks}")
    
    # Test the agents
    print(f"\n🧪 Testing agent access...")
    try:
        all_agents = client.agents.list_agents()
        print(f"   Found {len(all_agents)} total agents in your account")
        for agent in all_agents:
            print(f"   - {agent.name} (ID: {agent.agent_id})")
    except Exception as e:
        print(f"   ❌ Could not list agents: {e}")
    
    print(f"\n🎯 Your Relevance AI system is ready!")
    print(f"   Check your dashboard to see the agents and knowledge sets.")
    print(f"   You can now connect your landing page webhook to start processing leads.")
    
except Exception as e:
    print(f"❌ Setup failed: {e}")
    import traceback
    traceback.print_exc()
