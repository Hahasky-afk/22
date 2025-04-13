
import os
import pandas as pd

RAW_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_PATH = os.path.join(RAW_DIR, "dashboard_dataset.csv")

def load_and_clean_data():
    dfs = []
    for file in os.listdir(RAW_DIR):
        if file.endswith(".csv") and file not in ("latest_macro_data.csv", "dashboard_dataset.csv"):
            full_path = os.path.join(RAW_DIR, file)
            try:
                df = pd.read_csv(full_path, parse_dates=["date"], index_col="date")
                df = df.rename(columns={df.columns[0]: file.replace(".csv", "")})
                dfs.append(df)
            except Exception as e:
                print(f"Error processing {file}: {str(e)}")

    if not dfs:
        print("❌ 沒有可合併的文件。請確認抓數成功。")
        return

    merged = pd.concat(dfs, axis=1)
    merged = merged.sort_index().fillna(method="ffill").fillna(method="bfill")
    merged.to_csv(OUTPUT_PATH)
    print(f"✅ 數據已保存至 {OUTPUT_PATH}")

if __name__ == "__main__":
    load_and_clean_data()
