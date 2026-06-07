import pandas as pd
from graph import create_graph
import os
from pathlib import Path
from dotenv import load_dotenv # type: ignore
import groq

# Load environment variables from parent directory (.env file)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Also try loading from current directory
load_dotenv()

# Configure Groq client globally
client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

def run_autonomous_check():
    # Load Suppliers
    suppliers = pd.read_csv("suppliers.csv")
    app = create_graph()

    print("CHAI 2.0 Autonomous Agent Starting...")

    for _, supplier in suppliers.iterrows():
        print(f"\n--- Checking Supplier: {supplier['supplier_name']} ---")

        # Initial State
        initial_state = {
            "supplier_info": supplier.to_dict(),
            "raw_news": [],
            "identified_risks": [],
            "final_alert": "",
            "logs": []
        }

        # Run the Agent
        final_output = app.invoke(initial_state)

        print(final_output["final_alert"])
        for log in final_output["logs"]:
            print(f"DEBUG: {log}")

if __name__ == "__main__":
    run_autonomous_check()