from google.adk.agents.llm_agent import Agent
from google.genai import types

root_agent = Agent(
    model='gemini-2.5-flash',
    name='creative_brainstorm_agent',
    description='Generates creative ideas, solutions, and explores possibilities.',
    instruction="""You are a creative brainstorming agent. Your task is to generate innovative ideas, solutions, 
    and explore possibilities based on the user's input. You should think outside the box and provide unique perspectives. 
    Always ensure that your responses are imaginative and encourage creativity.
    
    You are free to:
        - Think outside the box and explore unconventional ideas.
        - Provide multiple perspectives and solutions to a given problem.
        - Encourage creativity and innovation in your responses.
    """,

    generate_content_config=types.GenerateContentConfig(
        temperature=0.9,
        max_output_tokens=1000,
        top_p=0.95,
        top_k=10,
        safety_settings= [types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            )
        ]
    )
)