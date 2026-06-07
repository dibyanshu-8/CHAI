# CHAI 2.0 Dashboard - User Guide

Welcome to the **Cognitive Hazard AI Dashboard** - a modern, responsive web interface for real-time supply chain intelligence monitoring.

---

## 📋 Overview

The CHAI 2.0 Dashboard provides:

✅ **Real-time Alert Monitoring** - Live supply chain risk alerts  
✅ **Supplier Management** - Add, update, delete suppliers  
✅ **Risk Analytics** - Visual analytics and trend analysis  
✅ **Agent Control** - Trigger autonomous agent checks  
✅ **REST API** - Full API for programmatic access  
✅ **Responsive Design** - Works on desktop, tablet, and mobile  

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Environment

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. Run the Dashboard

**Option A: Dashboard Only (Streamlit)**
```bash
streamlit run dashboard.py
```

The dashboard will open at: `http://localhost:8501`

**Option B: Dashboard + API (Recommended)**

Terminal 1 - Start the API:
```bash
python api.py
```
API runs at: `http://localhost:5000`

Terminal 2 - Start the Dashboard:
```bash
streamlit run dashboard.py
```
Dashboard runs at: `http://localhost:8501`

---

## 🎨 Dashboard Features

### 📊 Dashboard Tab
- **Key Metrics**: Total suppliers, high-risk count, active alerts, system health
- **Real-Time Alerts**: Live alert feed with severity indicators
- **Risk Overview**: Interactive charts showing risk distribution
- **Suppliers Database**: Complete supplier inventory with status badges

### 📈 Analytics Tab
- **Alert Trends**: 30-day alert frequency visualization
- **Risk Breakdown**: Alert distribution by category
- **Risk Heatmaps**: Geopolitical, weather, labor, logistics analysis

### 🚨 Alerts Tab
- **Alert Management**: Search, filter, and sort alerts
- **Alert Details**: Comprehensive alert information
- **Actions**: Acknowledge, send, or archive alerts

### 📋 Suppliers Tab
- **Add Suppliers**: Easy form to add new suppliers
- **View All**: Complete supplier database
- **Manage**: Update or delete suppliers
- **Risk Assessment**: Real-time risk level monitoring

---

## 🔧 API Endpoints

### Dashboard Overview
```
GET /api/dashboard/overview
GET /api/dashboard/metrics
```

### Suppliers Management
```
GET    /api/suppliers                    # Get all suppliers
GET    /api/suppliers/<supplier_name>   # Get specific supplier
POST   /api/suppliers                    # Add new supplier
PUT    /api/suppliers/<supplier_name>   # Update supplier
DELETE /api/suppliers/<supplier_name>   # Delete supplier
```

### Alerts Management
```
GET    /api/alerts                       # Get all alerts
GET    /api/alerts/<alert_id>           # Get specific alert
POST   /api/alerts                       # Create manual alert
POST   /api/alerts/<alert_id>/acknowledge
POST   /api/alerts/<alert_id>/resolve
```

### Agent Control
```
POST   /api/agents/run                   # Run all agents
POST   /api/agents/run/<supplier_name>  # Run agent for specific supplier
GET    /api/agents/status               # Get agents status
```

### System
```
GET    /api/events                       # Get global events
GET    /api/health                       # Health check
```

---

## 📊 Dashboard Settings

### Sidebar Controls

**Filters:**
- Alert Severity (High, Medium, Low, Critical)
- Regions (Asia, Europe, Americas, Africa)

**Auto Refresh:**
- Configurable refresh interval (1, 5, 10, 30, 60 minutes)

**Display Mode:**
- Dashboard (Overview)
- Analytics (Trends & Analysis)
- Alerts (Alert Management)
- Suppliers (Supplier Management)

---

## 🎯 Example Usage

### Adding a New Supplier via API
```bash
curl -X POST http://localhost:5000/api/suppliers \
  -H "Content-Type: application/json" \
  -d '{
    "supplier_name": "New Supplier",
    "region": "Asia",
    "category": "Electronics",
    "risk_level": "Low"
  }'
```

### Triggering Agent Check
```bash
curl -X POST http://localhost:5000/api/agents/run \
  -H "Content-Type: application/json"
```

### Getting Alerts
```bash
curl http://localhost:5000/api/alerts?severity=High
```

---

## 📱 Responsive Design

The dashboard is fully responsive and optimized for:
- 🖥️ Desktop (1920px+)
- 💻 Laptop (1024px-1920px)
- 📱 Tablet (768px-1024px)
- 📞 Mobile (320px-768px)

---

## 🔐 Security Notes

1. **API Keys**: Always use environment variables for API keys
2. **CORS**: API has CORS enabled for dashboard access
3. **Authentication**: Consider adding API authentication for production
4. **Data**: Supplier and alert data stored locally in CSV files

---

## 🐛 Troubleshooting

### Dashboard won't load?
```bash
# Clear Streamlit cache
streamlit cache clear

# Run with verbose output
streamlit run dashboard.py --logger.level=debug
```

### API connection issues?
```bash
# Check if API is running
curl http://localhost:5000/api/health

# Check ports aren't in use
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Mac/Linux
```

### Missing data files?
- Ensure `suppliers.csv` and `global_events.csv` are in the project root
- Dashboard will create default data if files don't exist

---

## 📦 Project Structure

```
.
├── dashboard.py          # Streamlit dashboard UI
├── api.py               # Flask REST API backend
├── graph.py             # LangGraph agent orchestration
├── state.py             # Agent state definitions
├── main.py              # Autonomous execution script
├── requirements.txt     # Python dependencies
├── suppliers.csv        # Supplier database
├── global_events.csv    # Global events data
└── README.md            # This file
```

---

## 🚀 Production Deployment

### Docker Deployment

```bash
# Build Docker image
docker build -t chai-dashboard .

# Run container (Dashboard + API)
docker run -p 8501:8501 -p 5000:5000 \
  -e GROQ_API_KEY=your_key \
  -e TAVILY_API_KEY=your_key \
  chai-dashboard
```

### Environment Setup
```bash
# Create .env file
cat > .env << EOF
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
EOF
```

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check console logs for errors
4. Verify environment variables are set

---

## 📝 License

This project is part of Cognitive Hazard AI (CHAI) 2.0

**Version**: 2.0  
**Last Updated**: 2024
