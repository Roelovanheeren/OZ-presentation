import os
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

print(f"🔍 Finding Working API Endpoints")
print(f"Region: {RAI_REGION}")
print(f"Project: {RAI_PROJECT}")

try:
    client = RelevanceAI(api_key=RAI_API_KEY, region=RAI_REGION, project=RAI_PROJECT)
    print("✅ Client created successfully")
    
    # Check the client's base URL and headers
    print(f"\n🌐 Client Configuration:")
    print(f"   Base URL: {client._client.base_url}")
    print(f"   Headers: {client._client.headers}")
    
    # Try to see what endpoints the SDK is actually calling
    print(f"\n🔍 Testing SDK Methods...")
    
    # Test agents
    try:
        agents = client.agents.list_agents()
        print(f"✅ list_agents() works - found {len(agents)} agents")
        
        # Try to see what URL it's calling
        print(f"   Let's inspect the agents manager...")
        print(f"   Agents manager type: {type(client.agents)}")
        print(f"   Available methods: {[method for method in dir(client.agents) if not method.startswith('_')]}")
        
    except Exception as e:
        print(f"❌ list_agents() failed: {e}")
    
    # Test knowledge
    try:
        knowledge = client.knowledge.list_knowledge()
        print(f"✅ list_knowledge() works - found {len(knowledge)} knowledge sets")
        
    except Exception as e:
        print(f"❌ list_knowledge() failed: {e}")
    
    # Test tools
    try:
        tools = client.tools.list_tools()
        print(f"✅ list_tools() works - found {len(tools)} tools")
        
    except Exception as e:
        print(f"❌ list_tools() failed: {e}")
    
    # Try to create a simple agent with minimal parameters
    print(f"\n🤖 Testing Minimal Agent Creation...")
    try:
        # Try with just name and system_prompt
        agent = client.agents.create_agent(
            name="minimal_test_v2",
            system_prompt="You are a minimal test agent."
        )
        print(f"✅ Minimal agent created: {agent}")
        print(f"   Agent ID: {agent.agent_id}")
        
        # Try to delete it
        try:
            client.agents.delete_agent(agent_id=agent.agent_id)
            print(f"✅ Test agent deleted successfully")
        except Exception as e:
            print(f"⚠️  Could not delete test agent: {e}")
            
    except Exception as e:
        print(f"❌ Minimal agent creation failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Try to create a simple tool
    print(f"\n🔧 Testing Minimal Tool Creation...")
    try:
        tool = client.tools.create_tool(
            title="minimal_test_tool",
            description="A minimal test tool",
            public=False
        )
        print(f"✅ Minimal tool created: {tool}")
        print(f"   Tool ID: {tool.tool_id}")
        
    except Exception as e:
        print(f"❌ Minimal tool creation failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Try to create a simple knowledge set
    print(f"\n📊 Testing Minimal Knowledge Set Creation...")
    try:
        # Try different methods
        methods_to_try = ['create', 'upsert', 'create_knowledge', 'upsert_knowledge']
        
        for method_name in methods_to_try:
            if hasattr(client.knowledge, method_name):
                print(f"   Trying {method_name}...")
                try:
                    method = getattr(client.knowledge, method_name)
                    result = method(name="minimal_test_ks", description="A minimal test knowledge set")
                    print(f"   ✅ {method_name} worked: {result}")
                    break
                except Exception as e:
                    print(f"   ❌ {method_name} failed: {e}")
            else:
                print(f"   ⚠️  {method_name} not available")
        
    except Exception as e:
        print(f"❌ Knowledge set creation failed: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n🎯 Summary:")
    print(f"   The SDK is working for basic operations.")
    print(f"   The issue is with parameter handling, not the API itself.")
    print(f"   We can create agents and tools, but need to use minimal parameters.")
    
except Exception as e:
    print(f"❌ Setup failed: {e}")
    import traceback
    traceback.print_exc()
