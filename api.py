"""
CHAI 2.0 - REST API Backend
Provides endpoints for dashboard integration with the autonomous agent system
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import pandas as pd
import json
import os
from dotenv import load_dotenv
import threading
from graph import create_graph
import groq

# Load environment
load_dotenv(override=True)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for dashboard

# Configure Groq client
groq_client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

# In-memory storage for alerts and results
alerts_store = []
suppliers_status = {}
system_metrics = {
    "total_runs": 0,
    "successful_alerts": 0,
    "failed_alerts": 0,
    "last_run": None,
    "system_health": 98
}

# ============= UTILITY FUNCTIONS =============

def load_suppliers():
    """Load suppliers from CSV"""
    try:
        return pd.read_csv("suppliers.csv").to_dict('records')
    except FileNotFoundError:
        return []

def load_global_events():
    """Load global events from CSV"""
    try:
        return pd.read_csv("global_events.csv").to_dict('records')
    except FileNotFoundError:
        return []

def run_agent_check(supplier_info):
    """Run the autonomous agent check for a supplier"""
    try:
        app_graph = create_graph()
        
        initial_state = {
            "supplier_info": supplier_info,
            "raw_news": [],
            "identified_risks": [],
            "final_alert": "",
            "logs": []
        }
        
        result = app_graph.invoke(initial_state)
        
        alert = {
            "id": f"ALT-{int(datetime.now().timestamp())}",
            "supplier": supplier_info.get('supplier_name', 'Unknown'),
            "timestamp": datetime.now().isoformat(),
            "status": "processed",
            "alert_data": result.get('final_alert', ''),
            "risks": result.get('identified_risks', []),
            "logs": result.get('logs', [])
        }
        
        return alert
    except Exception as e:
        return {
            "id": f"ERR-{int(datetime.now().timestamp())}",
            "supplier": supplier_info.get('supplier_name', 'Unknown'),
            "timestamp": datetime.now().isoformat(),
            "status": "error",
            "error": str(e)
        }

# ============= API ENDPOINTS =============

# === Dashboard Overview ===

@app.route('/api/dashboard/overview', methods=['GET'])
def get_dashboard_overview():
    """Get dashboard overview metrics"""
    suppliers = load_suppliers()
    
    overview = {
        "timestamp": datetime.now().isoformat(),
        "total_suppliers": len(suppliers),
        "total_alerts": len(alerts_store),
        "active_alerts": len([a for a in alerts_store if a.get('severity') == 'High']),
        "system_health": system_metrics['system_health'],
        "metrics": {
            "total_runs": system_metrics['total_runs'],
            "successful": system_metrics['successful_alerts'],
            "failed": system_metrics['failed_alerts'],
            "last_run": system_metrics['last_run']
        }
    }
    
    return jsonify(overview)

@app.route('/api/dashboard/metrics', methods=['GET'])
def get_metrics():
    """Get detailed metrics"""
    suppliers = load_suppliers()
    
    risk_distribution = {
        'High': 0,
        'Medium': 0,
        'Low': 0
    }
    
    for supplier in suppliers:
        risk = supplier.get('risk_level', 'Low')
        if risk in risk_distribution:
            risk_distribution[risk] += 1
    
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "risk_distribution": risk_distribution,
        "supplier_count": len(suppliers),
        "alert_count": len(alerts_store),
        "system_status": "operational"
    }
    
    return jsonify(metrics)

# === Suppliers Endpoints ===

@app.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    """Get all suppliers"""
    suppliers = load_suppliers()
    return jsonify({
        "status": "success",
        "data": suppliers,
        "count": len(suppliers)
    })

@app.route('/api/suppliers/<supplier_name>', methods=['GET'])
def get_supplier(supplier_name):
    """Get specific supplier details"""
    suppliers = load_suppliers()
    supplier = next((s for s in suppliers if s.get('supplier_name') == supplier_name), None)
    
    if supplier:
        return jsonify({
            "status": "success",
            "data": supplier
        })
    
    return jsonify({
        "status": "error",
        "message": "Supplier not found"
    }), 404

@app.route('/api/suppliers', methods=['POST'])
def add_supplier():
    """Add new supplier"""
    try:
        data = request.json
        
        suppliers = load_suppliers()
        new_supplier = {
            "supplier_name": data.get('supplier_name'),
            "region": data.get('region'),
            "category": data.get('category'),
            "risk_level": data.get('risk_level', 'Low')
        }
        
        suppliers.append(new_supplier)
        
        # Save to CSV
        df = pd.DataFrame(suppliers)
        df.to_csv("suppliers.csv", index=False)
        
        return jsonify({
            "status": "success",
            "message": "Supplier added successfully",
            "data": new_supplier
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/api/suppliers/<supplier_name>', methods=['PUT'])
def update_supplier(supplier_name):
    """Update supplier details"""
    try:
        data = request.json
        suppliers = load_suppliers()
        
        supplier = next((s for s in suppliers if s.get('supplier_name') == supplier_name), None)
        if not supplier:
            return jsonify({"status": "error", "message": "Supplier not found"}), 404
        
        # Update fields
        supplier.update(data)
        
        # Save to CSV
        df = pd.DataFrame(suppliers)
        df.to_csv("suppliers.csv", index=False)
        
        return jsonify({
            "status": "success",
            "message": "Supplier updated successfully",
            "data": supplier
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/api/suppliers/<supplier_name>', methods=['DELETE'])
def delete_supplier(supplier_name):
    """Delete supplier"""
    try:
        suppliers = load_suppliers()
        suppliers = [s for s in suppliers if s.get('supplier_name') != supplier_name]
        
        # Save to CSV
        df = pd.DataFrame(suppliers)
        df.to_csv("suppliers.csv", index=False)
        
        return jsonify({
            "status": "success",
            "message": "Supplier deleted successfully"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# === Alerts Endpoints ===

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get all alerts"""
    severity = request.args.get('severity')
    supplier = request.args.get('supplier')
    
    filtered = alerts_store
    
    if severity:
        filtered = [a for a in filtered if a.get('severity') == severity]
    
    if supplier:
        filtered = [a for a in filtered if a.get('supplier') == supplier]
    
    return jsonify({
        "status": "success",
        "data": filtered,
        "count": len(filtered)
    })

@app.route('/api/alerts/<alert_id>', methods=['GET'])
def get_alert(alert_id):
    """Get specific alert"""
    alert = next((a for a in alerts_store if a.get('id') == alert_id), None)
    
    if alert:
        return jsonify({
            "status": "success",
            "data": alert
        })
    
    return jsonify({
        "status": "error",
        "message": "Alert not found"
    }), 404

@app.route('/api/alerts', methods=['POST'])
def create_alert():
    """Create new alert (manual)"""
    try:
        data = request.json
        
        alert = {
            "id": f"ALT-{int(datetime.now().timestamp())}",
            "supplier": data.get('supplier'),
            "severity": data.get('severity', 'Medium'),
            "title": data.get('title'),
            "description": data.get('description'),
            "timestamp": datetime.now().isoformat(),
            "mitigation": data.get('mitigation', 'Monitor situation'),
            "status": "active"
        }
        
        alerts_store.append(alert)
        
        return jsonify({
            "status": "success",
            "message": "Alert created successfully",
            "data": alert
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/api/alerts/<alert_id>/acknowledge', methods=['POST'])
def acknowledge_alert(alert_id):
    """Acknowledge an alert"""
    alert = next((a for a in alerts_store if a.get('id') == alert_id), None)
    
    if alert:
        alert['status'] = 'acknowledged'
        alert['acknowledged_at'] = datetime.now().isoformat()
        
        return jsonify({
            "status": "success",
            "message": "Alert acknowledged",
            "data": alert
        })
    
    return jsonify({
        "status": "error",
        "message": "Alert not found"
    }), 404

@app.route('/api/alerts/<alert_id>/resolve', methods=['POST'])
def resolve_alert(alert_id):
    """Resolve an alert"""
    alert = next((a for a in alerts_store if a.get('id') == alert_id), None)
    
    if alert:
        alert['status'] = 'resolved'
        alert['resolved_at'] = datetime.now().isoformat()
        
        return jsonify({
            "status": "success",
            "message": "Alert resolved",
            "data": alert
        })
    
    return jsonify({
        "status": "error",
        "message": "Alert not found"
    }), 404

# === Agent Execution Endpoints ===

@app.route('/api/agents/run', methods=['POST'])
def run_agents():
    """Trigger autonomous agent check"""
    try:
        suppliers = load_suppliers()
        
        results = []
        for supplier in suppliers:
            alert = run_agent_check(supplier)
            alerts_store.append(alert)
            results.append(alert)
        
        system_metrics['total_runs'] += 1
        system_metrics['last_run'] = datetime.now().isoformat()
        system_metrics['successful_alerts'] += len([a for a in results if a.get('status') == 'processed'])
        system_metrics['failed_alerts'] += len([a for a in results if a.get('status') == 'error'])
        
        return jsonify({
            "status": "success",
            "message": "Agent checks completed",
            "alerts_generated": len(results),
            "data": results
        }), 200
    except Exception as e:
        system_metrics['failed_alerts'] += 1
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/agents/run/<supplier_name>', methods=['POST'])
def run_agent_for_supplier(supplier_name):
    """Trigger agent check for specific supplier"""
    try:
        suppliers = load_suppliers()
        supplier = next((s for s in suppliers if s.get('supplier_name') == supplier_name), None)
        
        if not supplier:
            return jsonify({
                "status": "error",
                "message": "Supplier not found"
            }), 404
        
        alert = run_agent_check(supplier)
        alerts_store.append(alert)
        
        system_metrics['total_runs'] += 1
        system_metrics['last_run'] = datetime.now().isoformat()
        
        return jsonify({
            "status": "success",
            "message": "Agent check completed",
            "data": alert
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/agents/status', methods=['GET'])
def get_agents_status():
    """Get agents status"""
    return jsonify({
        "status": "operational",
        "agents": {
            "researcher": "active",
            "analyst": "active",
            "alerter": "active"
        },
        "metrics": system_metrics,
        "timestamp": datetime.now().isoformat()
    })

# === Events Endpoints ===

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get global events"""
    events = load_global_events()
    
    return jsonify({
        "status": "success",
        "data": events,
        "count": len(events)
    })

# === System Health ===

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "running",
        "version": "2.0"
    }), 200

# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

# ============= MAIN =============

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )
