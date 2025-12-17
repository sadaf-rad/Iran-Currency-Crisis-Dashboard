"""
🚨 Iran Currency Crisis Dashboard
Interactive visualization of USD/IRR exchange rate crisis analysis
Author: Sadaf Esmaeili Rad
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Iran Currency Crisis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E86AB;
    }
    </style>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    """Load and preprocess exchange rate data"""
    df = pd.read_csv('Dollar_Rial_Price_Dataset.csv')
    
    # Rename columns
    df = df.rename(columns={
        "Open Price": "open_price",
        "Low Price": "low_price",
        "High Price": "high_price",
        "Close Price": "close_price",
        "Change Amount": "change_amount",
        "Change Percent": "change_percent",
        "Gregorian Date": "date_gregorian",
        "Persian Date": "date_persian"
    })
    
    # Convert date
    df["date_gregorian"] = pd.to_datetime(df["date_gregorian"], format="%Y/%m/%d", errors="coerce")
    
    # Clean numeric columns
    df["change_amount"] = pd.to_numeric(
        df["change_amount"].astype(str).str.replace(",", ""), 
        errors="coerce"
    )
    df["change_percent"] = pd.to_numeric(
        df["change_percent"].astype(str).str.replace("%","").str.replace(",","."),
        errors="coerce"
    ) / 100.0
    
    # Sort by date
    df = df.sort_values('date_gregorian').reset_index(drop=True)
    
    # Calculate risk metrics
    df["ret_close_close"] = df["close_price"].pct_change()
    df["vol_intraday"] = (df["high_price"] - df["low_price"]) / df["open_price"]
    df["running_peak"] = df["close_price"].cummax()
    df["drawdown"] = df["close_price"] / df["running_peak"] - 1.0
    df["vol_7d"] = df["ret_close_close"].rolling(window=7).std()
    df["vol_30d"] = df["ret_close_close"].rolling(window=30).std()
    df["ma_7d"] = df["close_price"].rolling(window=7).mean()
    df["ma_30d"] = df["close_price"].rolling(window=30).mean()
    
    # Crisis detection
    df["is_crisis"] = (
        (df["ret_close_close"] < -0.05) | 
        (df["drawdown"] <= -0.20)
    ).astype(int)
    
    # Time features
    df['year'] = df['date_gregorian'].dt.year
    df['month'] = df['date_gregorian'].dt.month
    df['quarter'] = df['date_gregorian'].dt.quarter
    df['month_name'] = df['date_gregorian'].dt.strftime('%B')
    
    return df

@st.cache_data
def load_news_data():
    """Load news data if available"""
    try:
        news_df = pd.read_csv('crisis_days_with_news_english.csv')
        news_df['date'] = pd.to_datetime(news_df['date'])
        return news_df
    except FileNotFoundError:
        return None

# Load data
df = load_data()
news_df = load_news_data()
crisis_days = df[df['is_crisis'] == 1]

# Sidebar
st.sidebar.markdown("## 📊 Dashboard Controls")
st.sidebar.markdown("---")

# Page selection
page = st.sidebar.selectbox(
    "Select Analysis",
    ["📈 Overview", "📉 Time Series Analysis", "🚨 Crisis Analysis", 
     "📰 News Impact", "📊 Risk Metrics", "💡 Insights"]
)

# Date filter
st.sidebar.markdown("### Date Range")
min_date = df['date_gregorian'].min().date()
max_date = df['date_gregorian'].max().date()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Filter data by date
if len(date_range) == 2:
    mask = (df['date_gregorian'].dt.date >= date_range[0]) & (df['date_gregorian'].dt.date <= date_range[1])
    df_filtered = df[mask]
    crisis_filtered = df_filtered[df_filtered['is_crisis'] == 1]
else:
    df_filtered = df
    crisis_filtered = crisis_days

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Data Points:** {len(df_filtered):,}")
st.sidebar.markdown(f"**Crisis Days:** {len(crisis_filtered):,}")
st.sidebar.markdown(f"**Date Range:** {(df_filtered['date_gregorian'].max() - df_filtered['date_gregorian'].min()).days} days")

# Main content based on page selection
if page == "📈 Overview":
    st.markdown('<p class="main-header">🚨 Iran Currency Crisis Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">USD/IRR Exchange Rate Analysis (2011-2025)</p>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Current Rate",
            f"{df_filtered['close_price'].iloc[-1]:,.0f}",
            f"{df_filtered['ret_close_close'].iloc[-1]:.2%}"
        )
    
    with col2:
        st.metric(
            "Total Crisis Days",
            f"{len(crisis_filtered):,}",
            f"{len(crisis_filtered)/len(df_filtered)*100:.1f}%"
        )
    
    with col3:
        st.metric(
            "Avg Daily Return",
            f"{df_filtered['ret_close_close'].mean():.3%}",
            "Normal Days"
        )
    
    with col4:
        st.metric(
            "30-Day Volatility",
            f"{df_filtered['vol_30d'].iloc[-1]:.3%}",
            "Current"
        )
    
    with col5:
        st.metric(
            "Max Drawdown",
            f"{df_filtered['drawdown'].min():.1%}",
            "All-Time"
        )
    
    st.markdown("---")
    
    # Main chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Exchange Rate Over Time")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_filtered['date_gregorian'],
            y=df_filtered['close_price'],
            mode='lines',
            name='Close Price',
            line=dict(color='#2E86AB', width=2),
            hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br><b>Price:</b> %{y:,.0f}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=crisis_filtered['date_gregorian'],
            y=crisis_filtered['close_price'],
            mode='markers',
            name='Crisis Days',
            marker=dict(color='#EE4B2B', size=5, opacity=0.7),
            hovertemplate='<b>Crisis Day</b><br><b>Date:</b> %{x|%Y-%m-%d}<br><b>Price:</b> %{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            height=500,
            hovermode='x unified',
            template='plotly_white',
            xaxis_title='Date',
            yaxis_title='Close Price (Rials per USD)',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Key Statistics")
        
        # Crisis by year
        yearly_crisis = df_filtered.groupby('year').agg({
            'is_crisis': ['sum', 'count']
        }).reset_index()
        yearly_crisis.columns = ['year', 'crisis_days', 'total_days']
        yearly_crisis['crisis_pct'] = (yearly_crisis['crisis_days'] / yearly_crisis['total_days'] * 100)
        
        # Top crisis years
        st.markdown("**🔝 Top Crisis Years:**")
        top_years = yearly_crisis.nlargest(5, 'crisis_days')
        for _, row in top_years.iterrows():
            st.markdown(f"- **{int(row['year'])}:** {int(row['crisis_days'])} days ({row['crisis_pct']:.1f}%)")
        
        st.markdown("---")
        
        # Worst days
        st.markdown("**📉 Worst Crisis Days:**")
        worst_days = crisis_filtered.nsmallest(5, 'ret_close_close')[['date_gregorian', 'ret_close_close']]
        for _, row in worst_days.iterrows():
            st.markdown(f"- **{row['date_gregorian'].date()}:** {row['ret_close_close']:.2%}")
    
    # Additional charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Crisis Distribution by Year")
        fig = px.bar(
            yearly_crisis,
            x='year',
            y='crisis_days',
            color='crisis_pct',
            color_continuous_scale='Reds',
            labels={'crisis_days': 'Number of Crisis Days', 'year': 'Year', 'crisis_pct': 'Crisis %'}
        )
        fig.update_layout(height=350, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Average Price by Year")
        yearly_avg = df_filtered.groupby('year')['close_price'].mean().reset_index()
        fig = px.line(
            yearly_avg,
            x='year',
            y='close_price',
            markers=True,
            labels={'close_price': 'Average Close Price', 'year': 'Year'}
        )
        fig.update_traces(line_color='#2E86AB', line_width=3)
        fig.update_layout(height=350, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)

elif page == "📉 Time Series Analysis":
    st.markdown('<p class="main-header">📉 Time Series Analysis</p>', unsafe_allow_html=True)
    
    # Moving averages
    st.markdown("### 📈 Price with Moving Averages")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_filtered['date_gregorian'],
        y=df_filtered['close_price'],
        mode='lines',
        name='Close Price',
        line=dict(color='#2E86AB', width=1),
        opacity=0.7
    ))
    
    fig.add_trace(go.Scatter(
        x=df_filtered['date_gregorian'],
        y=df_filtered['ma_7d'],
        mode='lines',
        name='7-Day MA',
        line=dict(color='#F28C28', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_filtered['date_gregorian'],
        y=df_filtered['ma_30d'],
        mode='lines',
        name='30-Day MA',
        line=dict(color='#EE4B2B', width=2)
    ))
    
    fig.update_layout(
        height=500,
        template='plotly_white',
        xaxis_title='Date',
        yaxis_title='Price (Rials per USD)',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Returns and Volatility
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Daily Returns Distribution")
        fig = px.histogram(
            df_filtered,
            x='ret_close_close',
            nbins=50,
            color='is_crisis',
            color_discrete_map={0: '#2E86AB', 1: '#EE4B2B'},
            labels={'ret_close_close': 'Daily Return', 'is_crisis': 'Crisis'},
            opacity=0.7,
            barmode='overlay'
        )
        fig.update_layout(height=400, template='plotly_white', showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Rolling Volatility")
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_filtered['date_gregorian'],
            y=df_filtered['vol_7d'],
            mode='lines',
            name='7-Day',
            line=dict(color='#A23E48', width=1.5)
        ))
        
        fig.add_trace(go.Scatter(
            x=df_filtered['date_gregorian'],
            y=df_filtered['vol_30d'],
            mode='lines',
            name='30-Day',
            line=dict(color='#6A0572', width=2)
        ))
        
        fig.update_layout(
            height=400,
            template='plotly_white',
            xaxis_title='Date',
            yaxis_title='Volatility (Std Dev)',
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Seasonal patterns
    st.markdown("### 📅 Seasonal Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_avg = df_filtered.groupby('month')['ret_close_close'].mean().reset_index()
        monthly_avg['month_name'] = pd.to_datetime(monthly_avg['month'], format='%m').dt.strftime('%B')
        
        fig = px.bar(
            monthly_avg,
            x='month_name',
            y='ret_close_close',
            color='ret_close_close',
            color_continuous_scale='RdYlGn_r',
            labels={'ret_close_close': 'Avg Return', 'month_name': 'Month'}
        )
        fig.update_layout(height=400, template='plotly_white', title='Average Returns by Month')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        quarterly_crisis = df_filtered.groupby('quarter')['is_crisis'].sum().reset_index()
        fig = px.pie(
            quarterly_crisis,
            values='is_crisis',
            names='quarter',
            title='Crisis Days by Quarter',
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

elif page == "🚨 Crisis Analysis":
    st.markdown('<p class="main-header">🚨 Crisis Analysis</p>', unsafe_allow_html=True)
    
    # Crisis metrics
    col1, col2, col3, col4 = st.columns(4)
    
    normal_returns = df_filtered[df_filtered['is_crisis'] == 0]['ret_close_close'].mean()
    crisis_returns = df_filtered[df_filtered['is_crisis'] == 1]['ret_close_close'].mean()
    
    with col1:
        st.metric("Crisis Days", f"{len(crisis_filtered):,}", f"{len(crisis_filtered)/len(df_filtered)*100:.1f}%")
    with col2:
        st.metric("Normal Day Return", f"{normal_returns:.3%}")
    with col3:
        st.metric("Crisis Day Return", f"{crisis_returns:.3%}")
    with col4:
        st.metric("Return Difference", f"{abs(crisis_returns - normal_returns):.3%}")
    
    st.markdown("---")
    
    # Drawdown chart
    st.markdown("### 📉 Maximum Drawdown Over Time")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_filtered['date_gregorian'],
        y=df_filtered['drawdown'] * 100,
        fill='tozeroy',
        name='Drawdown',
        line=dict(color='#6A0572', width=1),
        fillcolor='rgba(106, 5, 114, 0.3)'
    ))
    
    fig.add_hline(
        y=-20,
        line_dash="dash",
        line_color="red",
        annotation_text="Crisis Threshold (-20%)",
        annotation_position="right"
    )
    
    fig.update_layout(
        height=400,
        template='plotly_white',
        xaxis_title='Date',
        yaxis_title='Drawdown (%)',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Crisis comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Returns: Crisis vs Normal")
        
        comparison_data = pd.DataFrame({
            'Type': ['Normal Days', 'Crisis Days'],
            'Avg Return': [normal_returns * 100, crisis_returns * 100],
            'Avg Volatility': [
                df_filtered[df_filtered['is_crisis'] == 0]['vol_intraday'].mean() * 100,
                df_filtered[df_filtered['is_crisis'] == 1]['vol_intraday'].mean() * 100
            ]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Avg Return (%)',
            x=comparison_data['Type'],
            y=comparison_data['Avg Return'],
            marker_color=['#2E86AB', '#EE4B2B']
        ))
        
        fig.update_layout(height=400, template='plotly_white', yaxis_title='Average Return (%)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Intraday Volatility Comparison")
        
        fig = px.box(
            df_filtered,
            x='is_crisis',
            y='vol_intraday',
            color='is_crisis',
            color_discrete_map={0: '#2E86AB', 1: '#EE4B2B'},
            labels={'is_crisis': 'Day Type', 'vol_intraday': 'Intraday Volatility'}
        )
        fig.update_layout(height=400, template='plotly_white', showlegend=False)
        fig.update_xaxes(ticktext=['Normal Days', 'Crisis Days'], tickvals=[0, 1])
        st.plotly_chart(fig, use_container_width=True)
    
    # Crisis timeline
    st.markdown("### 📅 Crisis Timeline")
    
    yearly_crisis = df_filtered.groupby('year').agg({
        'is_crisis': ['sum', 'count']
    }).reset_index()
    yearly_crisis.columns = ['year', 'crisis_days', 'total_days']
    yearly_crisis['crisis_pct'] = (yearly_crisis['crisis_days'] / yearly_crisis['total_days'] * 100)
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Crisis Days by Year', 'Crisis Percentage by Year'),
        vertical_spacing=0.15
    )
    
    fig.add_trace(
        go.Bar(x=yearly_crisis['year'], y=yearly_crisis['crisis_days'], 
               marker_color='#EE4B2B', name='Crisis Days'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=yearly_crisis['year'], y=yearly_crisis['crisis_pct'],
                   mode='lines+markers', marker_color='#F28C28', name='Crisis %',
                   line=dict(width=3)),
        row=2, col=1
    )
    
    fig.update_xaxes(title_text="Year", row=2, col=1)
    fig.update_yaxes(title_text="Number of Days", row=1, col=1)
    fig.update_yaxes(title_text="Percentage (%)", row=2, col=1)
    
    fig.update_layout(height=600, showlegend=False, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

elif page == "📰 News Impact":
    st.markdown('<p class="main-header">📰 Geopolitical News Impact</p>', unsafe_allow_html=True)
    
    if news_df is not None:
        # Filter news by selected date range
        if len(date_range) == 2:
            news_filtered = news_df[
                (news_df['date'].dt.date >= date_range[0]) & 
                (news_df['date'].dt.date <= date_range[1])
            ]
        else:
            news_filtered = news_df
        
        # News metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Headlines", f"{len(news_filtered):,}")
        with col2:
            st.metric("Crisis Days with News", f"{news_filtered['date'].nunique():,}")
        with col3:
            st.metric("Unique Sources", f"{news_filtered['source'].nunique():,}")
        with col4:
            avg_per_day = len(news_filtered) / max(news_filtered['date'].nunique(), 1)
            st.metric("Avg Headlines/Day", f"{avg_per_day:.1f}")
        
        st.markdown("---")
        
        # News over time
        st.markdown("### 📊 News Volume on Crisis Days")
        
        news_by_date = news_filtered.groupby(news_filtered['date'].dt.date).size().reset_index()
        news_by_date.columns = ['date', 'count']
        
        fig = px.bar(
            news_by_date,
            x='date',
            y='count',
            labels={'count': 'Number of Headlines', 'date': 'Date'},
            color='count',
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=400, template='plotly_white', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Top sources
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📰 Top News Sources")
            top_sources = news_filtered['source'].value_counts().head(10).reset_index()
            top_sources.columns = ['source', 'count']
            
            fig = px.bar(
                top_sources,
                y='source',
                x='count',
                orientation='h',
                labels={'count': 'Number of Articles', 'source': 'Source'},
                color='count',
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=400, template='plotly_white', showlegend=False)
            fig.update_yaxes(autorange="reversed")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📅 News Timeline")
            news_monthly = news_filtered.groupby(news_filtered['date'].dt.to_period('M')).size().reset_index()
            news_monthly.columns = ['month', 'count']
            news_monthly['month'] = news_monthly['month'].dt.to_timestamp()
            
            fig = px.line(
                news_monthly,
                x='month',
                y='count',
                markers=True,
                labels={'count': 'Number of Headlines', 'month': 'Month'}
            )
            fig.update_traces(line_color='#EE4B2B', line_width=3)
            fig.update_layout(height=400, template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)
        
        # Sample headlines
        st.markdown("### 📄 Recent Headlines on Crisis Days")
        
        # Display selector
        selected_date = st.selectbox(
            "Select a date to see headlines:",
            options=sorted(news_filtered['date'].dt.date.unique(), reverse=True)
        )
        
        headlines_for_date = news_filtered[news_filtered['date'].dt.date == selected_date]
        
        if len(headlines_for_date) > 0:
            st.markdown(f"**{len(headlines_for_date)} headlines on {selected_date}:**")
            for idx, row in headlines_for_date.iterrows():
                with st.expander(f"📰 {row['title'][:100]}..."):
                    st.markdown(f"**Source:** {row['source']}")
                    st.markdown(f"**URL:** {row['url']}")
                    st.markdown(f"**Full Title:** {row['title']}")
        else:
            st.info("No headlines found for this date.")
    
    else:
        st.warning("📭 News data not available. Run the GDELT API integration to fetch news headlines.")
        st.info("The news analysis correlates geopolitical events with currency crisis days using the GDELT project API.")

elif page == "📊 Risk Metrics":
    st.markdown('<p class="main-header">📊 Risk Metrics</p>', unsafe_allow_html=True)
    
    # Calculate risk metrics
    returns = df_filtered['ret_close_close'].dropna()
    
    # Value at Risk (VaR)
    var_95 = returns.quantile(0.05)
    var_99 = returns.quantile(0.01)
    
    # Conditional VaR (CVaR/Expected Shortfall)
    cvar_95 = returns[returns <= var_95].mean()
    cvar_99 = returns[returns <= var_99].mean()
    
    # Sharpe-like ratio (simplified)
    avg_return = returns.mean()
    std_return = returns.std()
    risk_adjusted_return = avg_return / std_return if std_return != 0 else 0
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("VaR (95%)", f"{var_95:.3%}", help="Maximum expected loss with 95% confidence")
    with col2:
        st.metric("VaR (99%)", f"{var_99:.3%}", help="Maximum expected loss with 99% confidence")
    with col3:
        st.metric("CVaR (95%)", f"{cvar_95:.3%}", help="Average loss beyond VaR")
    with col4:
        st.metric("Risk-Adj Return", f"{risk_adjusted_return:.4f}", help="Return per unit of risk")
    
    st.markdown("---")
    
    # Risk metrics over time
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Rolling VaR (95%)")
        
        rolling_var = df_filtered['ret_close_close'].rolling(window=30).quantile(0.05)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_filtered['date_gregorian'],
            y=rolling_var * 100,
            mode='lines',
            name='30-Day VaR',
            line=dict(color='#A23E48', width=2),
            fill='tozeroy',
            fillcolor='rgba(162, 62, 72, 0.2)'
        ))
        
        fig.update_layout(
            height=400,
            template='plotly_white',
            xaxis_title='Date',
            yaxis_title='VaR (%)',
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Return Distribution with VaR")
        
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=returns * 100,
            nbinsx=50,
            name='Returns',
            marker_color='#2E86AB',
            opacity=0.7
        ))
        
        fig.add_vline(
            x=var_95 * 100,
            line_dash="dash",
            line_color="red",
            annotation_text=f"VaR 95%: {var_95:.2%}",
            annotation_position="top"
        )
        
        fig.add_vline(
            x=var_99 * 100,
            line_dash="dash",
            line_color="darkred",
            annotation_text=f"VaR 99%: {var_99:.2%}",
            annotation_position="bottom"
        )
        
        fig.update_layout(
            height=400,
            template='plotly_white',
            xaxis_title='Daily Return (%)',
            yaxis_title='Frequency'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Correlation analysis
    st.markdown("### 🔗 Feature Correlations")
    
    corr_features = ['ret_close_close', 'vol_intraday', 'drawdown', 'vol_7d', 'vol_30d']
    corr_matrix = df_filtered[corr_features].corr()
    
    fig = px.imshow(
        corr_matrix,
        text_auto='.2f',
        color_continuous_scale='RdBu_r',
        aspect='auto',
        labels={'color': 'Correlation'}
    )
    fig.update_layout(height=400, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk summary table
    st.markdown("### 📋 Comprehensive Risk Summary")
    
    risk_summary = pd.DataFrame({
        'Metric': [
            'Average Daily Return',
            'Return Volatility',
            'Sharpe-like Ratio',
            'Maximum Single-Day Loss',
            'Maximum Drawdown',
            'VaR 95%',
            'VaR 99%',
            'CVaR 95%',
            'CVaR 99%',
            'Skewness',
            'Kurtosis'
        ],
        'Value': [
            f"{avg_return:.4%}",
            f"{std_return:.4%}",
            f"{risk_adjusted_return:.4f}",
            f"{returns.min():.2%}",
            f"{df_filtered['drawdown'].min():.2%}",
            f"{var_95:.3%}",
            f"{var_99:.3%}",
            f"{cvar_95:.3%}",
            f"{cvar_99:.3%}",
            f"{returns.skew():.3f}",
            f"{returns.kurtosis():.3f}"
        ]
    })
    
    st.dataframe(risk_summary, use_container_width=True, hide_index=True)

elif page == "💡 Insights":
    st.markdown('<p class="main-header">💡 Key Insights & Findings</p>', unsafe_allow_html=True)
    
    # Calculate key statistics
    total_days = len(df_filtered)
    crisis_days_count = len(crisis_filtered)
    crisis_pct = crisis_days_count / total_days * 100
    
    normal_return = df_filtered[df_filtered['is_crisis'] == 0]['ret_close_close'].mean()
    crisis_return = df_filtered[df_filtered['is_crisis'] == 1]['ret_close_close'].mean()
    
    max_drawdown = df_filtered['drawdown'].min()
    max_drawdown_date = df_filtered.loc[df_filtered['drawdown'].idxmin(), 'date_gregorian'].date()
    
    worst_day = crisis_filtered.loc[crisis_filtered['ret_close_close'].idxmin()]
    
    # Executive Summary
    st.markdown("## 📋 Executive Summary")
    st.markdown(f"""
    This analysis examines **{total_days:,} trading days** of USD/IRR exchange rate data spanning 
    **{(df_filtered['date_gregorian'].max() - df_filtered['date_gregorian'].min()).days:,} days**. 
    Using statistical methods, we identified **{crisis_days_count:,} crisis days** ({crisis_pct:.1f}% of all trading days) 
    characterized by extreme volatility and significant currency depreciation.
    """)
    
    st.markdown("---")
    
    # Key Findings
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🔍 Key Findings")
        
        st.markdown("### 1. Crisis Frequency & Severity")
        st.markdown(f"""
        - **{crisis_days_count:,} crisis days** identified over the analysis period
        - Crisis days represent **{crisis_pct:.1f}%** of all trading days
        - Average return on **normal days**: {normal_return:.3%}
        - Average return on **crisis days**: {crisis_return:.2%}
        - **{abs(crisis_return/normal_return):.1f}x worse** performance on crisis days
        """)
        
        st.markdown("### 2. Maximum Risk Exposure")
        st.markdown(f"""
        - **Worst single-day loss**: {worst_day['ret_close_close']:.2%} on {worst_day['date_gregorian'].date()}
        - **Maximum drawdown**: {max_drawdown:.2%} (reached on {max_drawdown_date})
        - **Currency depreciation**: Over {(1 - (df_filtered['close_price'].iloc[0] / df_filtered['close_price'].iloc[-1])) * 100:.0f}% value loss
        """)
        
        st.markdown("### 3. Volatility Patterns")
        normal_vol = df_filtered[df_filtered['is_crisis'] == 0]['vol_intraday'].mean()
        crisis_vol = df_filtered[df_filtered['is_crisis'] == 1]['vol_intraday'].mean()
        
        st.markdown(f"""
        - Crisis days show **{crisis_vol/normal_vol:.1f}x higher** intraday volatility
        - Normal day volatility: {normal_vol:.3%}
        - Crisis day volatility: {crisis_vol:.3%}
        - Volatility clustering observed around major geopolitical events
        """)
    
    with col2:
        st.markdown("## 📊 Crisis Severity")
        
        # Crisis severity gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = crisis_pct,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Crisis Days %"},
            gauge = {
                'axis': {'range': [None, 30]},
                'bar': {'color': "#EE4B2B"},
                'steps': [
                    {'range': [0, 5], 'color': "#90EE90"},
                    {'range': [5, 10], 'color': "#FFD700"},
                    {'range': [10, 15], 'color': "#FFA500"},
                    {'range': [15, 30], 'color': "#FF6B6B"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 15
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📈 Trend Analysis")
        recent_crisis_pct = df_filtered[df_filtered['year'] >= 2020]['is_crisis'].sum() / len(df_filtered[df_filtered['year'] >= 2020]) * 100
        old_crisis_pct = df_filtered[df_filtered['year'] < 2020]['is_crisis'].sum() / len(df_filtered[df_filtered['year'] < 2020]) * 100
        
        trend = "increasing" if recent_crisis_pct > old_crisis_pct else "decreasing"
        st.metric(
            "Recent Trend (2020+)",
            f"{recent_crisis_pct:.1f}%",
            f"{recent_crisis_pct - old_crisis_pct:+.1f}pp vs pre-2020"
        )
    
    st.markdown("---")
    
    # Geopolitical Context
    st.markdown("## 🌍 Geopolitical Context")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Major Crisis Periods")
        st.markdown("""
        **2012 (Sanctions Era)**
        - International sanctions imposed
        - 71 crisis days identified
        - Currency depreciation > 50%
        
        **2018 (JCPOA Withdrawal)**
        - US withdrawal from nuclear deal
        - Renewed sanctions
        - Market panic and capital flight
        
        **2020-2022 (Pandemic & Political Tensions)**
        - COVID-19 economic impact
        - Regional conflicts
        - Escalating US-Iran tensions
        
        **2025 (Recent Period)**
        - Ongoing geopolitical uncertainty
        - News correlation shows strong link to international events
        """)
    
    with col2:
        st.markdown("### Correlation with World Events")
        if news_df is not None:
            st.markdown(f"""
            **News Analysis Results:**
            - {len(news_df):,} headlines collected for crisis days
            - {news_df['date'].nunique():,} unique crisis days with news coverage
            - {news_df['source'].nunique():,} different news sources
            
            **Common Themes:**
            - US-Iran relations
            - Sanctions and diplomacy
            - Regional conflicts
            - Economic policies
            - Nuclear program developments
            
            Strong correlation observed between:
            - Negative geopolitical news → Currency depreciation
            - Sanction announcements → Immediate market reaction
            - Diplomatic tensions → Increased volatility
            """)
        else:
            st.info("News data analysis available when GDELT API integration is run.")
    
    st.markdown("---")
    
    # Business Applications
    st.markdown("## 💼 Business Applications")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🏦 For Financial Institutions")
        st.markdown("""
        - **Risk Management**: Use crisis detection for capital allocation
        - **Hedging Strategies**: Time FX hedges based on volatility patterns
        - **Portfolio Optimization**: Adjust exposure during high-risk periods
        - **Stress Testing**: Model worst-case scenarios
        """)
    
    with col2:
        st.markdown("### 🏢 For Businesses")
        st.markdown("""
        - **Import/Export Planning**: Forecast currency needs
        - **Pricing Strategy**: Adjust pricing during volatile periods
        - **Cash Management**: Optimize currency conversion timing
        - **Budgeting**: Account for exchange rate risk
        """)
    
    with col3:
        st.markdown("### 📊 For Analysts & Researchers")
        st.markdown("""
        - **Economic Research**: Study sanction impacts
        - **Policy Analysis**: Evaluate intervention effectiveness
        - **Predictive Modeling**: Build crisis forecasting models
        - **Academic Studies**: Publish geopolitical finance research
        """)
    
    st.markdown("---")
    
    # Recommendations
    st.markdown("## 🎯 Recommendations & Next Steps")
    
    st.markdown("""
    ### For Risk Management:
    1. **Early Warning System**: Monitor 30-day volatility > 5% as crisis indicator
    2. **Diversification**: Maintain multi-currency reserves during crisis periods
    3. **Dynamic Hedging**: Increase hedge ratios when volatility exceeds thresholds
    4. **Scenario Planning**: Prepare for -20% single-day moves during geopolitical events
    
    ### For Future Analysis:
    1. **Machine Learning Models**: Build predictive models using historical patterns
    2. **Real-time Monitoring**: Integrate live news feeds and API data
    3. **Sentiment Analysis**: NLP analysis of news headlines for early signals
    4. **Comparative Studies**: Analyze other emerging market currencies
    5. **Regime Switching Models**: Identify transitions between normal/crisis states
    
    ### Data Enhancement Opportunities:
    1. Add economic indicators (inflation, GDP, interest rates)
    2. Include commodity prices (oil, gold)
    3. Track policy announcements and central bank actions
    4. Monitor social media sentiment
    5. Incorporate options market implied volatility
    """)
    
    st.markdown("---")
    
    # Technical Details
    with st.expander("🔧 Technical Methodology"):
        st.markdown("""
        ### Crisis Detection Algorithm
        A day is classified as a "crisis day" if either condition is met:
        
        1. **Return Threshold**: Daily return < -5%
           - Indicates extreme single-day depreciation
           - Captures sudden market shocks
        
        2. **Drawdown Threshold**: Cumulative drawdown ≤ -20%
           - Measures decline from historical peak
           - Identifies prolonged depreciation periods
        
        ### Risk Metrics Calculated
        - **Returns**: Daily percentage change in close price
        - **Volatility**: Rolling standard deviation (7-day, 30-day windows)
        - **Drawdown**: Percentage below running maximum
        - **VaR**: Value at Risk at 95% and 99% confidence levels
        - **CVaR**: Conditional VaR (Expected Shortfall)
        - **Intraday Volatility**: (High - Low) / Open
        
        ### Data Sources
        - **Exchange Rates**: Historical USD/IRR prices (2011-2025)
        - **News Data**: GDELT Project API for geopolitical events
        - **Database**: PostgreSQL for data storage and SQL analytics
        
        ### Technologies Used
        - **Python**: pandas, numpy for data processing
        - **Visualization**: Plotly for interactive charts
        - **Dashboard**: Streamlit for web deployment
        - **Database**: PostgreSQL + SQLAlchemy
        - **APIs**: GDELT Doc API for news collection
        """)
    
    st.markdown("---")
    st.markdown("### 📧 Contact & Links")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**GitHub Repository**")
        st.markdown("[View on GitHub](https://github.com/sadaf-rad/Currency-Convertor)")
    with col2:
        st.markdown("**Author**")
        st.markdown("Sadaf Esmaeili Rad")
    with col3:
        st.markdown("**Project Type**")
        st.markdown("Data Analytics Portfolio")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
    <p>📊 Iran Currency Crisis Dashboard | Built with Streamlit & Plotly</p>
    <p>Data Analysis Project by Sadaf Esmaeili Rad | © 2025</p>
    </div>
    """,
    unsafe_allow_html=True
)
