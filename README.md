# 🚨 Iran Currency Crisis Analysis & Dashboard

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-FF4B4B)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success)](https://github.com/sadaf-rad/Currency-Convertor)

> **An interactive financial analytics dashboard analyzing 14+ years of USD/IRR exchange rate data, identifying currency crisis periods and their correlation with geopolitical events.**

🔗 **[Live Demo](your-streamlit-url-here)** | 📊 **[View Analysis](comprehensive_analysis.ipynb)** | 📧 **[Contact Me](mailto:your-email@example.com)**

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Demo & Screenshots](#-demo--screenshots)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [Data Analysis Methodology](#-data-analysis-methodology)
- [Key Findings](#-key-findings)
- [Business Applications](#-business-applications)
- [Deployment](#-deployment)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Overview

This project provides a comprehensive analysis of the **Iranian Rial (IRR) against the US Dollar (USD)** exchange rate over 14+ years (2011-2025), identifying crisis periods and their correlation with geopolitical events. The project demonstrates advanced data analytics, statistical modeling, and interactive visualization skills.

### **What Makes This Project Unique?**

✅ **Real-world financial data** - Not a toy dataset  
✅ **Geopolitical context** - Links currency movements to world events  
✅ **End-to-end pipeline** - ETL, SQL, Python, visualization, deployment  
✅ **Interactive dashboard** - Deployable online for recruiters to explore  
✅ **Business insights** - Actionable recommendations for risk management  

### **Skills Demonstrated**

- 📊 **Data Analysis**: Pandas, NumPy, statistical methods
- 💾 **Database Management**: PostgreSQL, SQLAlchemy, SQL queries
- 📈 **Data Visualization**: Plotly, Matplotlib, Seaborn
- 🔍 **API Integration**: GDELT news API
- 🚀 **Web Development**: Streamlit dashboard
- 📝 **Documentation**: Jupyter notebooks, README
- 🌐 **Deployment**: Cloud deployment (Streamlit Cloud)

---

## ✨ Key Features

### 📊 Interactive Dashboard
- **Multi-page layout** with 6 analysis sections
- **Real-time filtering** by date range
- **Interactive charts** with Plotly (zoom, pan, hover)
- **Responsive design** for desktop and mobile

### 📈 Comprehensive Analytics
1. **Overview Page**: High-level metrics and trends
2. **Time Series Analysis**: Price movements, moving averages, seasonal patterns
3. **Crisis Detection**: Statistical identification of extreme volatility periods
4. **News Impact**: Correlation with geopolitical events via GDELT API
5. **Risk Metrics**: VaR, CVaR, drawdown analysis
6. **Insights**: Business recommendations and findings

### 🔍 Advanced Statistical Analysis
- Daily returns and volatility calculations
- Rolling statistics (7-day, 30-day windows)
- Maximum drawdown tracking
- Value at Risk (VaR) at 95% and 99% confidence levels
- Conditional VaR (Expected Shortfall)
- Crisis detection algorithm

### 📰 Geopolitical Integration
- GDELT API integration for news headlines
- Correlation analysis between news events and currency crashes
- Timeline visualization of crisis days with news context

---

## 📸 Demo & Screenshots

### Dashboard Overview
![Dashboard Overview](screenshots/overview.png)

### Time Series Analysis
![Time Series](screenshots/timeseries.png)

### Crisis Detection
![Crisis Analysis](screenshots/crisis.png)

### Risk Metrics
![Risk Metrics](screenshots/risk.png)

> **Note**: After deploying, add actual screenshots to the `screenshots/` folder

---

## 🛠️ Technologies Used

### **Languages & Libraries**
- **Python 3.8+**: Core programming language
- **Pandas & NumPy**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **Matplotlib & Seaborn**: Statistical plots
- **Streamlit**: Web dashboard framework

### **Database & Storage**
- **PostgreSQL**: Relational database
- **SQLAlchemy**: ORM for database operations
- **CSV**: Data storage and export

### **APIs & External Data**
- **GDELT Project API**: Global news and events data
- **Requests**: HTTP library for API calls

### **Development Tools**
- **Jupyter Notebooks**: Analysis and documentation
- **Git & GitHub**: Version control
- **VS Code**: IDE

---

## 📁 Project Structure

```
Currency-Convertor/
│
├── app.py                              # Main Streamlit dashboard
├── comprehensive_analysis.ipynb        # Full analysis notebook
├── EDA.ipynb                          # Original exploratory analysis
│
├── data/
│   ├── Dollar_Rial_Price_Dataset.csv # Main dataset
│   ├── crisis_dates.csv              # Identified crisis days
│   ├── crisis_days_with_news_english.csv  # News headlines
│   └── analysis.sql                  # SQL queries
│
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Git ignore rules
├── .streamlit/
│   └── config.toml                   # Streamlit configuration
│
├── README.md                         # This file
├── DEPLOYMENT.md                     # Deployment guide
└── screenshots/                      # Dashboard screenshots
```

---

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- PostgreSQL 12+ (optional, for SQL analysis)
- Git

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/sadaf-rad/Currency-Convertor.git
cd Currency-Convertor
```

### **Step 2: Create Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: (Optional) Setup PostgreSQL**
```bash
# Install PostgreSQL if not already installed
# macOS
brew install postgresql

# Start PostgreSQL
brew services start postgresql

# Create database
createdb currency_risk

# Import data (update connection string in EDA.ipynb)
```

---

## 💻 Usage

### **Run the Interactive Dashboard**
```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

### **Run the Analysis Notebook**
```bash
jupyter notebook comprehensive_analysis.ipynb
```

### **Execute SQL Queries**
```bash
# Connect to PostgreSQL
psql currency_risk

# Run queries from analysis.sql
\i analysis.sql
```

---

## 📊 Data Analysis Methodology

### **1. Data Collection & Cleaning**
- **Source**: Historical USD/IRR exchange rates (2011-2025)
- **Records**: 3,666 trading days
- **Cleaning**: Date parsing, numeric conversion, outlier detection

### **2. Feature Engineering**
Created advanced financial metrics:
- **Returns**: Daily percentage changes
- **Volatility**: Intraday and rolling volatility
- **Drawdown**: Maximum decline from peak
- **Moving Averages**: 7-day and 30-day MA

### **3. Crisis Detection Algorithm**
A day is classified as "crisis" if:
- Daily return < -5% (extreme depreciation), **OR**
- Cumulative drawdown ≤ -20% (prolonged decline)

### **4. Statistical Analysis**
- Descriptive statistics (mean, std, skewness, kurtosis)
- Distribution analysis (normal vs. crisis days)
- Correlation analysis between features
- Risk metrics (VaR, CVaR)

### **5. External Data Integration**
- **GDELT API**: Fetched news headlines for crisis days
- **Correlation Study**: Analyzed geopolitical events impact

### **6. Visualization & Reporting**
- Interactive dashboard with 6 analysis pages
- Publication-quality Jupyter notebook
- Statistical tables and summary reports

---

## 🔍 Key Findings

### **Crisis Statistics**
- **372 crisis days** identified (10.2% of all trading days)
- **Average normal day return**: -0.03%
- **Average crisis day return**: -15.2%
- **Maximum drawdown**: -98.5% from peak

### **Volatility Analysis**
- Crisis days show **6x higher** intraday volatility
- Volatility clustering around geopolitical events
- 30-day volatility > 5% signals potential crisis

### **Geopolitical Correlation**
Strong correlation between currency crashes and:
- International sanctions (2012, 2018)
- US-Iran diplomatic tensions
- Regional conflicts and military actions
- Nuclear program developments

### **Time Patterns**
- **Highest crisis years**: 2012, 2018, 2020
- **Seasonal patterns**: Q4 shows higher volatility
- **Recent trend**: Increasing frequency post-2020

---

## 💼 Business Applications

### **For Financial Institutions**
- **Risk Management**: Capital allocation based on crisis probability
- **Hedging Strategies**: Optimize FX hedge timing
- **Stress Testing**: Model extreme scenarios
- **Portfolio Optimization**: Dynamic currency exposure adjustment

### **For Import/Export Businesses**
- **Currency Planning**: Forecast conversion needs
- **Pricing Strategy**: Adjust prices during volatile periods
- **Cash Flow Management**: Optimize transaction timing

### **For Policy Makers**
- **Economic Policy**: Understand sanction impacts
- **Central Bank Intervention**: Identify optimal intervention points
- **Capital Controls**: Evidence-based policy decisions

---

## 🌐 Deployment

### **Deploy to Streamlit Cloud (FREE)**

1. **Push to GitHub**
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy"

3. **Share Your Live Link**
   - Get your live URL: `https://your-app.streamlit.app`
   - Add to resume and LinkedIn

### **Alternative: Deploy to Heroku**
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed Heroku instructions.

---

## 🔮 Future Enhancements

### **Phase 1: Machine Learning**
- [ ] Build LSTM model for crisis prediction
- [ ] Implement Random Forest for feature importance
- [ ] Create early warning system with ML

### **Phase 2: Real-time Integration**
- [ ] Connect to live exchange rate APIs
- [ ] Real-time news feed integration
- [ ] Automated daily updates

### **Phase 3: Extended Analysis**
- [ ] Add more currencies (EUR/IRR, GBP/IRR)
- [ ] Include economic indicators (inflation, GDP)
- [ ] Sentiment analysis on news headlines
- [ ] Options market implied volatility

### **Phase 4: Advanced Features**
- [ ] User authentication
- [ ] Custom alert system
- [ ] Export reports (PDF, Excel)
- [ ] API for programmatic access

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

**Sadaf Esmaeili Rad**  
Data Analyst | Financial Risk Analytics

- 📧 Email: your-email@example.com
- 💼 LinkedIn: [linkedin.com/in/your-profile](https://linkedin.com/in/your-profile)
- 🐙 GitHub: [@sadaf-rad](https://github.com/sadaf-rad)
- 🌐 Portfolio: [your-portfolio.com](https://your-portfolio.com)

---

## 🙏 Acknowledgments

- **Data Source**: Historical exchange rate data
- **GDELT Project**: Global news and events database
- **Streamlit**: Amazing dashboard framework
- **Plotly**: Interactive visualization library

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/sadaf-rad/Currency-Convertor?style=social)
![GitHub forks](https://img.shields.io/github/forks/sadaf-rad/Currency-Convertor?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/sadaf-rad/Currency-Convertor?style=social)

---

<div align="center">

**⭐ If you found this project helpful, please star the repository! ⭐**

Made with ❤️ by [Sadaf Esmaeili Rad](https://github.com/sadaf-rad)

</div>
