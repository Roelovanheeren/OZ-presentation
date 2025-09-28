import os, json, time, uuid, hashlib
from datetime import datetime, timezone
from dotenv import load_dotenv

# If your SDK import path differs, Cursor will fix from error messages.
from relevanceai import RelevanceAI

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION  = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

assert RAI_API_KEY and RAI_REGION and RAI_PROJECT, "Missing Relevance env vars."

client = RelevanceAI(api_key=RAI_API_KEY, region=RAI_REGION, project=RAI_PROJECT)

# ---------- Helpers
def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def make_cache_key(d: dict) -> str:
    # Convert any UUID objects to strings before serializing
    def json_serial(obj):
        if hasattr(obj, 'hex'):  # UUID objects
            return str(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    raw = json.dumps(d, sort_keys=True, default=json_serial).encode("utf-8")
    return hashlib.sha1(raw).hexdigest()

# ---------- 1) Knowledge sets (our "sheets")
KS_LEADS   = "leads"
KS_CACHE   = "research_cache"
KS_REPORTS = "reports"

print("Creating knowledge sets...")
for ks in [KS_LEADS, KS_CACHE, KS_REPORTS]:
    try:
        client.knowledge.create_knowledge(knowledge_set=ks, description=f"{ks} storage")
        print(f"✅ Created knowledge set: {ks}")
    except Exception as e:
        print(f"ℹ️  Knowledge set {ks} may already exist: {e}")

# ---------- 2) Agents (simplified - no complex tools for now)

print("\nCreating agents...")

# 2.1 Intake agent
try:
    intake_agent = client.agents.upsert_agent(
        name="intake_agent",
        system_prompt="You receive a JSON payload from a webhook, ensure required fields exist, and save to 'leads' knowledge set.",
        model="gpt-4o-mini",
        temperature=0.1
    )
    print(f"✅ Created intake agent: {intake_agent.agent_id}")
except Exception as e:
    print(f"❌ Failed to create intake agent: {e}")

# 2.2 Research planner agent
try:
    planner_prompt = open("prompts/research_planner.md","r").read()
    planner_agent = client.agents.upsert_agent(
        name="research_planner_agent",
        system_prompt=planner_prompt,
        model="gpt-4o-mini",
        temperature=0.1
    )
    print(f"✅ Created planner agent: {planner_agent.agent_id}")
except Exception as e:
    print(f"❌ Failed to create planner agent: {e}")

# 2.3 Research agent
try:
    research_prompt = open("prompts/research_agent.md","r").read()
    research_agent = client.agents.upsert_agent(
        name="research_agent",
        system_prompt=research_prompt,
        model="gpt-4o-mini",
        temperature=0.1
    )
    print(f"✅ Created research agent: {research_agent.agent_id}")
except Exception as e:
    print(f"❌ Failed to create research agent: {e}")

# 2.4 Report agent
try:
    report_prompt = open("prompts/report_agent.md","r").read()
    report_agent = client.agents.upsert_agent(
        name="report_agent",
        system_prompt=report_prompt,
        model="gpt-4o-mini",
        temperature=0.1
    )
    print(f"✅ Created report agent: {report_agent.agent_id}")
except Exception as e:
    print(f"❌ Failed to create report agent: {e}")

print("\n🎉 Bootstrap complete!")
print("Agents created successfully. You can now test the workflow.")
