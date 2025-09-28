import json, uuid
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()
client = RelevanceAI()

# Grab agents by name (simple helper)
def get_agent_id_by_name(name: str) -> str:
    agents = client.agents.list_agents()
    for a in agents:
        if getattr(a, "name", "") == name:
            return a.agent_id
    raise ValueError(f"Agent named {name} not found")

lead = {
  "lead_id": str(uuid.uuid4()),
  "name": "Jane Analyst",
  "email": "jane@example.com",
  "company": "Acme Capital",
  "title": "VP, Acquisitions",
  "primary_states": ["AZ"],
  "secondary_markets": ["NV","UT"],
  "asset_type": "BTR / SFR",
  "stage": "Pre-Dev/Entitlements",
  "investment_size": "$10–$25M",
  "market_type": "All Markets",
  "strategy": "Sun Belt BTR, strong in-migration",
  "priorities": ["Market Demographics","Supply & Demand Analysis","Pricing & Rent Trends","Development Pipeline","Zoning & Regulations","Economic Indicators"],
  "watchlist": "Yardly Baseline, Taylor Morrison",
  "deal_breakers": "High vacancy, poor permit velocity"
}

# 1) PLAN
planner_id = get_agent_id_by_name("research_planner_agent")
plan_task = client.agents.retrieve_agent(planner_id).trigger_task(
    message=f"Create a research plan JSON for this lead:\n\n{json.dumps(lead)}"
)
# Depending on your workspace, fetch a preview of the last output if available:
try:
    preview = client.agents.retrieve_agent(planner_id).get_task_output_preview(conversation_id=plan_task.conversation_id)
except Exception:
    preview = {}
print("Planner output preview (truncated):", str(preview)[:600])

# 2) RESEARCH (demo: send the whole plan back to research_agent; in your workflow you'd fan-out per query)
research_id = get_agent_id_by_name("research_agent")
research_task = client.agents.retrieve_agent(research_id).trigger_task(
    message=f"Run this research plan (JSON). For each query, return a result JSON. If tools are stubs, just outline what you'd do:\n\n{json.dumps(preview)}"
)
print("Research task started:", research_task.conversation_id)

# 3) REPORT
report_id = get_agent_id_by_name("report_agent")
report_task = client.agents.retrieve_agent(report_id).trigger_task(
    message=f"Lead profile:\n{json.dumps(lead)}\n\nVerified research results (mock or real):\nUse the template structure and produce Markdown."
)
print("Report task:", report_task.conversation_id)
