# Relevance Market Intelligence

AI-powered real estate market research platform using Relevance AI agents and workflows.

## Setup

1. Copy `env_template` to `.env` and fill in your Relevance AI credentials
2. Install dependencies: `pip install -r requirements.txt`
3. Run bootstrap: `python bootstrap_relevance.py`
4. Test workflow: `python test_smokeworkflow.py`

## Project Structure

- `bootstrap_relevance.py` - Creates tools, agents, knowledge sets, and workflows
- `test_smokeworkflow.py` - End-to-end smoke test
- `prompts/` - Agent system prompts
- `templates/` - Report templates

## Workflow

1. Lead submission → Store in knowledge set
2. Research planning → Generate query plan
3. Research execution → Gather data from multiple sources
4. Report generation → Compile findings into structured report
5. Email delivery → Send report to lead

## Agents

- **Intake Agent**: Processes incoming leads
- **Research Planner**: Creates research query plans
- **Research Agent**: Executes individual research queries
- **Report Agent**: Compiles findings into reports
