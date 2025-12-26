import streamlit as st
import pandas as pd
import glob
import os
from datetime import datetime, timedelta
from broker_data import BROKER_CATEGORIES
from report_data import MARKETPLACE_REPORTS

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Jejak Duit - Broker Analyzer", layout="wide", page_icon="💸")

# 2. FUNGSI PEMBANTU (CSS & FORMATTING)
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def format_currency(num):
    if num >= 1_000_000_000_000: return f"Rp {num / 1_000_000_000_000:.2f} T"
    elif num >= 1_000_000_000: return f"Rp {num / 1_000_000_000:.2f} B"
    elif num >= 1_000_000: return f"Rp {num / 1_000_000:.2f} M"
    else: return f"Rp {num:,.0f}"

# 3. FUNGSI LOAD DATA
@st.cache_data
def load_data():
    files = glob.glob("*.parquet")
    if not files:
        st.error("❌ File .parquet tidak ditemukan!")
        st.stop()
    df = pd.read_parquet(files[0])
    df["date"] = pd.to_datetime(df["date"])
    df["net_value"] = df["net_value"].abs()
    df["net_lot"] = df["net_lot"].abs()
    return df

# --- EKSEKUSI DATA & TIMESTAMP (PENTING: Definisikan sebelum Layout) ---
local_css("style.css")
data = load_data()  # Mendefinisikan variabel 'data' agar tidak NameError

# Penanda waktu pembaruan aplikasi (WIT - UTC+9)
utc_mtime = datetime.fromtimestamp(os.path.getmtime(__file__))
wit_mtime = utc_mtime + timedelta(hours=9) 
app_last_update = wit_mtime.strftime('%d %b %Y, %H:%M')

# 4. LAYOUT UTAMA [3, 6, 3]
_, col_main, _ = st.columns([3, 6, 3])

with col_main:
    # --- HEADER ---
    st.markdown("<h1 style='text-align: center; font-size: 60px; margin-bottom: 0;'>💸</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-top: 0;'>Jejak Duit: Broker Analyzer</h2>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; margin-bottom: 15px;'><a href='https://trakteer.id/' target='_blank'><img src='https://cdn.trakteer.id/images/embed/trbtn-red-1.png' height='35' style='border:0px;height:35px;' alt='Trakteer'></a></div>", unsafe_allow_html=True)

    # --- DISCLAIMER ---
    with st.expander("⚠️ Disclaimer & Info Dashboard"):
        st.markdown("""
        * **DYOR:** Dashboard ini hanya alat bantu visualisasi statistik, bukan ajakan jual/beli saham tertentu.
        * **Broker Terkurasi:** Menganalisa 34 broker pilihan.
        > Gunakan dashboard ini sebagai referensi tambahan bagi analisa mandiri Anda.
        """)

    st.divider()

    # --- FILTER ANALISA ---
    st.markdown('<div class="filter-header">⚙️ Filter Analisa</div>', unsafe_allow_html=True)
    max_date = data["date"].max()
    
    c1, c2 = st.columns(2)
    with c1: start_date = st.date_input("Mulai", max_date)
    with c2: end_date = st.date_input("Akhir", max_date)

    c3, c4 = st.columns(2)
    with c3: s_brokers = st.multiselect("Broker", sorted(data["broker_code"].unique()), placeholder="Semua")
    with c4: s_stocks = st.multiselect("Saham", sorted(data["stock_code"].unique()), placeholder="Semua")

    c5, c6 = st.columns(2)
    with c5: s_inv = st.multiselect("Investor", sorted(data["investor_type"].unique()), placeholder="Semua")
    with c6: s_mkt = st.multiselect("Market", sorted(data["market_type"].unique()), placeholder="Semua")

    st.divider()

    # --- DASHBOARD SAHAM ---
    tab_beli, tab_jual = st.tabs(["🟢 TABEL BELI", "🔴 TABEL JUAL"])

    def render_analysis(side):
        mask = (data["date"] >= pd.Timestamp(start_date)) & (data["date"] <= pd.Timestamp(end_date)) & (data["side"] == side)
        if s_brokers: mask &= (data["broker_code"].isin(s_brokers))
        if s_stocks: mask &= (data["stock_code"].isin(s_stocks))
        if s_inv: mask &= (data["investor_type"].isin(s_inv))
        if s_mkt: mask &= (data["market_type"].isin(s_mkt))
        
        f_df = data.loc[mask]
        if f_df.empty:
            st.warning(f"Data {side} tidak ditemukan.")
            return

        # Metrik Dashboard
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">TOTAL {side}</div><div class="metric-value">{format_currency(f_df["net_value"].sum())}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">SAHAM DITRANSAKSI</div><div class="metric-value">{f_df["stock_code"].nunique()}</div></div>', unsafe_allow_html=True)

        st.download_button(label="📥 Unduh Data (.csv)", data=f_df.to_csv(index=False).encode('utf-8'), file_name=f'jejak_duit_{side.lower()}.csv', mime='text/csv', use_container_width=True)
        
        top_15 = f_df.groupby("stock_code")["net_value"].sum().sort_values(ascending=False).head(15)
        with st.expander(f"📈 Grafik Top 15 {side}"):
            st.bar_chart(top_15, color="#007bff")

        # Judul Daftar
        p_str = f"{start_date.strftime('%d/%m/%y')} - {end_date.strftime('%d/%m/%y')}"
        st.markdown(f"""
            <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 20px; margin-bottom: 10px;'>
                <h3 style='margin: 0;'>📋 Daftar Akumulasi/Distribusi {side}</h3>
                <span style='background-color: #374151; color: #9ca3af; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;'>
                    📅 {p_str}
                </span>
            </div>
        """, unsafe_allow_html=True)

        for stock, val in top_15.items():
            full_s = data[(data["stock_code"] == stock) & (data["date"] >= pd.Timestamp(start_date)) & (data["date"] <= pd.Timestamp(end_date)) & (data["side"] == side)]
            g_vwap = full_s["net_value"].sum() / (full_s["net_lot"].sum() * 100) if full_s["net_lot"].sum() > 0 else 0
            header = f"**{stock}** &nbsp; • &nbsp; **Value:** {format_currency(val)} &nbsp; • &nbsp; **VWAP:** {g_vwap:,.2f}"
            with st.expander(header):
                b_df = f_df[f_df["stock_code"] == stock].copy()
                b_agg = b_df.groupby("broker_code").agg({"net_value":"sum", "net_lot":"sum"}).sort_values("net_value", ascending=False).head(5)
                b_agg["Mkt Share (%)"] = (b_agg["net_value"] / full_s["net_value"].sum()) * 100
                b_agg["Avg Price"] = b_agg["net_value"] / (b_agg["net_lot"] * 100)
                st.table(b_agg[["net_value", "Mkt Share (%)", "Avg Price"]].style.format({"net_value":"{:,.0f}", "Mkt Share (%)":"{:.2f}%", "Avg Price":"{:,.2f}"}))

    with tab_beli: render_analysis("BUY")
    with tab_jual: render_analysis("SELL")

    st.divider()
    
    # --- FOOTER LAPORAN & KLASIFIKASI ---
    with st.expander("📚 Laporan Hasil Analisa Periodik (PDF)"):
        st.write("Rangkuman analisa mingguan dan bulanan:")
        for report in MARKETPLACE_REPORTS[:3]:
            st.markdown(f"- [{report['title']}]({report['url']})")

    with st.expander("🔍 Klasifikasi 34 Broker Terpilih"):
        r1_c1, r1_c2 = st.columns(2)
        r2_c1, r2_c2 = st.columns(2)
        cols = [r1_c1, r1_c2, r2_c1, r2_c2]
        for idx, col in enumerate(cols):
            with col:
                item = BROKER_CATEGORIES[idx]
                st.markdown(f"""<div class="broker-info-card">
                    <p style="font-weight: bold; margin-bottom: 5px; color: #007bff;">{item['name']}</p>
                    <p style="font-size: 0.85rem; color: #8b949e;">{item['desc']}</p>
                    <p style="font-size: 0.9rem;"><b>Codes:</b> {', '.join(item['codes'])}</p>
                </div>""", unsafe_allow_html=True)

    # --- FINAL CENTERED FOOTER (WIT - 24H) ---
    st.divider()
    st.markdown(f"""
        <div style='text-align: center; color: #4b5563; font-size: 0.85rem; padding-bottom: 30px;'>
            <p style='font-style: italic; margin-bottom: 5px;'>
                Aplikasi diracik dengan bantuan kafein, LLM, 
                dan rasa penasaran terhadap pergerakan bursa. ☕ 🤖 🤖 📈
            </p>
            <p><b>App Last Update:</b> {app_last_update}</p>
        </div>
    """, unsafe_allow_html=True)