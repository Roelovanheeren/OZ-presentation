import os
from dotenv import load_dotenv
from relevanceai import RelevanceAI

load_dotenv()

RAI_API_KEY = os.getenv("RAI_API_KEY")
RAI_REGION = os.getenv("RAI_REGION")
RAI_PROJECT = os.getenv("RAI_PROJECT")

print(f"🔧 Correct SDK Usage - Following Documentation")
print(f"Region: {RAI_REGION}")
print(f"Project: {RAI_PROJECT}")

try:
    client = RelevanceAI(api_key=RAI_API_KEY, region=RAI_REGION, project=RAI_PROJECT)
    print("✅ Client connected successfully")
    
    # 1. Test agent creation with correct usage
    print(f"\n🤖 Testing Agent Creation...")
    try:
        agent = client.agents.upsert_agent(
            name="SDK Test Agent",
            system_prompt="You are a test agent using correct SDK methods.",
            model="gpt-4o-mini",
            temperature=0.2
        )
        print(f"✅ Agent created: {agent}")
        print(f"   Type: {type(agent)}")
        print(f"   Agent ID: {agent.agent_id}")
        print(f"   Attributes: {[attr for attr in dir(agent) if not attr.startswith('_')]}")
        
        # Retrieve the agent to test retrieval
        retrieved_agent = client.agents.retrieve_agent(agent_id=agent.agent_id)
        print(f"✅ Agent retrieved: {retrieved_agent}")
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        import traceback
        traceback.print_exc()
    
    # 2. Test tool creation
    print(f"\n🔧 Testing Tool Creation...")
    try:
        tool = client.tools.create_tool(
            title="Hello Tool",
            description="Returns hello message",
            public=False,
            params_schema={"name": {"type": "string"}},
            output_schema={"greeting": {"type": "string"}},
            transformations=[{
                "name": "hello",
                "type": "transformation_type", 
                "config": {"param": "value"}
            }]
        )
        print(f"✅ Tool created: {tool}")
        print(f"   Type: {type(tool)}")
        print(f"   Tool ID: {tool.tool_id}")
        print(f"   Attributes: {[attr for attr in dir(tool) if not attr.startswith('_')]}")
        
    except Exception as e:
        print(f"❌ Tool creation failed: {e}")
        import traceback
        traceback.print_exc()
    
    # 3. Test attaching tool to agent
    print(f"\n🔗 Testing Tool Attachment...")
    try:
        if 'agent' in locals() and 'tool' in locals():
            agent.add_tool(tool_id=tool.tool_id)
            print(f"✅ Tool attached to agent")
            
            # List tools on the agent
            tools = agent.list_tools()
            print(f"✅ Agent tools: {tools}")
        else:
            print(f"⚠️  Skipping tool attachment - agent or tool not created")
            
    except Exception as e:
        print(f"❌ Tool attachment failed: {e}")
        import traceback
        traceback.print_exc()
    
    # 4. Test knowledge sets
    print(f"\n📊 Testing Knowledge Sets...")
    try:
        knowledge_sets = client.knowledge.list_knowledge()
        print(f"✅ Knowledge sets: {knowledge_sets}")
        print(f"   Count: {len(knowledge_sets)}")
        for i, ks in enumerate(knowledge_sets):
            print(f"   {i+1}. {ks}")
            
    except Exception as e:
        print(f"❌ Knowledge listing failed: {e}")
        import traceback
        traceback.print_exc()
    
    # 5. Now create the real estate agents properly
    print(f"\n🏠 Creating Real Estate Agents with Correct Methods...")
    
    real_estate_agents = [
        {
            "name": "Real Estate Intake Agent v2",
            "system_prompt": """You are a Real Estate Intake Agent. Process incoming leads from the landing page form, extract contact information and investment criteria, validate data quality, and store lead data in the leads knowledge set."""
        },
        {
            "name": "Real Estate Research Planner Agent v2", 
            "system_prompt": """You are a Real Estate Research Planner Agent. Create structured research plans based on lead data, identify key research areas, and coordinate the research process."""
        },
        {
            "name": "Real Estate Research Agent v2",
            "system_prompt": """You are a Real Estate Research Agent. Conduct market research using Google Search and web scraping, analyze real estate data, and store findings in the research cache."""
        },
        {
            "name": "Real Estate Report Agent v2",
            "system_prompt": """You are a Real Estate Report Agent. Generate comprehensive market research reports from research data, format reports professionally, and send them via email to leads."""
        }
    ]
    
    created_agents = []
    
    for agent_config in real_estate_agents:
        print(f"\n   Creating {agent_config['name']}...")
        try:
            agent = client.agents.upsert_agent(
                name=agent_config["name"],
                system_prompt=agent_config["system_prompt"],
                model="gpt-4o-mini",
                temperature=0.1
            )
            print(f"   ✅ Created: {agent.name} (ID: {agent.agent_id})")
            created_agents.append(agent)
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    # 6. Create tools for the agents
    print(f"\n🔧 Creating Tools for Real Estate Agents...")
    
    tools_to_create = [
        {
            "title": "Store Lead Tool",
            "description": "Store lead information in the leads knowledge set",
            "params_schema": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "company": {"type": "string"},
                "target_markets": {"type": "string"},
                "investment_focus": {"type": "string"}
            },
            "output_schema": {"status": {"type": "string"}}
        },
        {
            "title": "Google Search Tool",
            "description": "Search Google for real estate market data",
            "params_schema": {"query": {"type": "string"}},
            "output_schema": {"results": {"type": "string"}}
        },
        {
            "title": "Generate Report Tool", 
            "description": "Generate market research report from data",
            "params_schema": {"research_data": {"type": "string"}},
            "output_schema": {"report": {"type": "string"}}
        }
    ]
    
    created_tools = []
    
    for tool_config in tools_to_create:
        print(f"\n   Creating {tool_config['title']}...")
        try:
            tool = client.tools.create_tool(
                title=tool_config["title"],
                description=tool_config["description"],
                public=False,
                params_schema=tool_config["params_schema"],
                output_schema=tool_config["output_schema"],
                transformations=[{
                    "name": "execute",
                    "type": "transformation_type",
                    "config": {"param": "value"}
                }]
            )
            print(f"   ✅ Created: {tool.title} (ID: {tool.tool_id})")
            created_tools.append(tool)
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    # 7. Attach tools to appropriate agents
    print(f"\n🔗 Attaching Tools to Agents...")
    
    if len(created_agents) >= 4 and len(created_tools) >= 3:
        try:
            # Intake Agent gets Store Lead Tool
            created_agents[0].add_tool(tool_id=created_tools[0].tool_id)
            print(f"   ✅ Attached Store Lead Tool to Intake Agent")
            
            # Research Agent gets Google Search Tool  
            created_agents[2].add_tool(tool_id=created_tools[1].tool_id)
            print(f"   ✅ Attached Google Search Tool to Research Agent")
            
            # Report Agent gets Generate Report Tool
            created_agents[3].add_tool(tool_id=created_tools[2].tool_id)
            print(f"   ✅ Attached Generate Report Tool to Report Agent")
            
        except Exception as e:
            print(f"   ❌ Tool attachment failed: {e}")
    
    print(f"\n🎉 Real Estate System Created Successfully!")
    print(f"✅ Created {len(created_agents)} agents")
    print(f"✅ Created {len(created_tools)} tools")
    print(f"✅ Attached tools to agents")
    
    print(f"\n📋 Final Agent List:")
    for i, agent in enumerate(created_agents, 1):
        print(f"   {i}. {agent.name} (ID: {agent.agent_id})")
        try:
            tools = agent.list_tools()
            print(f"      Tools: {len(tools)} attached")
        except:
            print(f"      Tools: Could not list")
    
except Exception as e:
    print(f"❌ Setup failed: {e}")
    import traceback
    traceback.print_exc()
