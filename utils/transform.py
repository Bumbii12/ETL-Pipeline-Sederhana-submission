import pandas as pd
from datetime import datetime

USD_TO_IDR = 16000  # Nilai tukar dolar ke rupiah

def clean_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    # Hapus nilai null dan duplikat
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    # Hapus baris yang memiliki judul tidak valid
    df = df[df['Title'].str.lower() != 'unknown product']

    # Bersihkan dan ubah kolom Price ke rupiah (float)
    df['Price'] = df['Price'].replace(r'[\$,]', '', regex=True)  # Hapus simbol dolar
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')  # Ubah nilai tidak valid menjadi NaN
    df['Price'] = df['Price'].fillna(0) * USD_TO_IDR  # Isi NaN dengan 0 dan konversi ke IDR

    # Bersihkan dan ubah kolom Rating ke float
    def parse_rating(rating):
        try:
            return float(rating)
        except:
            match = pd.to_numeric(rating.split('/')[0].strip(), errors='coerce')
            return match if pd.notnull(match) else None

    df['Rating'] = df['Rating'].apply(parse_rating)
    df = df[df['Rating'].notnull()]

    # Ambil angka dari kolom Colors
    df['Colors'] = df['Colors'].astype(str).str.extract(r'(\d+)')
    df = df[df['Colors'].notnull()]
    df['Colors'] = df['Colors'].astype(int)

    # Bersihkan kolom Size dan Gender sebagai string
    df['Size'] = df['Size'].astype(str).str.strip()
    df['Gender'] = df['Gender'].astype(str).str.strip()

    # Tambahkan kolom timestamp
    df['timestamp'] = datetime.now()

    # Ubah tipe data secara eksplisit
    df = df.astype({
        'Title': 'object',
        'Price': 'float64',
        'Rating': 'float64',
        'Colors': 'int64',
        'Size': 'object',
        'Gender': 'object'
    })

    return df
