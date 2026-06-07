# 🚀 CHAI 2.0 Dashboard - Quick Start Guide

## ⚡ Fastest Way to Get Started (5 Minutes)

### For Windows Users: 
**Double-click → Done! 🎉**
```
run_dashboard.bat
```
Everything else is automatic!

---

## 📋 Manual Setup (if batch script doesn't work)

### Step 1: Install Dependencies (1 minute)
```bash
pip install -r requirements.txt
```

### Step 2: Configure API Keys (1 minute)

Create a `.env` file in the project folder:

**Windows (File Explorer):**
1. Right-click → New → Text Document
2. Name it `.env` (with the dot!)
3. Open and add:
```
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```

**Or Terminal:**
```bash
# Windows
echo GROQ_API_KEY=your_key > .env
echo TAVILY_API_KEY=your_key >> .env

# Mac/Linux
echo "GROQ_API_KEY=your_key" > .env
echo "TAVILY_API_KEY=your_key" >> .env
```

### Step 3: Start Services (2 minutes)

**Terminal 1 - Start Backend API:**
```bash
python api.py
```
You should see: `Running on http://0.0.0.0:5000`

**Terminal 2 - Start Dashboard:**
```bash
streamlit run dashboard.py
```
Dashboard opens automatically at `http://localhost:8501`

---

## ✨ Dashboard Features

### Left Sidebar Menu
- **Filters**: Choose alert severity and regions
- **Auto Refresh**: Set refresh interval
- **View Modes**: Switch between Dashboard/Analytics/Alerts/Suppliers
- **System Status**: See if system is healthy

### Dashboard Tab (Main View)
```
📊 Key Metrics (4 cards at top)
├─ Total Suppliers
├─ High Risk Count  
├─ Active Alerts
└─ System Health

🚨 Real-Time Alerts Section
├─ Alert cards with severity colors
└─ Action buttons

🗺️ Risk Charts
├─ Pie chart: Risk distribution
└─ Bar chart: Risk by category

📋 Suppliers Table
└─ Complete supplier list with status
```

### Other Tabs
- **📈 Analytics**: Trends and visualizations
- **🚨 Alerts**: Full alert management
- **📋 Suppliers**: Add/edit suppliers

---

## 🎮 How to Use

### View All Suppliers
1. Go to **Suppliers** tab
2. See the complete list
3. Click on a supplier for details

### Add New Supplier
1. Go to **Suppliers** tab
2. Click "➕ Add New Supplier"
3. Fill in the form:
   - Supplier Name
   - Region
   - Category
   - Risk Level
4. Click "Add Supplier"

### Check Alerts
1. Go to **Alerts** tab
2. Use search to find specific alerts
3. Sort by Latest/Severity/Supplier
4. Click expander to view details
5. Take action: Send, Acknowledge, or Archive

### View Analytics
1. Go to **Analytics** tab
2. See 30-day alert trends
3. Review risk categories
4. Analyze patterns

---

## 🔌 API Usage Examples

### Check if API is Running
```bash
curl http://localhost:5000/api/health
```

### Get All Suppliers
```bash
curl http://localhost:5000/api/suppliers
```

### Add New Supplier
```bash
curl -X POST http://localhost:5000/api/suppliers \
  -H "Content-Type: application/json" \
  -d '{"supplier_name":"New Corp","region":"Asia","category":"Electronics","risk_level":"Low"}'
```

### Get All Alerts
```bash
curl http://localhost:5000/api/alerts
```

### Run Agent Check
```bash
curl -X POST http://localhost:5000/api/agents/run
```

---

## 🎨 Dashboard Colors & Meaning

| Color | Meaning | Action |
|-------|---------|--------|
| 🔴 Red/Pink | **High Risk** | Immediate attention needed |
| 🟡 Yellow | **Medium Risk** | Monitor closely |
| 🔵 Blue | **Low Risk** | Normal monitoring |
| 🟢 Green | **Safe** | No action required |

---

## 📱 Responsive Design

Dashboard works on:
- 🖥️ Desktop computers
- 💻 Laptops
- 📱 Tablets
- 📞 Mobile phones

Just resize the window or rotate your device!

---

## 🔐 Keeping Your Keys Secure

**IMPORTANT:** Never commit `.env` file to GitHub!

Check `.gitignore` includes:
```
.env
*.pyc
__pycache__/
```

---

## ⚠️ Common Issues & Fixes

### "Module not found" error?
```bash
# Reinstall requirements
pip install -r requirements.txt
```

### Port already in use?
```bash
# Change port in different terminal
# Kill the process using the port

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Mac/Linux:
lsof -i :5000
kill -9 <PID_NUMBER>
```

### Dashboard doesn't load?
```bash
# Clear cache
streamlit cache clear

# Check dependencies
pip list | grep streamlit
```

### API not responding?
```bash
# Verify it's running
curl http://localhost:5000/api/health

# Check firewall isn't blocking port 5000
```

---

## 🐳 Using Docker (Advanced)

If you have Docker installed:

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 📊 File Structure

```
📁 Project Root
├── 📄 dashboard.py              ← Main dashboard
├── 📄 api.py                   ← Backend API
├── 📄 run_dashboard.bat        ← Windows launcher ⭐
├── 📄 requirements.txt         ← Dependencies
├── 📄 suppliers.csv           ← Your suppliers
├── 📄 global_events.csv       ← Global events
└── 📄 .env                    ← Your API keys (secret!)
```

---

## 🎓 Next Steps

1. ✅ Run `run_dashboard.bat` or start services manually
2. ✅ Open dashboard at http://localhost:8501
3. ✅ Add some suppliers via Suppliers tab
4. ✅ Explore all dashboard views
5. ✅ Test API endpoints with curl
6. ✅ Set up auto-refresh interval
7. ✅ Customize filters and settings

---

## 📚 Learn More

- **Detailed Setup**: Read `SETUP_GUIDE.md`
- **Feature Docs**: Read `DASHBOARD_README.md`
- **API Reference**: Check `DASHBOARD_README.md` → API Endpoints
- **Troubleshooting**: See "Common Issues" section above

---

## 💡 Pro Tips

1. **Keep Dashboard Running**: Leave it open during work day
2. **Set Auto-Refresh**: Choose 5-10 min interval for real-time updates
3. **Use Alerts Filters**: Focus on High severity first
4. **Regular Backups**: Keep backup of suppliers.csv
5. **Monitor API Logs**: Watch API terminal for errors
6. **Check System Health**: See metric in top-right corner

---

## 🆘 Need Help?

1. Check if services are running
2. Verify `.env` file exists with API keys
3. Check console for error messages
4. Try restarting services
5. Look at the troubleshooting section above

**You got this!** 🚀

---

## 🎉 Congratulations!

You now have:
✅ Modern web dashboard  
✅ REST API backend  
✅ Real-time alert monitoring  
✅ Supplier management  
✅ Risk analytics  

**Go explore and monitor those supply chains!** 📊
