import os
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION  = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

print(f"🔍 Debug: Checking what's actually in your account")
print(f"API Key: {RAI_API_KEY[:10]}...")
print(f"Region: {RAI_REGION}")
print(f"Project: {RAI_PROJECT}")

try:
    client = RelevanceAI(api_key=RAI_API_KEY, region=RAI_REGION, project=RAI_PROJECT)
    print("✅ Client created successfully")
    
    # Check what methods are actually available
    print("\n🔧 Available methods:")
    print("Agents methods:", [method for method in dir(client.agents) if not method.startswith('_')])
    print("Knowledge methods:", [method for method in dir(client.knowledge) if not method.startswith('_')])
    
    # Try to list agents with different methods
    print("\n📋 Trying to list agents:")
    try:
        agents = client.agents.list_agents()
        print(f"✅ list_agents() found {len(agents)} agents")
        for i, agent in enumerate(agents):
            print(f"  Agent {i+1}: {agent}")
    except Exception as e:
        print(f"❌ list_agents() failed: {e}")
    
    try:
        agents = client.agents.list()
        print(f"✅ list() found {len(agents)} agents")
    except Exception as e:
        print(f"❌ list() failed: {e}")
    
    # Try to create a simple agent and see what happens
    print("\n🤖 Trying to create a test agent:")
    try:
        test_agent = client.agents.upsert_agent(
            name="debug_test_agent",
            system_prompt="I am a test agent for debugging",
            model="gpt-4o-mini",
            temperature=0.1
        )
        print(f"✅ Agent creation returned: {type(test_agent)}")
        print(f"   Object: {test_agent}")
        print(f"   Attributes: {dir(test_agent)}")
        
        # Check if it actually appears in the list
        agents_after = client.agents.list_agents()
        print(f"📊 Agents after creation: {len(agents_after)}")
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        print(f"   Error type: {type(e)}")
        print(f"   Error details: {str(e)}")
    
except Exception as e:
    print(f"❌ Failed to create client: {e}")

print("\n🎯 Honest Assessment:")
print("If you don't see agents in your dashboard, then the SDK calls are not working as expected.")
print("This could be due to:")
print("1. SDK version incompatibility")
print("2. API endpoint changes")
print("3. Authentication issues")
print("4. Different API structure than expected")
