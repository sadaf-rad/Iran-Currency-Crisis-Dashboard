"""
Auto-Update Script for Currency Crisis Dashboard
Fetches latest exchange rate data and news headlines automatically
Run this script daily/weekly to keep your dashboard current
"""

import pandas as pd
import requests
from datetime import datetime, timedelta
import os
from pathlib import Path

# Configuration
DATA_DIR = Path(__file__).parent
EXCHANGE_RATE_FILE = DATA_DIR / 'Dollar_Rial_Price_Dataset.csv'
NEWS_FILE = DATA_DIR / 'crisis_days_with_news_english.csv'

def fetch_latest_exchange_rates():
    """
    Fetch latest USD/IRR exchange rates
    Note: You'll need to find a suitable API or data source
    This is a placeholder that shows the structure
    """
    print("📊 Fetching latest exchange rates...")
    
    # Option 1: Manual update - Download from your data source
    # For production, you would integrate with:
    # - Central Bank APIs
    # - Financial data providers (Alpha Vantage, etc.)
    # - Web scraping from official sources
    
    try:
        # Load existing data
        df_existing = pd.read_csv(EXCHANGE_RATE_FILE)
        
        # Get last date in dataset
        df_existing['Gregorian Date'] = pd.to_datetime(df_existing['Gregorian Date'], format='%Y/%m/%d')
        last_date = df_existing['Gregorian Date'].max()
        
        print(f"   Last date in dataset: {last_date.date()}")
        print(f"   Today: {datetime.now().date()}")
        
        days_behind = (datetime.now() - last_date).days
        
        if days_behind > 0:
            print(f"   ⚠️  Dataset is {days_behind} days behind")
            print(f"   📝 Manual action required: Update {EXCHANGE_RATE_FILE} with latest data")
            return False
        else:
            print(f"   ✅ Dataset is up to date!")
            return True
            
    except Exception as e:
        print(f"   ❌ Error checking exchange rates: {e}")
        return False


def fetch_latest_news():
    """
    Fetch latest news headlines for recent crisis days using GDELT API
    """
    print("\n📰 Fetching latest news headlines...")
    
    try:
        # Load existing data
        df = pd.read_csv(EXCHANGE_RATE_FILE)
        df['Gregorian Date'] = pd.to_datetime(df['Gregorian Date'], format='%Y/%m/%d', errors='coerce')
        
        # Calculate risk metrics for recent data
        df = df.sort_values('Gregorian Date').reset_index(drop=True)
        df['Close Price'] = pd.to_numeric(df['Close Price'], errors='coerce')
        df['ret_close_close'] = df['Close Price'].pct_change()
        df['running_peak'] = df['Close Price'].cummax()
        df['drawdown'] = df['Close Price'] / df['running_peak'] - 1.0
        df['is_crisis'] = ((df['ret_close_close'] < -0.05) | (df['drawdown'] <= -0.20)).astype(int)
        
        # Get crisis days from last 30 days
        recent_date = datetime.now() - timedelta(days=30)
        recent_crisis = df[(df['Gregorian Date'] >= recent_date) & (df['is_crisis'] == 1)]
        
        if len(recent_crisis) == 0:
            print("   ℹ️  No crisis days in the last 30 days")
            return True
        
        print(f"   Found {len(recent_crisis)} crisis days in last 30 days")
        
        # Load existing news
        try:
            existing_news = pd.read_csv(NEWS_FILE)
            existing_news['date'] = pd.to_datetime(existing_news['date'])
        except FileNotFoundError:
            existing_news = pd.DataFrame(columns=['date', 'title', 'url', 'source'])
        
        # Fetch news for each crisis day
        new_headlines = []
        
        for idx, row in recent_crisis.iterrows():
            crisis_date = row['Gregorian Date']
            
            # Check if we already have news for this date
            if len(existing_news[existing_news['date'].dt.date == crisis_date.date()]) > 0:
                continue
            
            print(f"   Fetching news for {crisis_date.date()}...")
            
            # GDELT API query
            date_str = crisis_date.strftime("%Y%m%d")
            url = "https://api.gdeltproject.org/api/v2/doc/doc"
            params = {
                "query": "Iran currency exchange rate dollar sanctions",
                "mode": "ArtList",
                "format": "json",
                "maxrecords": 10,
                "sort": "DateDesc",
                "startdatetime": f"{date_str}000000",
                "enddatetime": f"{date_str}235959",
            }
            
            try:
                resp = requests.get(url, params=params, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    if "articles" in data:
                        for art in data["articles"]:
                            title = art.get("title", "")
                            # Filter English headlines
                            if any(c.isascii() and c.isalpha() for c in title):
                                new_headlines.append({
                                    "date": str(crisis_date),
                                    "title": title,
                                    "url": art.get("url"),
                                    "source": art.get("domain")
                                })
            except Exception as e:
                print(f"   ⚠️  Error fetching news for {crisis_date.date()}: {e}")
        
        # Append new headlines to existing data
        if new_headlines:
            new_news_df = pd.DataFrame(new_headlines)
            updated_news = pd.concat([existing_news, new_news_df], ignore_index=True)
            updated_news = updated_news.drop_duplicates(subset=['date', 'title'])
            updated_news.to_csv(NEWS_FILE, index=False)
            print(f"   ✅ Added {len(new_headlines)} new headlines")
        else:
            print(f"   ℹ️  No new headlines to add")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error fetching news: {e}")
        return False


def calculate_and_update_crisis_dates():
    """
    Recalculate crisis dates based on latest data
    """
    print("\n🚨 Updating crisis detection...")
    
    try:
        df = pd.read_csv(EXCHANGE_RATE_FILE)
        
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
        
        # Calculate metrics
        df = df.sort_values('date_gregorian').reset_index(drop=True)
        df["ret_close_close"] = df["close_price"].pct_change()
        df["running_peak"] = df["close_price"].cummax()
        df["drawdown"] = df["close_price"] / df["running_peak"] - 1.0
        df["vol_intraday"] = (df["high_price"] - df["low_price"]) / df["open_price"]
        
        # Crisis detection
        df["is_crisis"] = (
            (df["ret_close_close"] < -0.05) | 
            (df["drawdown"] <= -0.20)
        ).astype(int)
        
        # Save crisis dates
        crisis_df = df[df["is_crisis"] == 1][['date_gregorian', 'close_price', 'ret_close_close', 
                                               'drawdown', 'vol_intraday', 'is_crisis']]
        crisis_df.to_csv(DATA_DIR / 'crisis_dates.csv', index=False)
        
        print(f"   ✅ Updated crisis dates file")
        print(f"   Total crisis days: {len(crisis_df)}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error updating crisis dates: {e}")
        return False


def generate_update_report():
    """
    Generate a summary report of the update
    """
    print("\n" + "="*60)
    print("📊 UPDATE SUMMARY REPORT")
    print("="*60)
    
    try:
        # Exchange rate data stats
        df = pd.read_csv(EXCHANGE_RATE_FILE)
        df['Gregorian Date'] = pd.to_datetime(df['Gregorian Date'], format='%Y/%m/%d')
        
        print(f"\n📈 Exchange Rate Data:")
        print(f"   Total records: {len(df):,}")
        print(f"   Date range: {df['Gregorian Date'].min().date()} to {df['Gregorian Date'].max().date()}")
        print(f"   Days of data: {(df['Gregorian Date'].max() - df['Gregorian Date'].min()).days}")
        
        # Crisis data stats
        crisis_df = pd.read_csv(DATA_DIR / 'crisis_dates.csv')
        print(f"\n🚨 Crisis Detection:")
        print(f"   Total crisis days: {len(crisis_df):,}")
        print(f"   Crisis percentage: {len(crisis_df)/len(df)*100:.1f}%")
        
        # News data stats
        try:
            news_df = pd.read_csv(NEWS_FILE)
            news_df['date'] = pd.to_datetime(news_df['date'])
            print(f"\n📰 News Headlines:")
            print(f"   Total headlines: {len(news_df):,}")
            print(f"   Unique crisis days with news: {news_df['date'].nunique()}")
            print(f"   Date range: {news_df['date'].min().date()} to {news_df['date'].max().date()}")
        except FileNotFoundError:
            print(f"\n📰 News Headlines: No data available")
        
        print(f"\n⏰ Update completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
    except Exception as e:
        print(f"   ⚠️  Error generating report: {e}")


def main():
    """
    Main update function
    """
    print("="*60)
    print("🔄 CURRENCY CRISIS DASHBOARD - AUTO UPDATE")
    print("="*60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Step 1: Check exchange rates
    rates_updated = fetch_latest_exchange_rates()
    
    # Step 2: Recalculate crisis dates
    crisis_updated = calculate_and_update_crisis_dates()
    
    # Step 3: Fetch latest news
    news_updated = fetch_latest_news()
    
    # Step 4: Generate report
    generate_update_report()
    
    if rates_updated and crisis_updated and news_updated:
        print("\n✅ All updates completed successfully!")
        print("\n💡 Your dashboard will now show the latest data.")
        print("   Restart Streamlit to see the updates.")
    else:
        print("\n⚠️  Some updates had issues. Check the logs above.")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
