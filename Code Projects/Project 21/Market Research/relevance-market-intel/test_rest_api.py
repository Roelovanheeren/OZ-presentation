import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

print(f"🔍 Testing Relevance AI REST API directly")
print(f"API Key: {RAI_API_KEY[:10]}...")
print(f"Region: {RAI_REGION}")
print(f"Project: {RAI_PROJECT}")

# Test 1: Try the direct REST API call
print("\n1️⃣ Testing direct REST API call...")

try:
    # Try different possible endpoints
    endpoints_to_try = [
        f"https://api.relevanceai.com/v1/agents.create",
        f"https://api-{RAI_REGION}.stack.tryrelevance.com/latest/agents",
        f"https://api-{RAI_REGION}.stack.tryrelevance.com/v1/agents",
        f"https://api.relevanceai.com/agents"
    ]
    
    headers = {
        "Authorization": f"Bearer {RAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": "smoke_test_agent",
        "system_prompt": "You are a test agent for debugging.",
        "model": "gpt-4o-mini",
        "temperature": 0.1
    }
    
    for endpoint in endpoints_to_try:
        print(f"   Trying: {endpoint}")
        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=10)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ SUCCESS! Response: {result}")
                break
            else:
                print(f"   ❌ Failed: {response.text[:200]}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
except Exception as e:
    print(f"❌ REST API test failed: {e}")

# Test 2: Try using the SDK's HTTP client directly
print("\n2️⃣ Testing SDK HTTP client...")

try:
    from relevanceai import RelevanceAI
    client = RelevanceAI(api_key=RAI_API_KEY, region=RAI_REGION, project=RAI_PROJECT)
    
    # Try to access the underlying HTTP client
    if hasattr(client, '_client'):
        print("   Found _client attribute")
        if hasattr(client._client, 'post'):
            print("   Found post method")
            # Try making a direct HTTP call
            try:
                response = client._client.post(
                    "/agents",
                    json={
                        "name": "sdk_http_test_agent",
                        "system_prompt": "Test agent via SDK HTTP",
                        "model": "gpt-4o-mini"
                    }
                )
                print(f"   ✅ SDK HTTP call result: {response}")
            except Exception as e:
                print(f"   ❌ SDK HTTP call failed: {e}")
    
except Exception as e:
    print(f"❌ SDK HTTP test failed: {e}")

# Test 3: Try different SDK methods
print("\n3️⃣ Testing alternative SDK methods...")

try:
    from relevanceai import RelevanceAI
    client = RelevanceAI(api_key=RAI_API_KEY, region=RAI_REGION, project=RAI_PROJECT)
    
    # Try create_agent instead of upsert_agent
    try:
        agent = client.agents.create_agent(
            name="create_test_agent",
            system_prompt="Test agent via create_agent",
            model="gpt-4o-mini"
        )
        print(f"   ✅ create_agent worked: {agent}")
    except Exception as e:
        print(f"   ❌ create_agent failed: {e}")
    
    # Try with different parameters
    try:
        agent = client.agents.upsert_agent(
            name="upsert_test_agent",
            system_prompt="Test agent via upsert_agent",
            model="gpt-4o-mini",
            temperature=0.1
        )
        print(f"   ✅ upsert_agent worked: {agent}")
    except Exception as e:
        print(f"   ❌ upsert_agent failed: {e}")
        
except Exception as e:
    print(f"❌ Alternative SDK methods failed: {e}")

print("\n🎯 Conclusion:")
print("If any of these tests succeed, then agent creation DOES work.")
print("The issue is just finding the right method/endpoint.")
print("Once we find what works, I can create all your agents programmatically!")
