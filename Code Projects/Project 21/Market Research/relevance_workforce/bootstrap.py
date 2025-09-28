import os, json, hashlib, uuid
from datetime import datetime, timezone
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# --- Init client (env-based per quickstart)
# Docs show initializing RelevanceAI() with env vars set 
client = RelevanceAI()

# ---------- CREATE TOOLS ----------
# Docs: client.tools.create_tool(...) with params_schema, output_schema, transformations 

# 1) save_to_knowledge (generic row writer; here the "persistence" is via Relevance Knowledge tools later)
save_to_knowledge = client.tools.create_tool(
    title="save_to_knowledge",
    description="Save a JSON row to a named knowledge set (handled downstream).",
    public=False,
    params_schema={
        "knowledge_set": {"type":"string","description":"Target knowledge set name"},
        "row": {"type":"object","description":"Arbitrary JSON row to save"}
    },
    output_schema={"ok":{"type":"boolean"},"id":{"type":"string"}},
    transformations=[
        {"name":"noop","type":"transformation_type","config":{"note":"replace with real persistence or wiring in UI"}}
    ]
)

# 2) cache_lookup (stub that relies on your later persistence; this tool's behavior is typically implemented server-side)
cache_lookup = client.tools.create_tool(
    title="cache_lookup",
    description="Lookup a cached research_result by cache_key with freshness_days.",
    public=False,
    params_schema={
        "cache_key":{"type":"string"},
        "freshness_days":{"type":"integer","description":"Days considered fresh","default":14}
    },
    output_schema={"hit":{"type":"boolean"},"row":{"type":"object"}},
    transformations=[
        {"name":"noop","type":"transformation_type","config":{"note":"implement via HTTP tool later or UI wiring"}}
    ]
)

# 3) google_search (stub; swap to SerpAPI/Tavily via HTTP later)
google_search = client.tools.create_tool(
    title="google_search",
    description="Search the web and return candidate links (stub).",
    public=False,
    params_schema={"query":{"type":"string","description":"Search query"}},
    output_schema={"results":{"type":"array","items":{"type":"object"}}},
    transformations=[
        {"name":"noop","type":"transformation_type","config":{"note":"implement HTTP call to your search provider"}}
    ]
)

# 4) scrape_url (stub; implement HTTP scrape later)
scrape_url = client.tools.create_tool(
    title="scrape_url",
    description="Fetch a URL, extract readable text, optionally summarize (stub).",
    public=False,
    params_schema={"url":{"type":"string"},"summarize":{"type":"boolean","default":True}},
    output_schema={"content":{"type":"string"},"summary":{"type":"string"}},
    transformations=[
        {"name":"noop","type":"transformation_type","config":{"note":"implement HTTP call to your scraper service"}}
    ]
)

# 5) send_email (stub; implement SendGrid/Mailgun via HTTP later)
send_email = client.tools.create_tool(
    title="send_email",
    description="Send an email with subject and markdown body (stub).",
    public=False,
    params_schema={
        "to":{"type":"string"},
        "subject":{"type":"string"},
        "markdown_body":{"type":"string"}
    },
    output_schema={"ok":{"type":"boolean"}},
    transformations=[
        {"name":"noop","type":"transformation_type","config":{"note":"implement HTTP email provider"}}
    ]
)

print("Tools created:",
      save_to_knowledge.tool_id, cache_lookup.tool_id, google_search.tool_id, scrape_url.tool_id, send_email.tool_id)

# ---------- CREATE AGENTS ----------
# Docs: upsert agents with name/system_prompt/model/temperature; then add tools via agent.add_tool(...)  

with open("prompts/research_planner.md","r") as f:
    planner_prompt = f.read()
with open("prompts/research_agent.md","r") as f:
    research_prompt = f.read()
with open("prompts/report_agent.md","r") as f:
    report_prompt = f.read()

intake_agent = client.agents.upsert_agent(
    name="intake_agent",
    system_prompt="You receive JSON from a webhook, validate required fields, and save to 'leads' via tooling.",
    model="gpt-4o-mini",
    temperature=0.1
)
planner_agent = client.agents.upsert_agent(
    name="research_planner_agent",
    system_prompt=planner_prompt,
    model="gpt-4o-mini",
    temperature=0.1
)
research_agent = client.agents.upsert_agent(
    name="research_agent",
    system_prompt=research_prompt,
    model="gpt-4o-mini",
    temperature=0.1
)
report_agent = client.agents.upsert_agent(
    name="report_agent",
    system_prompt=report_prompt,
    model="gpt-4o-mini",
    temperature=0.1
)

print("Agents created:",
      intake_agent.agent_id, planner_agent.agent_id, research_agent.agent_id, report_agent.agent_id)

# ---------- ATTACH TOOLS TO AGENTS ----------
intake_agent.add_tool(tool_id=save_to_knowledge.tool_id)   # attach save tool

planner_agent.add_tool(tool_id=save_to_knowledge.tool_id)
planner_agent.add_tool(tool_id=cache_lookup.tool_id)

research_agent.add_tool(tool_id=google_search.tool_id)
research_agent.add_tool(tool_id=scrape_url.tool_id)
research_agent.add_tool(tool_id=save_to_knowledge.tool_id)
research_agent.add_tool(tool_id=cache_lookup.tool_id)

report_agent.add_tool(tool_id=save_to_knowledge.tool_id)
report_agent.add_tool(tool_id=send_email.tool_id)

print("Tools attached to agents.")
