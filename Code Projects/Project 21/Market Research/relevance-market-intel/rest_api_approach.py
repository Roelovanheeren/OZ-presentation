import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

print(f"🌐 Using REST API Directly")
print(f"Region: {RAI_REGION}")
print(f"Project: {RAI_PROJECT}")

# Base URL for the API
base_url = f"https://api-{RAI_REGION}.stack.tryrelevance.com/latest"

headers = {
    "Authorization": f"Bearer {RAI_API_KEY}",
    "Content-Type": "application/json"
}

print(f"🔗 Base URL: {base_url}")

# 1. Test basic connectivity
print(f"\n🔍 Testing API Connectivity...")
try:
    # Try to get agents using GET
    response = requests.get(f"{base_url}/agents", headers=headers, timeout=10)
    print(f"   GET /agents: {response.status_code}")
    if response.status_code == 200:
        agents = response.json()
        print(f"   ✅ Found {len(agents)} existing agents")
        for i, agent in enumerate(agents):
            print(f"      {i+1}. {agent.get('name', 'Unknown')} (ID: {agent.get('agent_id', 'Unknown')})")
    else:
        print(f"   ❌ Failed: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 2. Create agents using POST
print(f"\n🤖 Creating Real Estate Agents via REST API...")

real_estate_agents = [
    {
        "name": "Real Estate Intake Agent REST",
        "system_prompt": """You are a Real Estate Intake Agent. Process incoming leads from the landing page form, extract contact information and investment criteria, validate data quality, and store lead data in the leads knowledge set.""",
        "model": "gpt-4o-mini",
        "temperature": 0.1
    },
    {
        "name": "Real Estate Research Planner Agent REST", 
        "system_prompt": """You are a Real Estate Research Planner Agent. Create structured research plans based on lead data, identify key research areas, and coordinate the research process.""",
        "model": "gpt-4o-mini",
        "temperature": 0.1
    },
    {
        "name": "Real Estate Research Agent REST",
        "system_prompt": """You are a Real Estate Research Agent. Conduct market research using Google Search and web scraping, analyze real estate data, and store findings in the research cache.""",
        "model": "gpt-4o-mini",
        "temperature": 0.1
    },
    {
        "name": "Real Estate Report Agent REST",
        "system_prompt": """You are a Real Estate Report Agent. Generate comprehensive market research reports from research data, format reports professionally, and send them via email to leads.""",
        "model": "gpt-4o-mini",
        "temperature": 0.1
    }
]

created_agents = []

for i, agent_config in enumerate(real_estate_agents, 1):
    print(f"\n{i}. Creating {agent_config['name']}...")
    try:
        response = requests.post(f"{base_url}/agents", headers=headers, json=agent_config, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            agent_data = response.json()
            print(f"   ✅ Created: {agent_data.get('name', 'Unknown')}")
            print(f"   🆔 Agent ID: {agent_data.get('agent_id', 'Unknown')}")
            created_agents.append(agent_data)
        else:
            print(f"   ❌ Failed: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

# 3. Create knowledge sets
print(f"\n📊 Creating Knowledge Sets via REST API...")

knowledge_sets = [
    {
        "name": "leads",
        "description": "Real estate leads and contact information"
    },
    {
        "name": "research_cache",
        "description": "Cached research data to avoid duplicates"
    },
    {
        "name": "reports", 
        "description": "Generated market research reports"
    }
]

created_knowledge = []

for i, ks_config in enumerate(knowledge_sets, 1):
    print(f"\n{i}. Creating {ks_config['name']}...")
    try:
        # Try different endpoints for knowledge sets
        endpoints = [
            f"{base_url}/knowledge",
            f"{base_url}/knowledge-sets",
            f"{base_url}/knowledge_set"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.post(endpoint, headers=headers, json=ks_config, timeout=10)
                print(f"   {endpoint}: {response.status_code}")
                if response.status_code in [200, 201]:
                    ks_data = response.json()
                    print(f"   ✅ Created: {ks_data.get('name', 'Unknown')}")
                    created_knowledge.append(ks_data)
                    break
                else:
                    print(f"   ❌ Failed: {response.text[:100]}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
                
    except Exception as e:
        print(f"   ❌ Knowledge set creation failed: {e}")

# 4. Create tools
print(f"\n🔧 Creating Tools via REST API...")

tools_to_create = [
    {
        "title": "Store Lead Tool",
        "description": "Store lead information in the leads knowledge set",
        "public": False,
        "params_schema": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "company": {"type": "string"},
            "target_markets": {"type": "string"},
            "investment_focus": {"type": "string"}
        },
        "output_schema": {"status": {"type": "string"}}
    },
    {
        "title": "Google Search Tool",
        "description": "Search Google for real estate market data",
        "public": False,
        "params_schema": {"query": {"type": "string"}},
        "output_schema": {"results": {"type": "string"}}
    },
    {
        "title": "Generate Report Tool",
        "description": "Generate market research report from data", 
        "public": False,
        "params_schema": {"research_data": {"type": "string"}},
        "output_schema": {"report": {"type": "string"}}
    }
]

created_tools = []

for i, tool_config in enumerate(tools_to_create, 1):
    print(f"\n{i}. Creating {tool_config['title']}...")
    try:
        response = requests.post(f"{base_url}/tools", headers=headers, json=tool_config, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            tool_data = response.json()
            print(f"   ✅ Created: {tool_data.get('title', 'Unknown')}")
            print(f"   🆔 Tool ID: {tool_data.get('tool_id', 'Unknown')}")
            created_tools.append(tool_data)
        else:
            print(f"   ❌ Failed: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

# 5. Final summary
print(f"\n🎉 REST API Setup Complete!")
print(f"✅ Created {len(created_agents)} agents")
print(f"✅ Created {len(created_knowledge)} knowledge sets")
print(f"✅ Created {len(created_tools)} tools")

print(f"\n📋 Created Agents:")
for i, agent in enumerate(created_agents, 1):
    print(f"   {i}. {agent.get('name', 'Unknown')} (ID: {agent.get('agent_id', 'Unknown')})")

print(f"\n📊 Created Knowledge Sets:")
for i, ks in enumerate(created_knowledge, 1):
    print(f"   {i}. {ks.get('name', 'Unknown')}")

print(f"\n🔧 Created Tools:")
for i, tool in enumerate(created_tools, 1):
    print(f"   {i}. {tool.get('title', 'Unknown')} (ID: {tool.get('tool_id', 'Unknown')})")

print(f"\n🎯 Next Steps:")
print(f"   1. Check your Relevance AI dashboard")
print(f"   2. Verify agents, knowledge sets, and tools are visible")
print(f"   3. Manually attach tools to agents in the dashboard")
print(f"   4. Set up workflows to connect everything")
print(f"   5. Connect your landing page webhook")

print(f"\n🚀 Your real estate market intelligence system is ready!")
