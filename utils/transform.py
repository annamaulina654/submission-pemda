import pandas as pd
import numpy as np

def transform_data(data: list) -> pd.DataFrame:
    """
    Mengambil data mentah (list of dict), membersihkannya, 
    dan mengembalikannya sebagai DataFrame yang bersih.
    """
    try:
        # 1. Konversi ke DataFrame
        df = pd.DataFrame(data)

        # 2. Pembersihan Awal (Handle Null & Duplikat)
        # Sesuai kriteria "tidak boleh memiliki nilai yang duplikat" [cite: 72, 76]
        # dan "tidak boleh memiliki nilai null" [cite: 73, 77]
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)

        # 3. Filter Data Invalid (berdasarkan string)
        # Sesuai kriteria "dirty patterns" [cite: 84-88]
        df = df[df['Title'] != 'Unknown Product'].copy()
        df = df[df['Price'] != 'Price Unavailable']
        df = df[df['Rating'] != 'Not Rated']

        # 4. Transformasi Kolom
        
        # Price: Hapus '$', konversi ke float, kalikan 16000 
        df['Price'] = df['Price'].str.replace('$', '', regex=False).astype(float)
        df['Price'] = df['Price'] * 16000

        # Rating: Ekstrak angka float (misal '3.9') 
        # Regex (r'(\d+\.\d+)') akan mengekstrak pola "angka.angka"
        # str.extract akan menghasilkan NaN jika pola tidak ditemukan 
        # (seperti di "Invalid Rating"), yang kita inginkan.
        df['Rating'] = df['Rating'].str.extract(r'(\d+\.\d+)').astype(float)

        # Colors: Ekstrak angka (misal '3') 
        # Regex (r'(\d+)') akan mengekstrak pola "angka"
        df['Colors'] = df['Colors'].str.extract(r'(\d+)').astype(float) # Ekstrak sbg float dulu

        # Size: Hapus 'Size: ' [cite: 92]
        df['Size'] = df['Size'].str.replace('Size: ', '', regex=False)

        # Gender: Hapus 'Gender: ' [cite: 94]
        df['Gender'] = df['Gender'].str.replace('Gender: ', '', regex=False)

        # 5. Pembersihan Akhir (setelah transformasi)
        # Setelah 'Rating' diekstrak, 'Invalid Rating' akan menjadi NaN.
        # Kita dropna() lagi untuk menghapus baris-baris tersebut.
        df.dropna(inplace=True)

        # 6. Set Tipe Data Final
        # Memastikan tipe data sesuai ekspektasi 
        df = df.astype({
            'Price': 'float64',
            'Rating': 'float64',
            'Colors': 'int64', # Ubah ke int64 setelah NaN dibersihkan
            'Title': 'object',
            'Size': 'object',
            'Gender': 'object'
        })
        
        print("Transformasi data berhasil.")
        return df

    except Exception as e:
        # Error handling untuk kriteria 'Advanced' 
        print(f"Terjadi kesalahan saat transformasi data: {e}")
        return pd.DataFrame() # Kembalikan DataFrame kosong jika gagal

# Untuk testing modul secara independen
if __name__ == '__main__':
    # Contoh data kotor (mirip output extract.py)
    dummy_data = [
        {'Title': 'Unknown Product', 'Price': '$100.00', 'Rating': 'Rating: ⭐ Invalid Rating / 5', 'Colors': '5 Colors', 'Size': 'Size: M', 'Gender': 'Gender: Men', 'timestamp': '...'},
        {'Title': 'T-shirt 2', 'Price': '$102.15', 'Rating': 'Rating: ⭐ 3.9 / 5', 'Colors': '3 Colors', 'Size': 'Size: M', 'Gender': 'Gender: Women', 'timestamp': '...'},
        {'Title': 'Hoodie 3', 'Price': '$496.88', 'Rating': 'Rating: ⭐ 4.8 / 5', 'Colors': '3 Colors', 'Size': 'Size: L', 'Gender': 'Gender: Unisex', 'timestamp': '...'},
        {'Title': 'Pants 4', 'Price': '$467.31', 'Rating': 'Rating: ⭐ 3.3 / 5', 'Colors': '3 Colors', 'Size': 'Size: XL', 'Gender': 'Gender: Men', 'timestamp': '...'},
        {'Title': 'Jacket 5', 'Price': '$321.59', 'Rating': 'Rating: ⭐ Invalid Rating / 5', 'Colors': '3 Colors', 'Size': 'Size: XXL', 'Gender': 'Gender: Women', 'timestamp': '...'},
        {'Title': 'T-shirt 2', 'Price': '$102.15', 'Rating': 'Rating: ⭐ 3.9 / 5', 'Colors': '3 Colors', 'Size': 'Size: M', 'Gender': 'Gender: Women', 'timestamp': '...'}, # Duplikat
        {'Title': 'Missing Data', 'Price': '$50.00', 'Rating': 'Rating: ⭐ 4.0 / 5', 'Colors': None, 'Size': 'Size: S', 'Gender': 'Gender: Men', 'timestamp': '...'}, # Data Null
    ]
    
    print("Mulai transformasi (mode testing)...")
    cleaned_df = transform_data(dummy_data)
    
    if not cleaned_df.empty:
        print("\nData setelah dibersihkan:")
        print(cleaned_df.head())
        print("\nTipe Data:")
        print(cleaned_df.info())
    else:
        print("Transformasi gagal atau tidak menghasilkan data.")