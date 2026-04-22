import json
import os
import pandas as pd
from graph import create_graph

# Initialize the Agent Graph once (Global)
app = create_graph()

def lambda_handler(event, context):
    """
    AWS Lambda handler for CHAI 2.0.
    Triggered by: EventBridge (Cron) or SQS.
    """
    print("🚀 CHAI 2.0 Cloud Agent triggered...")
    
    # In production, we'd fetch this from S3 or a database.
    # For now, we use the local CSV bundled in the deployment package.
    try:
        suppliers = pd.read_csv("data/suppliers.csv")
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error loading supplier data: {str(e)}"
        }

    reports_generated = 0
    
    # Process each supplier
    for _, supplier in suppliers.iterrows():
        print(f"Processing: {supplier['supplier_name']}")
        
        initial_state = {
            "supplier_info": supplier.to_dict(),
            "raw_news": [],
            "identified_risks": [],
            "final_alert": "",
            "logs": []
        }
        
        # Execute the Agentic Graph
        # Note: Lambda environment is stateless, so our local JSON memory 
        # should eventually move to DynamoDB for true persistence.
        result = app.invoke(initial_state)
        
        # Log result to CloudWatch
        if result["final_alert"] and "No risk" not in result["final_alert"]:
            print(f"ALERT GENERATED for {supplier['supplier_name']}")
            reports_generated += 1
        
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Execution complete",
            "suppliers_checked": len(suppliers),
            "alerts_generated": reports_generated
        })
    }