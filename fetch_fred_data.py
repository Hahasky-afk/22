
import os
import pandas as pd
from fredapi import Fred
from datetime import datetime, timedelta
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

FRED_API_KEY = "96472d8ae6dea88245d1c85a29e4e2cd"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

INDICATORS = {
    "Fed Funds Rate": "FEDFUNDS", "2Y Treasury": "GS2", "5Y Treasury": "GS5", "10Y Treasury": "GS10",
    "30Y Treasury": "GS30", "SOFR": "SOFR", "IOER": "IORB", "EFFR": "EFFR", "ON RRP": "RRPONTSYD",
    "CPI YoY": "CPIAUCSL", "Core CPI": "CPILFESL", "PPI": "PPIACO", "Core PPI": "WPSFD49207",
    "PCE": "PCE", "Core PCE": "PCEPILFE", "Nonfarm Payrolls": "PAYEMS", "Unemployment Rate": "UNRATE",
    "Initial Jobless Claims": "ICSA", "JOLTS Job Openings": "JTSJOL", "Labor Force Participation": "CIVPART",
    "M1 Money Supply": "M1SL", "M2 Money Supply": "M2SL", "TGA Account": "WTREGEN", "Excess Reserves": "EXCSRESNS",
    "RRP Balance": "RRPONTSYD", "Federal Debt": "GFDEBTN", "Federal Deficit": "FYFSD",
    "Interest Payments": "A091RC1Q027SBEA", "Retail Sales": "RSAFS", "Personal Savings Rate": "PSAVERT",
    "Consumer Confidence": "UMCSENT", "Credit Card Debt": "CCLACBW027SBOG", "FHFA Home Price Index": "USSTHPI",
    "30Y Mortgage Rate": "MORTGAGE30US", "Housing Starts": "HOUST", "DXY Index": "DTWEXBGS",
    "ISM Manufacturing PMI": "NAPM", "Exports": "IEABC", "Imports": "IRABC", "Industrial Production": "INDPRO",
    "Trade Balance": "NETEXP"
}

def get_fred_data(api_key, series_id, start_date, end_date=None):
    try:
        fred = Fred(api_key=api_key)
        data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)
        df = pd.DataFrame(data, columns=[series_id])
        df.index.name = 'date'
        return df
    except Exception as e:
        logger.error(f"獲取FRED數據時出錯 (series_id: {series_id}): {str(e)}")
        return pd.DataFrame()

def main():
    logger.info("開始抓取宏觀數據")
    start_date = "2018-01-01"
    end_date = datetime.today().strftime('%Y-%m-%d')

    all_data = {}

    for name, code in INDICATORS.items():
        logger.info(f"抓取 {name} ({code})")
        df = get_fred_data(FRED_API_KEY, code, start_date, end_date)
        if not df.empty:
            df.to_csv(os.path.join(DATA_DIR, f"{code}.csv"))
            all_data[name] = df.iloc[-1, 0]
        time.sleep(0.4)

    latest_df = pd.DataFrame(all_data.items(), columns=["指標", "最新值"])
    latest_df.to_csv(os.path.join(DATA_DIR, "latest_macro_data.csv"), index=False)
    logger.info("數據抓取完成 ✅")

if __name__ == "__main__":
    main()
