import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

print(f"🔍 Finding the correct Relevance AI endpoint")
print(f"Region: {RAI_REGION}")
print(f"Project: {RAI_PROJECT}")

# Let's try to reverse engineer the correct endpoint
base_url = f"https://api-{RAI_REGION}.stack.tryrelevance.com"

print(f"\n🎯 Base URL: {base_url}")

# Test different possible agent endpoints
endpoints_to_try = [
    "/latest/agents/create",
    "/latest/agents/upsert", 
    "/latest/agents",
    "/agents/create",
    "/agents/upsert",
    "/agents",
    "/v1/agents/create",
    "/v1/agents/upsert",
    "/v1/agents",
    "/api/agents/create",
    "/api/agents/upsert", 
    "/api/agents"
]

headers = {
    "Authorization": f"Bearer {RAI_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "name": "endpoint_test_agent",
    "system_prompt": "Testing endpoint discovery",
    "model": "gpt-4o-mini",
    "temperature": 0.1
}

print(f"\n🔧 Testing {len(endpoints_to_try)} possible endpoints...")

for endpoint in endpoints_to_try:
    full_url = base_url + endpoint
    print(f"\n   Testing: {endpoint}")
    try:
        response = requests.post(full_url, headers=headers, json=payload, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ SUCCESS! Response: {result}")
            print(f"   🎉 Found working endpoint: {full_url}")
            break
        elif response.status_code == 201:
            result = response.json()
            print(f"   ✅ CREATED! Response: {result}")
            print(f"   🎉 Found working endpoint: {full_url}")
            break
        elif response.status_code == 400:
            print(f"   ⚠️  Bad Request - might be wrong payload format")
            print(f"   Response: {response.text[:200]}")
        elif response.status_code == 401:
            print(f"   ❌ Unauthorized - API key issue")
        elif response.status_code == 404:
            print(f"   ❌ Not Found - wrong endpoint")
        else:
            print(f"   ❌ Status {response.status_code}: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

# Also try GET requests to see what endpoints exist
print(f"\n🔍 Trying GET requests to discover available endpoints...")

get_endpoints = [
    "/latest/agents",
    "/agents", 
    "/v1/agents",
    "/api/agents"
]

for endpoint in get_endpoints:
    full_url = base_url + endpoint
    try:
        response = requests.get(full_url, headers=headers, timeout=10)
        print(f"   GET {endpoint}: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Found GET endpoint: {full_url}")
            try:
                data = response.json()
                print(f"   Response: {data}")
            except:
                print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   GET {endpoint}: Error {e}")

print(f"\n🎯 If we find a working endpoint, I can create all your agents!")
print(f"   The issue is just finding the right URL structure.")
