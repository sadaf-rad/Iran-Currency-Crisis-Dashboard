# 🚀 Quick Start Guide

## Get Your Dashboard Running in 5 Minutes!

### Step 1: Install Dependencies (2 minutes)

```bash
cd /Users/sadaf/Desktop/da/first

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Run the Dashboard (1 minute)

```bash
streamlit run app.py
```

Your browser will automatically open to: `http://localhost:8501`

### Step 3: Explore! (2 minutes)

Navigate through the 6 dashboard pages:
1. 📈 Overview - Key metrics and trends
2. 📉 Time Series Analysis - Price charts and patterns
3. 🚨 Crisis Analysis - Crisis detection results
4. 📰 News Impact - Geopolitical correlation
5. 📊 Risk Metrics - VaR, volatility analysis
6. 💡 Insights - Key findings and recommendations

---

## 📁 File Checklist

Make sure you have these files:

```
✅ app.py                              - Main dashboard
✅ requirements.txt                    - Dependencies
✅ Dollar_Rial_Price_Dataset.csv      - Main data
✅ crisis_days_with_news_english.csv  - News data
✅ .streamlit/config.toml             - Configuration
✅ README.md                          - Documentation
✅ DEPLOYMENT.md                      - Deployment guide
```

---

## 🎯 Next Steps

### For Testing Locally:
1. Run the dashboard
2. Test all 6 pages
3. Try the date filters
4. Verify charts load correctly

### For Deployment:
1. Read `DEPLOYMENT.md`
2. Push to GitHub
3. Deploy to Streamlit Cloud (FREE!)
4. Share your live link with recruiters

### For Job Applications:
1. Add live demo link to resume
2. Add GitHub link to LinkedIn
3. Take screenshots for portfolio
4. Prepare talking points about the project

---

## 🐛 Troubleshooting

**Problem**: `streamlit: command not found`
```bash
pip install streamlit
# OR if using venv:
source venv/bin/activate
```

**Problem**: `FileNotFoundError` for CSV
```bash
# Make sure you're in the correct directory
cd /Users/sadaf/Desktop/da/first
ls *.csv  # Should see your CSV files
```

**Problem**: Dashboard shows errors
```bash
# Check if all packages installed correctly
pip install -r requirements.txt --upgrade
```

---

## 💡 Demo Tips for Recruiters

When presenting your dashboard:

1. **Start with Overview Page**
   - Show key metrics
   - Explain the data (14 years, 3,666 days)
   - Highlight crisis detection (372 crisis days)

2. **Show Time Series Analysis**
   - Interactive charts
   - Moving averages
   - Seasonal patterns

3. **Explain Crisis Detection**
   - Algorithm methodology
   - Statistical thresholds
   - Business impact

4. **Demonstrate Technical Skills**
   - Python, Pandas, Streamlit
   - SQL integration
   - API usage (GDELT)
   - Data visualization

5. **Discuss Business Value**
   - Risk management applications
   - Predictive potential
   - Real-world use cases

---

## 📧 Need Help?

- Check `README.md` for full documentation
- See `DEPLOYMENT.md` for deployment instructions
- Open an issue on GitHub
- Contact: your-email@example.com

---

**Ready to impress recruiters? Let's go! 🚀**
