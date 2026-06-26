from google.adk.agents.llm_agent import Agent

# Simulated Database

ORDERS_DB = {
    "ORDER123": { "status": "Shipped", "total": "99.99", "customer": "john@gmail.com" },
    "ORDER456": { "status": "Processing", "total": "49.99", "customer": "jane@gmail.com"},
    "ORDER789": { "status": "Delivered", "total": "149.99", "customer": "bob@gmail.com" },
}

# Tool 1: Check order status
def check_order_status(order_id: str) -> dict: 
    """"Check the current status of an order given its ID.
        Use this when a customer asks about their order status or delivery.

        Args:
            order_id (str): The ID of the order to check. (e.g., "ORDER123")

        Returns:
            dict: A dictionary containing the order status and other details.

            On success: {'status': 'success', 'order_status': '...', 'details': '{...}'}
            On error: {'status': 'error', 'error_type': 'Order not found.'/'invalid_format'/'database_error', 'message': '...'}
    """
    if not order_id.startswith("ORDER"):
        return {"status": "error", "error_type": "invalid_format", "message": "Order ID must start with 'ORDER'."}
    
    # Look up the order in the simulated database
    if order_id not in ORDERS_DB:
        return {"status": "error", "error_type": "Order not found.", "message": f"Order {order_id} not found."}
    
    order_details = ORDERS_DB[order_id]
    return {
            "status": "success",
            "order_id": order_id,
            "order_status": order_details["status"], 
            "details": order_details
            }

# Tool 2: Process refund request
def process_refund(order_id: str, reason: str) -> dict:
    """Process a refund request for a given order ID and reason.
        Use this ONLY after verifying if the order exists with check_order_status.

        Args:
            order_id (str): The ID of the order to refund. (e.g., "ORDER123")
            reason (str): The reason for the refund request.
            
        Returns:
            dict: Refund processing result.
                On success: {'status': 'success', 'refund_amount': X, 'reference_id': 'REF####', 'message': 'Refund processed successfully.'}
                on error: {'status': 'error', 'error_type': 'Order not found.'/'cannot_refund'/'database_error', 'message': '...'}
        """
    if order_id not in ORDERS_DB:
        return {"status": "error", "error_type": "Order not found.", "message": f"Order {order_id} not found."}
    
    order_details = ORDERS_DB[order_id]

    if order_details["status"] == "Delivered":
        return {
            "status": "success", 
            "refund_amount": order_details["total"],
            "reference_id": f"REF{order_id[3:]}",
            "estimated_refund_time": "5-7 business days",
            "message": f"Refund for order {order_id} has been processed successfully."
            }
    else:
        return {
            "status": "error", 
            "error_type": "cannot_refund", 
            "message": f"Order {order_id} is not eligible for a refund. Current status: {order_details['status']}."
            }

def escalate_to_human_agent(issue_summary: str, order_id: str) -> dict:
    """Escalate the issue to a human agent for further assistance.
        Use this when the AI cannot resolve the user's issue.

        Args:
            issue_summary (str): A summary of the issue that needs human intervention.
            order_id (str): The ID of the order related to the issue.

        Returns:
            dict: Escalation result.
                On success: {'status': 'success', 'message': 'Issue escalated to human agent.', 'ticket_id': 'TICKET####'}
                on error: {'status': 'error', 'error_type': 'escalation_failed', 'message': '...'}
    """
    # Simulate escalation process
    ticket_id = f"TICKET{len(issue_summary)}"  # Simple ticket ID generation based on summary length
    
    return {
        "status": "success",
        "message": "Issue escalated to human supervisor.",
        "ticket_id": ticket_id,
        "estimated response_time": "within 2 hours",
        "order_id": order_id if order_id in ORDERS_DB else "N/A",
    }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='customer_support_agent',
    description='Handles customer support inquiries about orders and refunds with comprehensive assistance and error handling.',
    instruction="""
            You are a customer support agent for an e-commerce platform. 
            
            Your primary responsibilities include:
            - Processing refund requests for eligible orders.
            - Escalating complex issues to human supervisors.
            - Providing accurate information about order status and refund policies.

            You have three tools available at your disposal:
            1. check_order_status(order_id: str) -> dict
                - Use this tool to check the current status of an order given its ID.
                - This is useful when a customer asks about their order status or delivery.
                - Returns a dictionary containing the order status and other details.

            2. process_refund(order_id: str) -> dict
                - Use this tool to initiate a refund process for an eligible order.
                - This is useful when a customer requests a refund for their order.
                - Returns a dictionary containing the refund status and details.

            3. escalate_to_human_agent(issue_summary: str, order_id: str) -> dict
                - Use this tool to escalate a complex issue to a human supervisor.
                - This is useful when the AI cannot resolve the user's issue.
                - Returns a dictionary containing the escalation result and ticket information.


        Workflow Guidelines:

        ## For Order Status Inquiries:
        1.) Greet the customer politely/warmly.
        2.) Ask for the order ID to check the order status.
        3.) If the order ID is valid, check the order status using the check_order_status tool.
        4.) Handle the result:
            -If status is success: Provide clear status update with details.
            - if error_type is "Order not found.": Inform the customer and ask for a valid order ID.
            - if error_type is "invalid_format": Inform the customer about the correct format and ask for a valid order ID.
        
        ## For Refund Requests:
        1.) Express empathy and understanding for the customer's situation.
        2.) Ask for the order ID and reason for the refund request.
        3.) Check the order status using the check_order_status tool.
        4.) If error_type = 'Order not found.': Inform the customer and ask for a valid order ID.
        5.) If order exists, use process_refund tool with the order ID and reason.
        6.) Handle the result:
            - If status is success: Provide refund confirmation with reference ID and estimated refund timeframe.
            - If error_type is "cannot_refund": Inform the customer that the order is not eligible for a refund and provide 
            the current order status.
            - if error_type is "database_error": Inform the customer that there was an issue processing the refund and advise 
            them to try again later or contact support.
            - if error_type is "order_not_found": Inform the customer that the order was not found and ask for a valid order ID.

        ## Error Handling Strategy:

            1.) For 'not_found' errors:
            - Ask customer to double-check the order ID
            - Offer to search by email if they have it
            - Be patient and helpful

            2.) For 'invalid_format' errors:
            - Politely explain the correct format: "ORD" followed by numbers
            - Provide an example: ORD123
            - Ask them to provide the order ID in correct format

            3.) For 'cannot_refund' errors:
            - Explain the policy clearly (only delivered orders can be refunded)
            - Show empathy for their frustration
            - Offer to escalate to supervisor if they want an exception

        ## When to Escalate:
            Use escalate_to_supervisor tool when:

                - Customer is frustrated or angry and requests supervisor
                - Issue cannot be resolved with available tools
                - Customer requests policy exception
                - Multiple tool attempts have failed
                - Customer specifically asks to speak with a manager

                After escalating:
                - Provide the ticket ID
                - Tell them expected response time
                - Thank them for their patience

                Communication Style
                - Always be polite, professional, and empathetic
                - Use the customer's name if you know it
                - Provide clear next steps
                - Acknowledge their feelings (frustration, concern)
                - Thank them for their patience
                - Never make promises you can't keep
                """,

tools=[check_order_status, process_refund, escalate_to_human_agent]
)
