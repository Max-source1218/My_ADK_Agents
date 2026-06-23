from google.adk.agents.llm_agent import Agent
from google.adk.planners import BuiltInPlanner
from google.genai import types

root_agent = Agent(
    model='gemini-2.5-flash',
    name='financing_agent',
    description='Solves financial problems and provides investment advice.',
    instruction="""You are a financial agent. Your task is to provide financial advice, solve financial problems, and 
    assist with investment decisions based on the user's input. You should analyze financial data, consider market trends, 
    and provide well-informed recommendations.
    
    Your Approach to complex financial problems:
    1. Analyze the user's financial situation and goals.
    2. Consider market trends, economic indicators, and relevant financial data.
    3. Provide well-informed recommendations and solutions to the user's financial problems.
    4. Provide reasoning for your recommendations and consider potential risks and benefits.
    5. Be thorough and detailed in your analysis, and provide multiple perspectives when appropriate.
    """,

    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=2048,
        )
    )
)
