# 🚀 Deployment Guide - Iran Currency Crisis Dashboard

This guide provides step-by-step instructions for deploying your dashboard online so recruiters can access it.

---

## 📋 Table of Contents
1. [Streamlit Cloud Deployment (Recommended - FREE)](#streamlit-cloud-deployment)
2. [Heroku Deployment](#heroku-deployment)
3. [Post-Deployment Checklist](#post-deployment-checklist)

---

## 🎯 Option 1: Streamlit Cloud Deployment (RECOMMENDED)

**Best for**: Quick, free deployment with zero configuration

### Prerequisites
- GitHub account
- Git installed on your computer
- Your project pushed to GitHub

### Step-by-Step Instructions

#### 1. Prepare Your Repository

Make sure your GitHub repo has these files in the root:
```
Currency-Convertor/
├── app.py                     # ✅ Must be in root
├── requirements.txt           # ✅ Must be in root
├── Dollar_Rial_Price_Dataset.csv  # ✅ Data files
├── crisis_days_with_news_english.csv
└── .streamlit/
    └── config.toml
```

#### 2. Push to GitHub

```bash
# If not already initialized
git init
git add .
git commit -m "Initial commit for deployment"

# Create new repo on GitHub, then:
git remote add origin https://github.com/sadaf-rad/Currency-Convertor.git
git branch -M main
git push -u origin main
```

#### 3. Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: [share.streamlit.io](https://share.streamlit.io)
   - Click "Sign in" and authenticate with GitHub

2. **Create New App**
   - Click "New app" button
   - Select your repository: `sadaf-rad/Currency-Convertor`
   - Set **Branch**: `main`
   - Set **Main file path**: `app.py`
   - Click "Advanced settings" (optional)
     - Set Python version: `3.11`
   
3. **Deploy**
   - Click "Deploy!"
   - Wait 2-3 minutes for deployment
   - Your app will be live at: `https://sadaf-rad-currency-convertor.streamlit.app`

#### 4. Verify Deployment

- Test all dashboard pages
- Verify data loads correctly
- Check all visualizations render
- Test date filters and interactivity

---

## 🔧 Option 2: Heroku Deployment

**Best for**: More control, custom domain options

### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed

### Step-by-Step Instructions

#### 1. Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows (download installer)
# https://devcenter.heroku.com/articles/heroku-cli

# Verify installation
heroku --version
```

#### 2. Create Additional Files

**Create `setup.sh`:**
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@example.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

**Create `Procfile`:**
```
web: sh setup.sh && streamlit run app.py
```

**Update `requirements.txt`** (add at the end):
```
streamlit==1.29.0
```

#### 3. Initialize Heroku

```bash
# Login to Heroku
heroku login

# Create new app
heroku create sadaf-currency-crisis-dashboard

# Or if name taken, Heroku will generate a random name
heroku create
```

#### 4. Deploy to Heroku

```bash
# Add files
git add setup.sh Procfile
git commit -m "Add Heroku deployment files"

# Push to Heroku
git push heroku main

# Open your app
heroku open
```

Your app will be at: `https://sadaf-currency-crisis-dashboard.herokuapp.com`

#### 5. Monitor Logs

```bash
# View real-time logs
heroku logs --tail

# Check app status
heroku ps
```

---

## ✅ Post-Deployment Checklist

### 1. Test Your Live App
- [ ] Dashboard loads without errors
- [ ] All 6 pages are accessible
- [ ] Data visualizations render correctly
- [ ] Date filters work properly
- [ ] News section displays (if data available)
- [ ] Mobile responsive design works

### 2. Update Your Materials

**Update README.md** with live link:
```markdown
🔗 **[Live Demo](https://your-actual-url.streamlit.app)**
```

**Add to Your Resume:**
```
Iran Currency Crisis Dashboard
• Live Demo: https://your-app.streamlit.app
• GitHub: https://github.com/sadaf-rad/Currency-Convertor
```

**Add to LinkedIn:**
```
🚨 Iran Currency Crisis Analysis Dashboard

Interactive financial analytics platform analyzing 14+ years of USD/IRR exchange rates.

🔗 Live Demo: https://your-app.streamlit.app
📊 Features: Crisis detection, risk metrics, geopolitical correlation
🛠️ Tech: Python, Streamlit, Plotly, PostgreSQL

#DataAnalytics #Python #Streamlit #FinancialAnalysis
```

### 3. Create Project Showcase

**Take Screenshots** for your portfolio:
1. Overview page
2. Time series chart
3. Crisis detection visualization
4. Risk metrics dashboard
5. News correlation page

**Create a Short Demo Video** (optional):
- Use Loom or screen recorder
- 2-3 minutes walkthrough
- Highlight key features
- Upload to YouTube/LinkedIn

### 4. Share with Network

```markdown
📊 Excited to share my latest data analytics project!

I built an interactive dashboard analyzing Iranian currency crisis patterns 
over 14 years, correlating volatility with geopolitical events.

✨ Features:
• Real-time crisis detection using statistical algorithms
• Risk metrics (VaR, CVaR, drawdown analysis)
• News correlation via GDELT API
• 6 interactive analysis pages

🛠️ Tech Stack: Python, Streamlit, Plotly, PostgreSQL, SQL

🔗 Live Demo: [your-url]
🐙 GitHub: https://github.com/sadaf-rad/Currency-Convertor

Open to feedback and opportunities in data analytics!

#DataAnalytics #Python #FinancialAnalysis #DataVisualization
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Module not found" error
```bash
# Solution: Verify all packages in requirements.txt
pip freeze | grep streamlit
pip install -r requirements.txt
```

**Issue**: "File not found" error for CSV
```bash
# Solution: Ensure CSV files are in the same directory as app.py
# Or update file paths in app.py to use absolute paths
```

**Issue**: App loads but shows no data
```bash
# Solution: Check file names and paths
# Verify CSV files are not in .gitignore
# Check Streamlit Cloud logs for errors
```

**Issue**: Slow loading on Streamlit Cloud
```bash
# Solution: Add @st.cache_data decorator to data loading functions
# Already implemented in app.py
```

### Getting Help

- **Streamlit Community**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **GitHub Issues**: [Create an issue](https://github.com/sadaf-rad/Currency-Convertor/issues)

---

## 🔄 Update Your Deployed App

### For Streamlit Cloud:
```bash
# Just push to GitHub
git add .
git commit -m "Update dashboard"
git push origin main

# Streamlit Cloud will auto-deploy
```

### For Heroku:
```bash
# Push to Heroku
git add .
git commit -m "Update dashboard"
git push heroku main
```

---

## 💰 Cost Comparison

| Platform | Free Tier | Limits | Best For |
|----------|-----------|--------|----------|
| **Streamlit Cloud** | ✅ Yes | 1 GB RAM, 1 app public | Quick demos |
| **Heroku** | ✅ Yes | 550-1000 dyno hours/month | Production apps |
| **AWS/GCP** | 🟡 Limited | Pay per use | Enterprise |

**Recommendation**: Start with **Streamlit Cloud** for portfolio projects!

---

## 📊 Analytics & Monitoring

### Add Google Analytics (Optional)

1. Get tracking ID from [analytics.google.com](https://analytics.google.com)

2. Add to `app.py`:
```python
import streamlit.components.v1 as components

# Google Analytics
components.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-GA-ID');
</script>
""", height=0)
```

---

## 🎉 Success!

Your dashboard is now live and accessible to recruiters worldwide!

**Next Steps:**
1. ✅ Add live link to resume
2. ✅ Share on LinkedIn
3. ✅ Add to portfolio website
4. ✅ Include in job applications

---

**Questions?** Open an issue on [GitHub](https://github.com/sadaf-rad/Currency-Convertor/issues)

**Good luck with your job search! 🚀**
