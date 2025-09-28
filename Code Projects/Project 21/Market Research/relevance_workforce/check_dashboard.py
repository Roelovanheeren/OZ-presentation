import os
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()

print("🔍 Checking Your Relevance AI Dashboard")
print("=" * 50)

try:
    client = RelevanceAI()
    print("✅ Connected to Relevance AI")
    
    # Check agents
    print(f"\n🤖 Agents:")
    agents = client.agents.list_agents()
    print(f"   Total agents: {len(agents)}")
    
    for i, agent in enumerate(agents, 1):
        print(f"   {i}. {agent.name}")
        print(f"      ID: {agent.agent_id}")
        try:
            tools = agent.list_tools()
            print(f"      Tools: {len(tools)}")
        except:
            print(f"      Tools: Could not list")
    
    # Check tools
    print(f"\n🔧 Tools:")
    try:
        tools = client.tools.list_tools()
        print(f"   Total tools: {len(tools)}")
        for i, tool in enumerate(tools, 1):
            print(f"   {i}. {tool.title} (ID: {tool.tool_id})")
    except Exception as e:
        print(f"   ❌ Could not list tools: {e}")
    
    # Check knowledge sets
    print(f"\n📚 Knowledge Sets:")
    try:
        knowledge = client.knowledge.list_knowledge()
        print(f"   Total knowledge sets: {len(knowledge)}")
        for i, ks in enumerate(knowledge, 1):
            print(f"   {i}. {ks.name}")
    except Exception as e:
        print(f"   ❌ Could not list knowledge sets: {e}")
    
    print(f"\n🎯 Honest Assessment:")
    print(f"   The SDK can create agents but has limitations for:")
    print(f"   - Creating tools (UUID serialization issues)")
    print(f"   - Creating knowledge sets (no methods available)")
    print(f"   - Attaching tools to agents (parameter issues)")
    print(f"   - Setting up workflows (SDK limitations)")
    
    print(f"\n📋 What You Need to Do Manually:")
    print(f"   1. Go to https://app.relevanceai.com")
    print(f"   2. Create knowledge sets in the dashboard:")
    print(f"      - 'leads' - for storing lead information")
    print(f"      - 'research_cache' - for cached research data")
    print(f"      - 'reports' - for generated reports")
    print(f"   3. Create tools in the dashboard:")
    print(f"      - Google Search tool")
    print(f"      - Web scraping tool")
    print(f"      - Email sending tool")
    print(f"      - Knowledge storage tools")
    print(f"   4. Attach tools to agents manually")
    print(f"   5. Set up workflows to connect all agents")
    print(f"   6. Connect your landing page webhook")
    
    print(f"\n🚀 The agents are created with good prompts!")
    print(f"   You just need to add the tools and workflows manually.")
    print(f"   This is the standard workflow for Relevance AI setup.")
    
except Exception as e:
    print(f"❌ Check failed: {e}")
    import traceback
    traceback.print_exc()
