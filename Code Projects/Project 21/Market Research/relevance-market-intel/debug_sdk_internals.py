import os
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

print(f"🔍 Debugging SDK internals")
print(f"API Key: {RAI_API_KEY[:10]}...")
print(f"Region: {RAI_REGION}")
print(f"Project: {RAI_PROJECT}")

try:
    client = RelevanceAI(api_key=RAI_API_KEY, region=RAI_REGION, project=RAI_PROJECT)
    print("✅ Client created successfully")
    
    # Check the client's internal structure
    print(f"\n🔧 Client attributes:")
    print(f"   Type: {type(client)}")
    print(f"   Attributes: {[attr for attr in dir(client) if not attr.startswith('_')]}")
    
    # Check the agents manager
    print(f"\n🤖 Agents manager:")
    print(f"   Type: {type(client.agents)}")
    print(f"   Attributes: {[attr for attr in dir(client.agents) if not attr.startswith('_')]}")
    
    # Try to access the underlying HTTP client
    if hasattr(client, '_client'):
        print(f"\n🌐 HTTP client:")
        print(f"   Type: {type(client._client)}")
        print(f"   Base URL: {getattr(client._client, 'base_url', 'Not found')}")
        print(f"   Headers: {getattr(client._client, 'headers', 'Not found')}")
        
        # Try to see what URL it's actually calling
        if hasattr(client._client, 'post'):
            print(f"   POST method available")
    
    # Try to list agents and see what happens
    print(f"\n📋 Testing list_agents:")
    try:
        agents = client.agents.list_agents()
        print(f"   ✅ list_agents() returned: {type(agents)}")
        print(f"   Count: {len(agents)}")
        for i, agent in enumerate(agents):
            print(f"   Agent {i+1}: {agent}")
    except Exception as e:
        print(f"   ❌ list_agents() failed: {e}")
        print(f"   Error type: {type(e)}")
        
        # Try to see what the actual HTTP request looks like
        print(f"\n🔍 Let's try to see what URL it's calling...")
        try:
            # This might give us the actual endpoint
            import inspect
            source = inspect.getsource(client.agents.list_agents)
            print(f"   Source code: {source[:200]}...")
        except:
            print(f"   Could not get source code")
    
    # Try to create an agent with minimal parameters
    print(f"\n🤖 Testing minimal agent creation:")
    try:
        agent = client.agents.upsert_agent(
            name="minimal_test",
            system_prompt="Test"
        )
        print(f"   ✅ Agent created: {agent}")
    except Exception as e:
        print(f"   ❌ Agent creation failed: {e}")
        print(f"   Error type: {type(e)}")
        
        # Try to see what the actual request looks like
        print(f"\n🔍 Let's inspect the error more closely...")
        import traceback
        traceback.print_exc()
    
    # Try different authentication methods
    print(f"\n🔑 Testing different auth methods:")
    
    # Method 1: Try with explicit headers
    try:
        from relevanceai import RelevanceAI
        client2 = RelevanceAI(
            api_key=RAI_API_KEY, 
            region=RAI_REGION, 
            project=RAI_PROJECT,
            headers={"Authorization": f"Bearer {RAI_API_KEY}"}
        )
        print(f"   ✅ Client with explicit headers created")
    except Exception as e:
        print(f"   ❌ Explicit headers failed: {e}")
    
    # Method 2: Try without project parameter
    try:
        client3 = RelevanceAI(api_key=RAI_API_KEY, region=RAI_REGION)
        print(f"   ✅ Client without project created")
    except Exception as e:
        print(f"   ❌ Without project failed: {e}")
    
except Exception as e:
    print(f"❌ Client creation failed: {e}")
    import traceback
    traceback.print_exc()

print(f"\n🎯 Next steps:")
print(f"   If we can see the actual HTTP requests being made,")
print(f"   we can replicate them with direct requests library calls.")
