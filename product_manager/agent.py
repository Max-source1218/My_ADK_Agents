from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel, Field

class ProductInfo(BaseModel):
    product_name: str = Field(description= "The full name of the product.")
    price: float = Field(description= "The price of the product in USD.")
    storage_capacity: str = Field(description= "The storage capacity of the product, e.g., '256GB', '1TB'.")
    color: str = Field(default = "Not Specified", description= "The color of the product.")

root_agent = Agent(
    model='gemini-2.5-flash',
    name='product_manager_agent',
    description='Extracts product information from user messages and returns a structured JSON Response.',
    instruction=""" You are a product information extraction agent. You will be given a user message that 
    may contain details about a product. Your task is to extract the relevant product information and return 
    it in a structured JSON format according to the Product Info model. 
    If any information is missing, you should indicate it as "Not Specified" in the JSON response. 
    Always ensure that the JSON response is valid and adheres to the ProductInfo model structure.
    
    Your Task:
    1. Read the user message carefully and identify any product-related information.
    2. Extract: product_name, price, storage_capacity, and color.
    3. Respond with a JSON object that includes all the extracted information. 
    If any field is missing, set its value to "Not Specified". Use the following JSON format:
        {
        "product_name": "Extracted product name",
        "price": 0.0,
        "storage_capacity": "256 GB or 'Not Specified'",
        "color": "Black or 'Not Specified'"
        }

    Rules:
    1. Always return a valid JSON response that adheres to the ProductInfo model structure.
    2. Price must be a float. If the price is not mentioned, set it to 0.0. Do not put a dollar sign ($).
    3. Storage capacity should be a string, e.g., '256GB', '1TB'. If not mentioned, set it to "Not Specified".
    """,

    output_schema=ProductInfo,
    output_key='extracted_product',
)
