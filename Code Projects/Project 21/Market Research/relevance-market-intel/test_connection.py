import os
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION  = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

print(f"API Key: {RAI_API_KEY[:10]}...")
print(f"Region: {RAI_REGION}")
print(f"Project: {RAI_PROJECT}")

try:
    client = RelevanceAI(api_key=RAI_API_KEY, region=RAI_REGION, project=RAI_PROJECT)
    print("✅ Client created successfully")
    
    # Test basic connection
    print("Testing connection...")
    # Try to list agents to test connection
    agents = client.agents.list()
    print(f"✅ Connection successful! Found {len(agents)} existing agents")
    
    # Test knowledge sets
    print("Testing knowledge sets...")
    knowledge_sets = client.knowledge.list()
    print(f"✅ Found {len(knowledge_sets)} knowledge sets")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("This might be due to:")
    print("1. Incorrect API credentials")
    print("2. Network connectivity issues")
    print("3. Relevance AI service issues")
