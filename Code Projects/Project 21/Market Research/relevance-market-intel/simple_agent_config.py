import os
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

print(f"🔧 Simple Agent Configuration")
print(f"Region: {RAI_REGION}")
print(f"Project: {RAI_PROJECT}")

try:
    client = RelevanceAI(api_key=RAI_API_KEY, region=RAI_REGION, project=RAI_PROJECT)
    print("✅ Client connected successfully")
    
    # Get all agents
    agents = client.agents.list_agents()
    print(f"📋 Found {len(agents)} agents")
    
    # Find real estate agents by checking the string representation
    real_estate_agents = []
    for agent in agents:
        agent_str = str(agent)
        if "Real Estate" in agent_str:
            real_estate_agents.append(agent)
            print(f"   🏠 Found: {agent_str}")
    
    print(f"\n📊 Creating Knowledge Sets...")
    
    # Try to create knowledge sets using different methods
    knowledge_methods = [
        ("create", "leads"),
        ("upsert", "research_cache"),
        ("create_knowledge", "reports")
    ]
    
    for method_name, ks_name in knowledge_methods:
        print(f"   Creating {ks_name} using {method_name}...")
        try:
            if hasattr(client.knowledge, method_name):
                method = getattr(client.knowledge, method_name)
                result = method(name=ks_name, description=f"Real estate {ks_name}")
                print(f"   ✅ Created: {ks_name}")
            else:
                print(f"   ⚠️  Method {method_name} not available")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    # Try to add basic tools to agents
    print(f"\n🔧 Adding Tools to Agents...")
    
    for i, agent in enumerate(real_estate_agents, 1):
        print(f"\n{i}. Configuring agent...")
        try:
            # Try to add a simple tool
            agent.add_tool(
                name=f"tool_{i}",
                description=f"Basic tool for agent {i}",
                tool_type="function"
            )
            print(f"   ✅ Added basic tool")
        except Exception as e:
            print(f"   ❌ Could not add tool: {e}")
    
    # Create a simple workflow
    print(f"\n🔄 Creating Simple Workflow...")
    
    try:
        # Try to create a workflow that connects the agents
        workflow_config = {
            "name": "Real Estate Research Workflow",
            "description": "Process real estate leads through research pipeline",
            "stages": [
                {
                    "name": "intake",
                    "agent": "Real Estate Intake Agent",
                    "action": "process_lead"
                },
                {
                    "name": "planning", 
                    "agent": "Real Estate Research Planner Agent",
                    "action": "create_plan"
                },
                {
                    "name": "research",
                    "agent": "Real Estate Research Agent", 
                    "action": "conduct_research"
                },
                {
                    "name": "reporting",
                    "agent": "Real Estate Report Agent",
                    "action": "generate_report"
                }
            ]
        }
        
        print(f"   Workflow configuration ready")
        print(f"   You'll need to set this up manually in the dashboard")
        
    except Exception as e:
        print(f"   ❌ Workflow creation failed: {e}")
    
    print(f"\n🎯 Manual Setup Required:")
    print(f"   The SDK has limitations for advanced configuration.")
    print(f"   You'll need to complete the setup in your Relevance AI dashboard:")
    print(f"   ")
    print(f"   1. Go to https://app.relevanceai.com")
    print(f"   2. Click on each agent to configure:")
    print(f"      - Add tools (Google Search, Web Scraping, Email)")
    print(f"      - Connect to knowledge sets")
    print(f"      - Set up triggers and workflows")
    print(f"   ")
    print(f"   3. Create knowledge sets manually:")
    print(f"      - 'leads' - for storing lead information")
    print(f"      - 'research_cache' - for cached research data")
    print(f"      - 'reports' - for generated reports")
    print(f"   ")
    print(f"   4. Set up the workflow to connect all agents")
    print(f"   5. Connect your landing page webhook to the Intake Agent")
    
    print(f"\n✅ Your agents are ready for manual configuration!")
    
except Exception as e:
    print(f"❌ Configuration failed: {e}")
    import traceback
    traceback.print_exc()
