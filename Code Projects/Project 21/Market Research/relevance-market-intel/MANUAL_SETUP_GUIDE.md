# 🏠 Real Estate Market Intelligence - Manual Setup Guide

## ✅ What's Already Done
Your 4 real estate agents are created and ready:
- **Real Estate Intake Agent** - `b4b5723b-3240-41c9-9288-065223060553`
- **Real Estate Report Agent** - `10048c33-dda6-4cf0-9dad-b6215324e46c`
- **Real Estate Research Agent** - `3694bd97-b621-45e9-991c-4abb8c53c937`
- **Real Estate Research Planner Agent** - `404dcafc-6be6-4923-a2c1-3d88071a0ee0`

## 🔧 Manual Configuration Steps

### 1. Create Knowledge Sets
Go to **Knowledge** section in your dashboard:

#### Create "leads" knowledge set:
- **Name:** `leads`
- **Description:** Real estate leads and contact information
- **Schema:**
  - `name` (text)
  - `email` (text)
  - `company` (text)
  - `target_markets` (text)
  - `investment_focus` (text)
  - `research_preferences` (text)
  - `timestamp` (text)

#### Create "research_cache" knowledge set:
- **Name:** `research_cache`
- **Description:** Cached research data to avoid duplicates
- **Schema:**
  - `query` (text)
  - `results` (text)
  - `timestamp` (text)
  - `source` (text)

#### Create "reports" knowledge set:
- **Name:** `reports`
- **Description:** Generated market research reports
- **Schema:**
  - `lead_id` (text)
  - `report_content` (text)
  - `status` (text)
  - `created_at` (text)

### 2. Configure Each Agent

#### 🏠 Real Estate Intake Agent
**Tools to add:**
- **Webhook Tool** - to receive form submissions
- **Knowledge Upsert Tool** - to store leads in "leads" knowledge set
- **Trigger Tool** - to start the research planner

**Configuration:**
1. Click on the agent
2. Go to "Tools" tab
3. Add webhook tool with your landing page URL
4. Connect to "leads" knowledge set
5. Set up trigger to "Real Estate Research Planner Agent"

#### 📋 Real Estate Research Planner Agent
**Tools to add:**
- **Knowledge Query Tool** - to read lead data
- **Function Tool** - to create research plans
- **Trigger Tool** - to start research agent

**Configuration:**
1. Connect to "leads" knowledge set (read access)
2. Add function to create research plans
3. Set up trigger to "Real Estate Research Agent"

#### 🔍 Real Estate Research Agent
**Tools to add:**
- **Google Search Tool** - for market research
- **Web Scraping Tool** - for real estate websites
- **Knowledge Upsert Tool** - to store research in "research_cache"
- **Trigger Tool** - to start report agent

**Configuration:**
1. Add Google Search API key
2. Add web scraping capabilities
3. Connect to "research_cache" knowledge set
4. Set up trigger to "Real Estate Report Agent"

#### 📄 Real Estate Report Agent
**Tools to add:**
- **Knowledge Query Tool** - to read research data
- **Function Tool** - to generate reports
- **Email Tool** - to send reports
- **Knowledge Upsert Tool** - to store reports

**Configuration:**
1. Connect to "research_cache" knowledge set (read access)
2. Connect to "reports" knowledge set (write access)
3. Add email sending capability
4. Add report generation function

### 3. Create Workflow
Go to **Workforce** section:

1. **Create New Workforce**
2. **Name:** "Real Estate Research Pipeline"
3. **Add Agents in Order:**
   - Real Estate Intake Agent
   - Real Estate Research Planner Agent
   - Real Estate Research Agent
   - Real Estate Report Agent

4. **Configure Triggers:**
   - Intake → Planner (when lead received)
   - Planner → Research (when plan created)
   - Research → Report (when research complete)

### 4. Connect Landing Page
1. **Get Webhook URL** from your Intake Agent
2. **Update your landing page** `script.js` with the webhook URL
3. **Test the connection** with a sample form submission

## 🧪 Testing Your Setup

### Test 1: Knowledge Sets
1. Go to each knowledge set
2. Try adding a test record
3. Verify the schema works

### Test 2: Agent Tools
1. Click on each agent
2. Test each tool individually
3. Verify connections to knowledge sets

### Test 3: Workflow
1. Send a test lead through the pipeline
2. Verify each agent processes the data
3. Check that the final report is generated

## 🚀 Production Checklist

- [ ] All 4 agents configured with tools
- [ ] All 3 knowledge sets created
- [ ] Workflow connecting all agents
- [ ] Landing page webhook connected
- [ ] Test lead processed successfully
- [ ] Email delivery working
- [ ] Error handling in place

## 📞 Support

If you need help with any step:
1. Check the Relevance AI documentation
2. Use their support chat
3. Refer to the agent prompts in `prompts/` folder
4. Use the report template in `templates/` folder

## 🎯 Next Steps After Setup

1. **Test with real leads** from your landing page
2. **Monitor the pipeline** for any issues
3. **Optimize agent prompts** based on results
4. **Scale up** as you get more leads
5. **Add more tools** as needed (SERP API, etc.)

Your real estate market intelligence system will be ready to process leads automatically! 🏠📊
