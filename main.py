import pandas as pd
from utils.extract import scrape_fashion
from utils.transform import clean_and_transform
from utils.load import DataSaver

def main():
    # URL dasar
    BASE_URL = 'https://fashion-studio.dicoding.dev/'

    # 1. Extract
    print("🔍 Mengambil data dari website...")
    raw_data = scrape_fashion(BASE_URL)
    if not raw_data:
        print("❌ Tidak ada data yang berhasil diambil.")
        return

    df_raw = pd.DataFrame(raw_data)
    print(f"✅ {len(df_raw)} baris data berhasil diambil.")

    # 2. Transform
    print("🧹 Membersihkan dan mentransformasi data...")
    df_clean = clean_and_transform(df_raw)
    print(f"✅ {len(df_clean)} baris data setelah dibersihkan.")

    # 3. Load
    print("💾 Menyimpan data ke CSV dan Google Sheets...")
    saver = DataSaver(df_clean)
    saver.save_all()

    print("🎉 Proses ETL selesai!")

if __name__ == '__main__':
    main()