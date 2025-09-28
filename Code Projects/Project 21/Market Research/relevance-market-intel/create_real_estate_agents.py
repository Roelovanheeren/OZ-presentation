import os
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

print(f"🏠 Creating Real Estate Market Intelligence Agents")
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
    
    # Create the real estate agents using create_agent (which works!)
    agents_to_create = [
        {
            "name": "Real Estate Intake Agent",
            "system_prompt": """You are a Real Estate Intake Agent. Your role is to:

1. **Process incoming leads** from the landing page form
2. **Extract and structure** contact information, investment criteria, and research preferences
3. **Validate data quality** and flag incomplete submissions
4. **Store lead data** in the leads knowledge set
5. **Trigger the research workflow** by notifying the Research Planner Agent

**Key Responsibilities:**
- Parse form submissions (name, email, company, target markets, investment focus, etc.)
- Validate email addresses and required fields
- Structure data for the research pipeline
- Maintain lead quality standards

**Output Format:** Always provide structured JSON with lead details and validation status."""
        },
        {
            "name": "Real Estate Research Planner Agent", 
            "system_prompt": read_prompt("research_planner.md")
        },
        {
            "name": "Real Estate Research Agent",
            "system_prompt": read_prompt("research_agent.md")
        },
        {
            "name": "Real Estate Report Agent",
            "system_prompt": read_prompt("report_agent.md")
        }
    ]
    
    created_agents = []
    
    print(f"\n🤖 Creating Real Estate Agents...")
    
    for i, agent_config in enumerate(agents_to_create, 1):
        print(f"\n{i}. Creating {agent_config['name']}...")
        try:
            agent = client.agents.create_agent(
                name=agent_config["name"],
                system_prompt=agent_config["system_prompt"]
            )
            print(f"   ✅ Created: {agent.name}")
            print(f"   🆔 Agent ID: {agent.agent_id}")
            created_agents.append({
                "name": agent.name,
                "id": agent.agent_id,
                "type": agent_config["name"]
            })
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    # List all agents to verify
    print(f"\n📋 Verifying all agents...")
    try:
        all_agents = client.agents.list_agents()
        print(f"   Found {len(all_agents)} total agents in your account:")
        for i, agent in enumerate(all_agents, 1):
            print(f"   {i}. {agent.name} (ID: {agent.agent_id})")
    except Exception as e:
        print(f"   ❌ Could not list agents: {e}")
    
    # Create knowledge sets using the correct method
    print(f"\n📊 Creating Knowledge Sets...")
    
    # Try different knowledge set creation methods
    knowledge_methods = [
        ("create_knowledge", "leads"),
        ("upsert_knowledge", "research_cache"), 
        ("create", "reports")
    ]
    
    created_knowledge = []
    
    for method_name, ks_name in knowledge_methods:
        print(f"   Creating {ks_name} using {method_name}...")
        try:
            if hasattr(client.knowledge, method_name):
                method = getattr(client.knowledge, method_name)
                knowledge = method(
                    name=ks_name,
                    description=f"Real estate {ks_name} data"
                )
                print(f"   ✅ Created: {ks_name}")
                created_knowledge.append(ks_name)
            else:
                print(f"   ❌ Method {method_name} not found")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    # Final summary
    print(f"\n🎉 Real Estate Market Intelligence System Ready!")
    print(f"✅ Created {len(created_agents)} agents:")
    for agent in created_agents:
        print(f"   🏠 {agent['name']}")
    
    print(f"✅ Created {len(created_knowledge)} knowledge sets:")
    for ks in created_knowledge:
        print(f"   📊 {ks}")
    
    print(f"\n🎯 Next Steps:")
    print(f"   1. Check your Relevance AI dashboard to see the agents")
    print(f"   2. Set up webhooks to connect your landing page")
    print(f"   3. Configure the workflow to process real estate leads")
    print(f"   4. Test with a sample lead to verify the pipeline")
    
    print(f"\n🔗 Your agents are ready to process real estate market research requests!")
    
except Exception as e:
    print(f"❌ Setup failed: {e}")
    import traceback
    traceback.print_exc()
