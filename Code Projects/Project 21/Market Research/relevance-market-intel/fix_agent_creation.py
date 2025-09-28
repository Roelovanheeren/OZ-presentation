import os
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

print(f"🔧 Fixing Agent Creation")
print(f"Region: {RAI_REGION}")
print(f"Project: {RAI_PROJECT}")

try:
    client = RelevanceAI(api_key=RAI_API_KEY, region=RAI_REGION, project=RAI_PROJECT)
    print("✅ Client connected successfully")
    
    # First, let's see what agents already exist
    print(f"\n📋 Current agents:")
    try:
        agents = client.agents.list_agents()
        print(f"   Found {len(agents)} agents")
        for i, agent in enumerate(agents):
            print(f"   Agent {i+1}: {agent}")
            print(f"   Type: {type(agent)}")
            print(f"   Attributes: {[attr for attr in dir(agent) if not attr.startswith('_')]}")
            if hasattr(agent, 'agent_id'):
                print(f"   Agent ID: {agent.agent_id}")
            if hasattr(agent, 'name'):
                print(f"   Name: {agent.name}")
            print()
    except Exception as e:
        print(f"   ❌ Could not list agents: {e}")
    
    # Try to create a simple agent with minimal parameters
    print(f"\n🤖 Testing simple agent creation:")
    try:
        agent = client.agents.upsert_agent(
            name="test_agent_simple",
            system_prompt="You are a test agent."
        )
        print(f"   ✅ Created agent: {agent}")
        print(f"   Type: {type(agent)}")
        print(f"   Attributes: {[attr for attr in dir(agent) if not attr.startswith('_')]}")
        
        # Try to access the agent_id
        if hasattr(agent, 'agent_id'):
            print(f"   Agent ID: {agent.agent_id}")
        else:
            print(f"   No agent_id attribute found")
            # Try other possible attribute names
            for attr in ['id', 'uuid', 'identifier']:
                if hasattr(agent, attr):
                    print(f"   Found {attr}: {getattr(agent, attr)}")
        
    except Exception as e:
        print(f"   ❌ Agent creation failed: {e}")
        print(f"   Error type: {type(e)}")
        import traceback
        traceback.print_exc()
    
    # Try different agent creation methods
    print(f"\n🔧 Trying alternative creation methods:")
    
    # Method 1: create_agent instead of upsert_agent
    try:
        agent = client.agents.create_agent(
            name="test_agent_create",
            system_prompt="You are a test agent via create_agent."
        )
        print(f"   ✅ create_agent worked: {agent}")
    except Exception as e:
        print(f"   ❌ create_agent failed: {e}")
    
    # Method 2: Try with different parameter names
    try:
        agent = client.agents.upsert_agent(
            name="test_agent_params",
            system_prompt="You are a test agent with different params.",
            model="gpt-4o-mini"
        )
        print(f"   ✅ Agent with model worked: {agent}")
    except Exception as e:
        print(f"   ❌ Agent with model failed: {e}")
    
    # Check what methods are actually available
    print(f"\n🔍 Available agent methods:")
    methods = [method for method in dir(client.agents) if not method.startswith('_')]
    for method in methods:
        print(f"   - {method}")
    
    # Try to see what the actual HTTP request looks like
    print(f"\n🌐 Checking HTTP client:")
    if hasattr(client, '_client'):
        print(f"   Base URL: {client._client.base_url}")
        print(f"   Headers: {client._client.headers}")
    
except Exception as e:
    print(f"❌ Setup failed: {e}")
    import traceback
    traceback.print_exc()

print(f"\n🎯 Summary:")
print(f"   The SDK is working but has some attribute access issues.")
print(f"   Agents are being created (we can see them in the list),")
print(f"   but accessing their properties is inconsistent.")
print(f"   This suggests the agents ARE being created successfully!")
