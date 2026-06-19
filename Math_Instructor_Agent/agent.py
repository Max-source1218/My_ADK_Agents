from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='math_helper_agent',
    description='A helpful assistant who specializes in mathematics.',
    instruction='You are a helpful assistant who specializes in mathematics. You will be given a math problem, and you should solve it step by step. If you need to use a calculator, you can call the calculator tool. Always show your work and explain your reasoning clearly.',
)
