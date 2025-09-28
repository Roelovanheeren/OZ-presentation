import os
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

print(f"🚀 Working Solution - What We Can Actually Do")
print(f"Region: {RAI_REGION}")
print(f"Project: {RAI_PROJECT}")

try:
    client = RelevanceAI(api_key=RAI_API_KEY, region=RAI_REGION, project=RAI_PROJECT)
    print("✅ Client connected successfully")
    
    # 1. Create real estate agents (this works!)
    print(f"\n🏠 Creating Real Estate Agents...")
    
    real_estate_agents = [
        {
            "name": "Real Estate Intake Agent Final",
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
            "name": "Real Estate Research Planner Agent Final",
            "system_prompt": """You are a Real Estate Research Planner Agent. Your role is to:

1. **Analyze lead data** to understand research requirements
2. **Create structured research plans** based on investment criteria
3. **Identify key research areas** (market analysis, competitive landscape, investment opportunities)
4. **Coordinate research tasks** and delegate to the Research Agent
5. **Monitor research progress** and ensure quality standards

**Key Responsibilities:**
- Review lead information and investment focus
- Create detailed research plans with specific tasks
- Identify relevant data sources and research methods
- Set research priorities and timelines
- Ensure comprehensive coverage of all requirements

**Output Format:** Provide structured research plans with clear tasks, priorities, and success criteria."""
        },
        {
            "name": "Real Estate Research Agent Final", 
            "system_prompt": """You are a Real Estate Research Agent. Your role is to:

1. **Conduct market research** using Google Search and web scraping
2. **Analyze real estate data** from multiple sources
3. **Gather market intelligence** on target locations and property types
4. **Store research findings** in the research cache
5. **Provide comprehensive data** for report generation

**Key Responsibilities:**
- Search for market data, property prices, and trends
- Scrape real estate websites for current listings and data
- Analyze demographic and economic factors
- Research competitive landscape and investment opportunities
- Organize and structure research findings

**Output Format:** Provide structured research data with sources, findings, and analysis."""
        },
        {
            "name": "Real Estate Report Agent Final",
            "system_prompt": """You are a Real Estate Report Agent. Your role is to:

1. **Generate comprehensive reports** from research data
2. **Format reports professionally** with clear sections and insights
3. **Send reports via email** to leads
4. **Store reports** in the reports knowledge set
5. **Ensure quality and accuracy** of all deliverables

**Key Responsibilities:**
- Compile research data into coherent reports
- Create executive summaries and detailed analysis
- Format reports with professional styling
- Send reports via email to leads
- Maintain report quality and consistency

**Output Format:** Generate professional market research reports with clear structure and actionable insights."""
        }
    ]
    
    created_agents = []
    
    for i, agent_config in enumerate(real_estate_agents, 1):
        print(f"\n{i}. Creating {agent_config['name']}...")
        try:
            agent = client.agents.create_agent(
                name=agent_config["name"],
                system_prompt=agent_config["system_prompt"]
            )
            print(f"   ✅ Created: {agent.name}")
            print(f"   🆔 Agent ID: {agent.agent_id}")
            created_agents.append(agent)
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    # 2. List all agents to verify
    print(f"\n📋 Verifying All Agents...")
    try:
        all_agents = client.agents.list_agents()
        print(f"   Found {len(all_agents)} total agents in your account:")
        for i, agent in enumerate(all_agents, 1):
            print(f"   {i}. {agent.name} (ID: {agent.agent_id})")
    except Exception as e:
        print(f"   ❌ Could not list agents: {e}")
    
    # 3. What we can't do programmatically (but you can do manually)
    print(f"\n⚠️  Manual Configuration Required:")
    print(f"   The SDK has limitations for:")
    print(f"   - Creating tools (UUID serialization issues)")
    print(f"   - Creating knowledge sets (no methods available)")
    print(f"   - Attaching tools to agents (parameter issues)")
    print(f"   - Setting up workflows (SDK limitations)")
    
    print(f"\n🎯 What You Need to Do Manually:")
    print(f"   1. Go to your Relevance AI dashboard")
    print(f"   2. Create knowledge sets manually:")
    print(f"      - 'leads' - for storing lead information")
    print(f"      - 'research_cache' - for cached research data")
    print(f"      - 'reports' - for generated reports")
    print(f"   3. Create tools manually:")
    print(f"      - Google Search tool")
    print(f"      - Web scraping tool") 
    print(f"      - Email sending tool")
    print(f"      - Knowledge storage tools")
    print(f"   4. Attach tools to agents in the dashboard")
    print(f"   5. Set up workflows to connect all agents")
    print(f"   6. Connect your landing page webhook")
    
    print(f"\n✅ What We Successfully Created:")
    print(f"   - {len(created_agents)} real estate agents with detailed prompts")
    print(f"   - All agents are ready for manual configuration")
    print(f"   - Agents have comprehensive system prompts")
    print(f"   - All prompts are in the prompts/ folder")
    print(f"   - Report template is in templates/ folder")
    
    print(f"\n🚀 Your Real Estate Market Intelligence System:")
    print(f"   ✅ Agents created and ready")
    print(f"   ✅ Prompts and templates ready")
    print(f"   ⚠️  Manual configuration needed for tools and workflows")
    print(f"   🎯 Ready for dashboard setup!")
    
except Exception as e:
    print(f"❌ Setup failed: {e}")
    import traceback
    traceback.print_exc()
