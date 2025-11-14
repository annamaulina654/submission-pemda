from utils.extract import scrape_products
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql
import time

def main():

    print("Memulai pipeline ETL...")
    start_time = time.time()
    
    print("Memulai Tahap Extract...")
    raw_data = scrape_products()
    
    if not raw_data:
        print("Tahap Extract gagal. Tidak ada data yang diambil. Pipeline berhenti.")
        return
    print(f"Tahap Extract selesai. {len(raw_data)} data mentah diambil.")

    print("\nMemulai Tahap Transform...")
    cleaned_df = transform_data(raw_data)
    
    if cleaned_df.empty:
        print("Tahap Transform gagal. Tidak ada data yang bersih. Pipeline berhenti.")
        return
    print("Tahap Transform selesai. Data berhasil dibersihkan.")
    print(f"Total data bersih: {len(cleaned_df)}")
    print("\nInfo DataFrame Bersih:")
    print(cleaned_df.info()) 

    print("\nMemulai Tahap Load...")
    
    csv_filename = "products.csv" 
    load_to_csv(cleaned_df, csv_filename)
    
    try:
        credentials_file = "google-sheets-api.json" 
        
        SPREADSHEET_ID = "1CCsYdkD5IpSvtAhhDRM0haSyPeY27VPhxF8P9hNYThU" 
        
        if SPREADSHEET_ID == "<GANTI_DENGAN_ID_ANDA>":
            print("\nPeringatan: SPREADSHEET_ID belum diisi. Melewati penyimpanan ke Google Sheets.")
        else:
            load_to_google_sheets(cleaned_df, SPREADSHEET_ID, credentials_file)
            
    except Exception as e:
        print(f"Gagal menyimpan ke Google Sheets: {e}")
    try:
            db_url = 'postgresql+psycopg2://developer:supersecretpassword@localhost:5432/fashion_db' 
            
            table_name = "fashion_products"
            
            load_to_postgresql(cleaned_df, db_url, table_name)
            
    except Exception as e:
            print(f"Gagal menyimpan ke PostgreSQL: {e}")
    
    end_time = time.time()
    
    end_time = time.time()
    print("\nTahap Load selesai.")
    print(f"Pipeline ETL selesai dalam {end_time - start_time:.2f} detik.")

if __name__ == "__main__":
    main()