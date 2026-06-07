# CHAI 2.0 Dashboard Setup & Integration Guide

## 🎯 Overview

This guide explains how to set up and run the CHAI 2.0 Dashboard - a modern, responsive web interface for real-time supply chain intelligence monitoring.

---

## 📦 What's Included

| Component | Purpose | Port |
|-----------|---------|------|
| **dashboard.py** | Streamlit UI Dashboard | 8501 |
| **api.py** | REST API Backend | 5000 |
| **run_dashboard.bat** | Windows startup script | - |
| **docker-compose.yml** | Container orchestration | 5000, 8501 |

---

## 🚀 Installation Methods

### Method 1: Direct Installation (Recommended for Development)

#### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 2: Configure Environment
Create `.env` file in project root:
```env
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```

#### Step 3: Run Services

**Terminal 1 - Start API Backend:**
```bash
python api.py
```

**Terminal 2 - Start Dashboard:**
```bash
streamlit run dashboard.py
```

**Access Dashboard:** http://localhost:8501

---

### Method 2: Windows Batch Script (Easiest for Windows Users)

Simply double-click `run_dashboard.bat` - it will:
- ✅ Check dependencies
- ✅ Install missing packages
- ✅ Start API server
- ✅ Start Dashboard
- ✅ Open in browser

---

### Method 3: Docker Deployment (Production)

#### Step 1: Create `.env` file
```env
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```

#### Step 2: Build and Run
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

**Access Services:**
- Dashboard: http://localhost:8501
- API: http://localhost:5000

#### Step 3: Stop Services
```bash
docker-compose down
```

---

## 🎨 Dashboard Features

### 📊 Dashboard View
```
Key Metrics (4 cards)
├── Total Suppliers
├── High Risk Count
├── Active Alerts
└── System Health

Real-Time Alerts Section
├── Alert Cards with severity levels
└── View Details buttons

Supplier Risk Overview
├── Pie Chart: Risk Distribution
└── Bar Chart: Risk by Category

Suppliers Database
├── Interactive table
└── Detailed supplier expander
```

### 📈 Analytics View
```
Alert Trends
├── 30-day timeline chart
└── Alert frequency analysis

Risk Category Breakdown
└── Distribution by type
    ├── Geopolitical
    ├── Weather
    ├── Labor
    ├── Logistics
    └── Market
```

### 🚨 Alerts View
```
Alert Management
├── Search functionality
├── Sort options
└── Individual alert details
    ├── Description
    ├── Timestamp
    ├── Mitigation steps
    └── Action buttons
```

### 📋 Suppliers View
```
Supplier Management
├── Add New Supplier form
├── All suppliers list
└── Edit/Delete options
```

---

## 🔌 API Integration

### Core API Endpoints

#### Dashboard Metrics
```bash
# Get overview
GET /api/dashboard/overview

# Get detailed metrics
GET /api/dashboard/metrics

Response:
{
  "timestamp": "2024-01-15T10:30:00",
  "total_suppliers": 10,
  "total_alerts": 5,
  "active_alerts": 3,
  "system_health": 98
}
```

#### Suppliers API
```bash
# Get all suppliers
GET /api/suppliers

# Get specific supplier
GET /api/suppliers/{supplier_name}

# Add supplier
POST /api/suppliers
{
  "supplier_name": "New Corp",
  "region": "Asia",
  "category": "Electronics",
  "risk_level": "Low"
}

# Update supplier
PUT /api/suppliers/{supplier_name}
{
  "risk_level": "Medium"
}

# Delete supplier
DELETE /api/suppliers/{supplier_name}
```

#### Alerts API
```bash
# Get all alerts
GET /api/alerts

# Get by severity
GET /api/alerts?severity=High

# Get by supplier
GET /api/alerts?supplier={name}

# Create alert
POST /api/alerts
{
  "supplier": "Supplier Name",
  "severity": "High",
  "title": "Alert Title",
  "description": "Alert details"
}

# Acknowledge alert
POST /api/alerts/{alert_id}/acknowledge

# Resolve alert
POST /api/alerts/{alert_id}/resolve
```

#### Agent Control API
```bash
# Run agents for all suppliers
POST /api/agents/run

# Run agent for specific supplier
POST /api/agents/run/{supplier_name}

# Get agent status
GET /api/agents/status

# Get global events
GET /api/events

# Health check
GET /api/health
```

---

## 🔗 Connecting with Existing Agent System

### Integration Architecture

```
┌─────────────────────┐
│  Autonomous Agents  │
│  (graph.py)         │
└──────────┬──────────┘
           │
           ├──> api.py (REST API)
           │         │
           │         └──> alerts_store (in-memory)
           │
           └──> dashboard.py (Streamlit UI)
                     │
                     └──> Visualizations & Forms
```

### How It Works

1. **Agent Execution**: Your `graph.py` agents run and generate alerts
2. **API Receives**: Flask API stores results in `alerts_store`
3. **Dashboard Display**: Streamlit dashboard fetches from API
4. **Real-time Updates**: Dashboard auto-refreshes based on settings

### Connecting Your Agents

Your `graph.py` is already compatible! The API automatically:
- ✅ Loads suppliers from `suppliers.csv`
- ✅ Executes your agent graph
- ✅ Stores results as alerts
- ✅ Makes them available in dashboard

---

## 🛠️ Configuration

### Dashboard Settings (Sidebar)

**Filters:**
- Alert Severity: High, Medium, Low, Critical
- Regions: Asia, Europe, Americas, Africa

**Auto Refresh:**
- 1, 5, 10, 30, or 60 minutes

**Display Modes:**
- Dashboard (Overview)
- Analytics (Trends)
- Alerts (Management)
- Suppliers (Admin)

### Streamlit Config (.streamlit/config.toml)

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"

[server]
port = 8501
headless = true

[logger]
level = "info"
```

---

## 📊 Data Files

### suppliers.csv
Required columns:
```csv
supplier_name,region,category,risk_level
Supplier A,China,Electronics,High
Supplier B,Vietnam,Manufacturing,Low
```

### global_events.csv
Optional - for context in agents:
```csv
event_date,region,event_type,description
2024-01-15,China,Geopolitical,Trade tensions update
```

---

## 🧪 Testing the Setup

### Quick Test

1. **Start Services**
   ```bash
   python api.py  # Terminal 1
   streamlit run dashboard.py  # Terminal 2
   ```

2. **Test API**
   ```bash
   curl http://localhost:5000/api/health
   curl http://localhost:5000/api/suppliers
   ```

3. **Test Dashboard**
   - Open http://localhost:8501
   - Navigate through views
   - Try adding a supplier

### Verify Setup

- [ ] API running on port 5000
- [ ] Dashboard running on port 8501
- [ ] Dashboard loads without errors
- [ ] Can view suppliers
- [ ] Can view alerts
- [ ] Can add new supplier

---

## 🐛 Troubleshooting

### Dashboard Won't Load
```bash
# Clear Streamlit cache
streamlit cache clear

# Check if port 8501 is free
netstat -ano | findstr :8501
```

### API Connection Errors
```bash
# Verify API is running
curl http://localhost:5000/api/health

# Check firewall
# Make sure port 5000 is allowed
```

### Missing Data
- Ensure `suppliers.csv` exists in project root
- Dashboard creates default data if missing

### Module Import Errors
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall

# Check Python version (3.8+)
python --version
```

---

## 🚀 Production Deployment

### With Docker

```bash
# Build and deploy
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f dashboard

# Stop services
docker-compose down
```

### Environment Variables

Create `.env`:
```env
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key
```

Load in docker-compose automatically.

---

## 📝 Project Structure

```
├── dashboard.py              # Streamlit UI
├── api.py                   # Flask API
├── graph.py                 # Agent DAG
├── state.py                 # Agent state
├── main.py                  # Autonomous runner
├── requirements.txt         # Dependencies
├── suppliers.csv           # Supplier data
├── global_events.csv       # Event data
├── Dockerfile              # Container setup
├── docker-compose.yml      # Multi-container
├── run_dashboard.bat       # Windows launcher
├── .streamlit/config.toml  # Streamlit config
├── DASHBOARD_README.md     # Dashboard docs
└── SETUP_GUIDE.md         # This file
```

---

## 📚 Next Steps

1. ✅ Follow setup method (1, 2, or 3)
2. ✅ Verify services are running
3. ✅ Open dashboard at http://localhost:8501
4. ✅ Test API endpoints
5. ✅ Explore dashboard features
6. ✅ Customize as needed

---

## 💡 Tips & Best Practices

- **Development**: Use Method 1 (Direct Installation)
- **Quick Testing**: Use Method 2 (Batch Script)
- **Production**: Use Method 3 (Docker)
- **Performance**: Run API and Dashboard on separate machines in production
- **Security**: Use environment variables for API keys
- **Monitoring**: Check logs regularly

---

## 📞 Support

- Check DASHBOARD_README.md for feature docs
- Review API endpoint documentation
- Check console logs for error messages
- Verify environment variables are set

**Happy monitoring!** 🚀
