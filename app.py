import streamlit as st
import pandas as pd

# 1. Judul Aplikasi
st.set_page_config(page_title="Jejak Duit - Broker Analyzer", layout="wide")
st.title("📊 Jejak Duit: Broker Analyzer")

# 2. Fungsi untuk Membaca Data
# @st.cache_data memastikan data tidak dibaca ulang setiap kali Anda klik menu, jadi lebih cepat.
@st.cache_data
def load_data():
    # Ganti 'nama_file_anda.parquet' dengan nama file asli Anda
    df = pd.read_parquet('broker_120d.parquet')
    
    # Memastikan kolom tanggal bertipe datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Mengubah semua nilai transaksi menjadi angka positif (absolut)
    df['net_value'] = df['net_value'].abs()
    
    return df

# 3. Memuat Data ke dalam Program
data = load_data()

# 4. Menampilkan Pesan Berhasil dan Tabel Data (Sampel 5 baris)
st.success("Data berhasil dimuat!")
st.write("Berikut adalah tampilan 5 data pertama Anda:")
st.dataframe(data.head())