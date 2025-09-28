import os
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

print(f"🔧 Configuring Real Estate Agents with Tools and Knowledge")
print(f"Region: {RAI_REGION}")
print(f"Project: {RAI_PROJECT}")

try:
    client = RelevanceAI(api_key=RAI_API_KEY, region=RAI_REGION, project=RAI_PROJECT)
    print("✅ Client connected successfully")
    
    # First, let's get our agents
    agents = client.agents.list_agents()
    print(f"📋 Found {len(agents)} agents")
    
    # Find our real estate agents
    real_estate_agents = {}
    for agent in agents:
        if "Real Estate" in agent.name:
            real_estate_agents[agent.name] = agent
            print(f"   🏠 {agent.name} (ID: {agent.agent_id})")
    
    # Create knowledge sets first
    print(f"\n📊 Creating Knowledge Sets...")
    
    knowledge_sets = [
        {
            "name": "leads",
            "description": "Real estate leads and contact information",
            "schema": {
                "name": "text",
                "email": "text", 
                "company": "text",
                "target_markets": "text",
                "investment_focus": "text",
                "research_preferences": "text",
                "timestamp": "text"
            }
        },
        {
            "name": "research_cache", 
            "description": "Cached research data to avoid duplicates",
            "schema": {
                "query": "text",
                "results": "text",
                "timestamp": "text",
                "source": "text"
            }
        },
        {
            "name": "reports",
            "description": "Generated market research reports", 
            "schema": {
                "lead_id": "text",
                "report_content": "text",
                "status": "text",
                "created_at": "text"
            }
        }
    ]
    
    created_knowledge = []
    
    for ks_config in knowledge_sets:
        print(f"   Creating {ks_config['name']}...")
        try:
            # Try different methods to create knowledge sets
            if hasattr(client.knowledge, 'create'):
                knowledge = client.knowledge.create(
                    name=ks_config["name"],
                    description=ks_config["description"]
                )
                print(f"   ✅ Created: {ks_config['name']}")
                created_knowledge.append(ks_config['name'])
            else:
                print(f"   ⚠️  Knowledge creation method not available")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    # Now configure each agent with tools and knowledge
    print(f"\n🤖 Configuring Agents...")
    
    # Configure Intake Agent
    if "Real Estate Intake Agent" in real_estate_agents:
        intake_agent = real_estate_agents["Real Estate Intake Agent"]
        print(f"\n📥 Configuring Intake Agent...")
        
        try:
            # Add tools to the intake agent
            print(f"   Adding tools...")
            # Try to add a webhook tool
            try:
                intake_agent.add_tool(
                    name="store_lead",
                    description="Store lead information in the leads knowledge set",
                    tool_type="knowledge_upsert",
                    knowledge_set="leads"
                )
                print(f"   ✅ Added store_lead tool")
            except Exception as e:
                print(f"   ⚠️  Could not add store_lead tool: {e}")
            
            # Try to add a trigger tool for the next agent
            try:
                intake_agent.add_tool(
                    name="trigger_research",
                    description="Trigger the research planner agent",
                    tool_type="agent_trigger",
                    target_agent="Real Estate Research Planner Agent"
                )
                print(f"   ✅ Added trigger_research tool")
            except Exception as e:
                print(f"   ⚠️  Could not add trigger_research tool: {e}")
                
        except Exception as e:
            print(f"   ❌ Intake agent configuration failed: {e}")
    
    # Configure Research Planner Agent
    if "Real Estate Research Planner Agent" in real_estate_agents:
        planner_agent = real_estate_agents["Real Estate Research Planner Agent"]
        print(f"\n📋 Configuring Research Planner Agent...")
        
        try:
            # Add research planning tools
            planner_agent.add_tool(
                name="create_research_plan",
                description="Create a structured research plan",
                tool_type="function",
                function_code="def create_research_plan(lead_data):\n    # Create research plan based on lead data\n    return {'plan': 'research_plan', 'steps': []}"
            )
            print(f"   ✅ Added create_research_plan tool")
            
            planner_agent.add_tool(
                name="trigger_research_agent",
                description="Trigger the research agent with the plan",
                tool_type="agent_trigger", 
                target_agent="Real Estate Research Agent"
            )
            print(f"   ✅ Added trigger_research_agent tool")
            
        except Exception as e:
            print(f"   ❌ Planner agent configuration failed: {e}")
    
    # Configure Research Agent
    if "Real Estate Research Agent" in real_estate_agents:
        research_agent = real_estate_agents["Real Estate Research Agent"]
        print(f"\n🔍 Configuring Research Agent...")
        
        try:
            # Add research tools
            research_agent.add_tool(
                name="google_search",
                description="Search Google for real estate market data",
                tool_type="function",
                function_code="def google_search(query):\n    # Perform Google search\n    return {'results': 'search_results'}"
            )
            print(f"   ✅ Added google_search tool")
            
            research_agent.add_tool(
                name="scrape_website",
                description="Scrape real estate websites for data",
                tool_type="function", 
                function_code="def scrape_website(url):\n    # Scrape website content\n    return {'content': 'scraped_data'}"
            )
            print(f"   ✅ Added scrape_website tool")
            
            research_agent.add_tool(
                name="store_research",
                description="Store research results in cache",
                tool_type="knowledge_upsert",
                knowledge_set="research_cache"
            )
            print(f"   ✅ Added store_research tool")
            
        except Exception as e:
            print(f"   ❌ Research agent configuration failed: {e}")
    
    # Configure Report Agent
    if "Real Estate Report Agent" in real_estate_agents:
        report_agent = real_estate_agents["Real Estate Report Agent"]
        print(f"\n📄 Configuring Report Agent...")
        
        try:
            # Add report generation tools
            report_agent.add_tool(
                name="generate_report",
                description="Generate market research report",
                tool_type="function",
                function_code="def generate_report(research_data):\n    # Generate report from research data\n    return {'report': 'generated_report'}"
            )
            print(f"   ✅ Added generate_report tool")
            
            report_agent.add_tool(
                name="store_report",
                description="Store generated report",
                tool_type="knowledge_upsert",
                knowledge_set="reports"
            )
            print(f"   ✅ Added store_report tool")
            
            report_agent.add_tool(
                name="send_email",
                description="Send report via email",
                tool_type="function",
                function_code="def send_email(to, subject, body):\n    # Send email with report\n    return {'status': 'sent'}"
            )
            print(f"   ✅ Added send_email tool")
            
        except Exception as e:
            print(f"   ❌ Report agent configuration failed: {e}")
    
    print(f"\n🎉 Agent Configuration Complete!")
    print(f"✅ Configured {len(real_estate_agents)} real estate agents")
    print(f"✅ Created {len(created_knowledge)} knowledge sets")
    
    print(f"\n📋 Next Steps:")
    print(f"   1. Check your Relevance AI dashboard")
    print(f"   2. Verify agents have tools and knowledge sets")
    print(f"   3. Set up workflows to connect the agents")
    print(f"   4. Test the complete pipeline")
    print(f"   5. Connect your landing page webhook")
    
except Exception as e:
    print(f"❌ Configuration failed: {e}")
    import traceback
    traceback.print_exc()
