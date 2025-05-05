import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine

class DataSaver:
    """Kelas untuk menangani penyimpanan data ke berbagai tempat."""

    def __init__(self, data):
        """Inisialisasi dengan data yang telah diproses."""
        self.data = data

    def save_to_csv(self, filename="products.csv"):
        """Simpan data ke CSV."""
        if self.data.empty:
            print("Dataframe kosong, tidak ada data yang disimpan.")
            return
        self.data.to_csv(filename, index=False)
        print(f"Data berhasil disimpan ke {filename}.")

    def save_to_google_sheets(self, spreadsheet_id, range_name):
        """Simpan data ke Google Sheets."""
        if self.data.empty:
            print("Dataframe kosong, tidak ada data yang disimpan ke Google Sheets.")
            return

        # Konversi kolom timestamp menjadi string
        if 'timestamp' in self.data.columns:
            self.data['timestamp'] = self.data['timestamp'].astype(str)

        creds = Credentials.from_service_account_file('endless-orb-458708-c9-1a3bd0022552.json')
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        values = self.data.values.tolist()
        body = {
            'values': values
        }

        try:
            sheet.values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            print(f"Data berhasil disimpan ke Google Sheets dengan ID {spreadsheet_id}.")
        except Exception as e:
            print(f"Gagal menyimpan ke Google Sheets: {e}")

    def save_all(self):
        """Menyimpan data ke CSV, dan Google Sheets."""
        try:
            self.save_to_csv()
        except Exception as e:
            print(f"Gagal menyimpan ke CSV: {e}")

        try:
            self.save_to_google_sheets(
                '1eNwOIu52kn1lO0t8ka9MvF8FKDhfBaU0OB8cidacd_Y',
                'Sheet1!A2'
            )
        except Exception as e:
            print(f"Gagal menyimpan ke Google Sheets: {e}")