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

for ks in [KS_LEADS, KS_CACHE, KS_REPORTS]:
    try:
        client.knowledge.create_knowledge(knowledge_set=ks, description=f"{ks} storage")
    except Exception:
        # likely already exists; keep idempotent
        pass

# ---------- 2) Tools

# 2.1 save_to_knowledge (generic insert/upsert)
save_tool = client.tools.create_tool(
    title="save_to_knowledge",
    description="Save a JSON row to a knowledge set.",
    public=False,
    params_schema={
        "knowledge_set": {"type":"string","description":"Target knowledge set name"},
        "row": {"type":"object","description":"Arbitrary JSON row"}
    },
    output_schema={"ok":{"type":"boolean"},"id":{"type":"string"}},
    transformations=[
        {
            "name":"save",
            "type":"python",
            "config":{
                "code": """
def handler(params, ctx):
    ks = params["knowledge_set"]
    row = params["row"]
    # add standard timestamps
    row.setdefault("created_at", ctx.now())
    ctx.client.knowledge.upsert_rows(knowledge_set=ks, rows=[row])
    return {"ok": True, "id": row.get("id", "")}
                """
            }
        }
    ]
)

# 2.2 cache_lookup
cache_tool = client.tools.create_tool(
    title="cache_lookup",
    description="Lookup a cached research_result by cache_key with freshness_days.",
    public=False,
    params_schema={
        "cache_key":{"type":"string"},
        "freshness_days":{"type":"integer","default":14}
    },
    output_schema={
        "hit":{"type":"boolean"},
        "row":{"type":"object"}
    },
    transformations=[
        {
            "name":"lookup",
            "type":"python",
            "config":{
                "code": """
from datetime import datetime, timezone, timedelta

def handler(params, ctx):
    key = params["cache_key"]
    fresh_days = params.get("freshness_days", 14)
    rows = ctx.client.knowledge.search(
        knowledge_set="research_cache",
        filters={"cache_key": key},
        limit=1,
        sort=[{"field":"cached_at","direction":"desc"}]
    )
    if not rows or len(rows)==0:
        return {"hit": False, "row": {}}
    row = rows[0]
    try:
        ts = datetime.fromisoformat(row.get("cached_at","").replace("Z","+00:00"))
    except:
        ts = datetime(1970,1,1,tzinfo=timezone.utc)
    fresh = (datetime.now(timezone.utc) - ts) <= timedelta(days=fresh_days)
    return {"hit": fresh, "row": row}
                """
            }
        }
    ]
)

# 2.3 google_search (placeholder using requests to a provider you choose)
# Swap in SerpAPI/Tavily as you prefer.
google_tool = client.tools.create_tool(
    title="google_search",
    description="Search the web and return candidate links.",
    public=False,
    params_schema={"query":{"type":"string"}},
    output_schema={"results":{"type":"array","items":{"type":"object"}}},
    transformations=[{
        "name":"search",
        "type":"python",
        "config":{
            "code": """
import requests, os
def handler(params, ctx):
    q = params["query"]
    # TODO: integrate your preferred search API here.
    # For bootstrap, return empty to let scrape_url use known portals.
    return {"results": []}
            """
        }
    }]
)

# 2.4 scrape_url with optional summarize
scrape_tool = client.tools.create_tool(
    title="scrape_url",
    description="Fetch a URL, extract readable text, optionally summarize.",
    public=False,
    params_schema={
        "url":{"type":"string"},
        "summarize":{"type":"boolean","default":True}
    },
    output_schema={"content":{"type":"string"},"summary":{"type":"string"}},
    transformations=[{
        "name":"scrape",
        "type":"python",
        "config":{
            "code": """
import requests, bs4

def clean_text(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    for s in soup(["script","style","noscript"]): s.extract()
    text = " ".join(soup.get_text(" ").split())
    return text[:20000]

def handler(params, ctx):
    url = params["url"]
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    text = clean_text(r.text)
    summary = ""
    if params.get("summarize", True):
        # call the model via ctx.llm for a 5-8 bullet extractive summary
        summary = ctx.llm(
            prompt=f"Summarize the following page into 5–8 concise bullets with numbers preserved when present:\\n\\n{text[:8000]}",
            max_tokens=500,
            temperature=0.1
        )
    return {"content": text, "summary": summary}
            """
        }
    }]
)

# 2.5 send_email (placeholder; swap in SendGrid/Mailgun later)
email_tool = client.tools.create_tool(
    title="send_email",
    description="Send an email with a subject and markdown body. (Bootstrap: logs only.)",
    public=False,
    params_schema={
        "to":{"type":"string"},
        "subject":{"type":"string"},
        "markdown_body":{"type":"string"}
    },
    output_schema={"ok":{"type":"boolean"}},
    transformations=[{
        "name":"send",
        "type":"python",
        "config":{
            "code": """
def handler(params, ctx):
    # TODO: integrate SendGrid/Mailgun. For now, just log.
    ctx.log(f"EMAIL TO: {params['to']} | SUBJECT: {params['subject']}")
    return {"ok": True}
            """
        }
    }]
)

# ---------- 3) Agents

# 3.1 Intake agent (optional: can just use webhook→save tool)
intake_agent = client.agents.upsert_agent(
    name="intake_agent",
    system_prompt="You receive a JSON payload from a webhook, ensure required fields exist, and save to 'leads' knowledge set.",
    model="gpt-4o-mini",
    temperature=0.1
)
client.agents.add_tool(intake_agent.agent_id, save_tool.tool_id)

# 3.2 Research planner agent
planner_prompt = open("prompts/research_planner.md","r").read()
planner_agent = client.agents.upsert_agent(
    name="research_planner_agent",
    system_prompt=planner_prompt,
    model="gpt-4o-mini",
    temperature=0.1
)
for t in [save_tool, cache_tool]:
    client.agents.add_tool(planner_agent.agent_id, t.tool_id)

# 3.3 Research agent (multi-type)
research_prompt = open("prompts/research_agent.md","r").read()
research_agent = client.agents.upsert_agent(
    name="research_agent",
    system_prompt=research_prompt,
    model="gpt-4o-mini",
    temperature=0.1
)
for t in [google_tool, scrape_tool, save_tool, cache_tool]:
    client.agents.add_tool(research_agent.agent_id, t.tool_id)

# 3.4 Report agent
report_prompt = open("prompts/report_agent.md","r").read()
report_agent = client.agents.upsert_agent(
    name="report_agent",
    system_prompt=report_prompt,
    model="gpt-4o-mini",
    temperature=0.1
)
client.agents.add_tool(report_agent.agent_id, save_tool.tool_id)

# ---------- 4) Workflow: define the orchestration graph (logical)

workflow = {
  "id": "market_research_workflow_v1",
  "description": "Landing page lead → plan → research → report → email",
  "stages": [
    {
      "id": "store_lead",
      "agent": "intake_agent",
      "action": "save_to_knowledge",
      "params_map": {
        "knowledge_set": KS_LEADS,
        "row": "{{lead_payload}}"
      },
      "output": "lead_row"
    },
    {
      "id": "plan",
      "agent": "research_planner_agent",
      "message": "Create a research plan JSON for this lead:\n\n{{lead_payload}}",
      "post_hooks": [
        {
          "tool": "save_to_knowledge",
          "params": {
            "knowledge_set": KS_LEADS,
            "row": {"id":"{{lead_payload.lead_id}}","plan_created_at":"{{now}}"}
          }
        }
      ],
      "output": "plan_json"
    },
    {
      "id": "research_fanout",
      "mode": "map",   # run per query
      "items": "{{plan_json.queries}}",
      "per_item": {
        "id": "research_one",
        "agent": "research_agent",
        "message": "Run this research query (JSON object):\n\n{{item}}",
        "post_hooks": [
          {
            "tool": "save_to_knowledge",
            "params": {
              "knowledge_set": KS_CACHE,
              "row": {
                "id": "{{item.id}}",
                "lead_id": "{{lead_payload.lead_id}}",
                "cache_key": "{{item.cache_key}}",
                "query_type": "{{item.type}}",
                "topic": "{{item.topic}}",
                "result": "{{last_response_json}}",
                "cached_at": "{{now}}"
              }
            }
          }
        ],
        "output": "research_result"
      },
      "collect_as": "research_results"
    },
    {
      "id": "compile_report",
      "agent": "report_agent",
      "message": "Lead profile:\n{{lead_payload}}\n\nVerified research results:\n{{research_results}}",
      "post_hooks": [
        {
          "tool": "save_to_knowledge",
          "params": {
            "knowledge_set": KS_REPORTS,
            "row": {
              "id": "{{lead_payload.lead_id}}-{{now}}",
              "lead_id": "{{lead_payload.lead_id}}",
              "report_markdown": "{{last_response_text}}",
              "created_at": "{{now}}"
            }
          }
        }
      ],
      "output": "report_markdown"
    },
    {
      "id": "email_report",
      "agent": "report_agent",   # tool-only use; could be any agent
      "action": "send_email",
      "params_map": {
        "to": "{{lead_payload.email}}",
        "subject": "Your Market Research Brief",
        "markdown_body": "{{report_markdown}}"
      },
      "output": "email_status"
    }
  ]
}

# Store workflow definition as a knowledge row for visibility
client.knowledge.upsert_rows(knowledge_set="leads", rows=[{
    "id": "WORKFLOW::market_research_workflow_v1",
    "workflow_json": workflow,
    "created_at": now_iso()
}])

print("Bootstrap complete.")
print("Agents created:",
      intake_agent.agent_id, planner_agent.agent_id, research_agent.agent_id, report_agent.agent_id)
