import pandas as pd
from sqlalchemy import create_engine
import os

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def load_to_csv(df: pd.DataFrame, filename: str):

    try:
        df.to_csv(filename, index=False) 
        print(f"Data berhasil disimpan ke {filename}")
    except PermissionError:
        print(f"Error: Gagal menyimpan ke {filename}. File mungkin sedang dibuka.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan ke CSV: {e}")

def load_to_google_sheets(df: pd.DataFrame, spreadsheet_id: str, credentials_path: str):

    try:
        if not os.path.exists(credentials_path):
            print(f"Error: File credentials '{credentials_path}' tidak ditemukan.")
            return

        SERVICE_ACCOUNT_FILE = credentials_path
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        
        credential = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        print("Otentikasi Google Sheets berhasil.")

        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()

        print("Menghapus data lama di 'Sheet1'...")
        sheet.values().clear(
            spreadsheetId=spreadsheet_id,
            range='Sheet1'
        ).execute()

        header = df.columns.tolist()
        values = df.values.tolist()
        data_to_write = [header] + values
        
        body = {
            'values': data_to_write
        }

        print(f"Menulis {len(data_to_write)} baris data baru ke 'Sheet1!A1'...")
        result = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range='Sheet1!A1', 
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"Data berhasil disimpan ke Google Sheets (ID: {spreadsheet_id})")

    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan ke Google Sheets: {e}")

def load_to_postgresql(df: pd.DataFrame, db_url: str, table_name: str):

    try:
        engine = create_engine(db_url)

        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        print(f"Data berhasil disimpan ke PostgreSQL, tabel: '{table_name}'")
    except ImportError:
        print("Error: Library 'sqlalchemy' atau 'psycopg2' belum terinstall.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan ke PostgreSQL: {e}")