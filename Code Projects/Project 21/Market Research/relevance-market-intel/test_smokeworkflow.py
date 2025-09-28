import json, uuid
from datetime import datetime, timezone
from dotenv import load_dotenv
from relevanceai import RelevanceAI
import os

load_dotenv()
client = RelevanceAI(
    api_key=os.getenv("RAI_API_KEY"),
    region=os.getenv("RAI_REGION"),
    project=os.getenv("RAI_PROJECT"),
)

lead = {
  "lead_id": str(uuid.uuid4()),
  "name": "Jane Analyst",
  "email": "jane@example.com",
  "company": "Acme Capital",
  "title": "VP, Acquisitions",
  "primary_states": ["AZ"],
  "secondary_markets": ["NV", "UT"],
  "asset_type": "BTR / SFR",
  "stage": "Pre-Dev/Entitlements",
  "investment_size": "$10–$25M",
  "market_type": "All Markets",
  "strategy": "Sun Belt BTR communities with strong in-migration",
  "priorities": ["Market Demographics","Supply & Demand Analysis","Pricing & Rent Trends","Development Pipeline","Zoning & Regulations","Economic Indicators"],
  "watchlist": "Yardly Baseline, Taylor Morrison",
  "deal_breakers": "High vacancy, poor permit velocity"
}

# 1) Store lead
client.knowledge.upsert_rows("leads", [lead])

# 2) Ask planner to make a plan
planner_id = client.agents.list_agents(name="research_planner_agent")[0]["agent_id"]
plan_msg = client.agents.trigger_task(planner_id, message=f"Create a research plan JSON for:\n\n{json.dumps(lead)}")
plan_json = plan_msg.get("latest_json", {})
print("Plan queries:", len(plan_json.get("queries", [])))

# 3) For each query, call research agent
research_id = client.agents.list_agents(name="research_agent")[0]["agent_id"]
results = []
for q in plan_json.get("queries", [])[:3]:  # limit 3 for smoke
    resp = client.agents.trigger_task(research_id, message=f"Run this query JSON:\n\n{json.dumps(q)}")
    results.append(resp.get("latest_json", {}))

# 4) Compile report
report_id = client.agents.list_agents(name="report_agent")[0]["agent_id"]
report_msg = client.agents.trigger_task(
    report_id,
    message=f"Lead profile:\n{json.dumps(lead)}\n\nVerified research results:\n{json.dumps(results)}"
)
print("Report excerpt:\n", report_msg.get("latest_text","")[:600])
