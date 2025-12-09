import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import seaborn as sns
import ast

# --- IMPORT UTILS ---
try:
    # UPDATED: Menambahkan preprocess_text_complete agar fitur Uji Coba jalan
    from utils import predict_sentiment_ai, detect_aspects, preprocess_text_complete
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False
    st.error("Gawat! File utils.py tidak ditemukan atau ada error import. Pastikan file ada di folder yang sama.")

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Sistem Monitoring Wisata Madura",
    page_icon="📊",
    layout="wide"
)

# --- FUNGSI LOAD DATA (CEPAT) ---
@st.cache_data
def load_ready_data():
    try:
        # Kita baca file yang sudah diproses
        df = pd.read_csv('data_final_dashboard.csv')
        
        # Kembalikan format tanggal & list aspek
        if 'published_at_date' in df.columns:
            df['published_at_date'] = pd.to_datetime(df['published_at_date'])
        
        # Konversi string "['a','b']" kembali menjadi list Python
        df['aspects'] = df['aspects'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
        
        return df
    except FileNotFoundError:
        return pd.DataFrame()

# --- LOGIKA APLIKASI ---

df = load_ready_data()

if df.empty:
    st.warning("⚠️ File 'data_final_dashboard.csv' belum ada.")
    st.info("Sistem tidak dapat menampilkan Dashboard. Pastikan Anda telah menjalankan script pemrosesan data terlebih dahulu.")
    # Fallback opsional: Jika Anda ingin tetap jalan tanpa data CSV, comment baris di bawah ini
    st.stop()

# --- HEADER ---
st.title("📊 Dashboard Kualitas Wisata Madura")
st.markdown("Sistem pemantauan sentimen pengunjung berbasis Machine Learning.")

# --- KPI CARDS (DENGAN NETRAL) ---
col1, col2, col3, col4, col5 = st.columns(5)

total = len(df)
pos = len(df[df['sentiment'] == 'Positif'])
neu = len(df[df['sentiment'] == 'Netral'])
neg = len(df[df['sentiment'] == 'Negatif'])
neg_rate = (neg/total)*100 if total > 0 else 0

col1.metric("Total Ulasan", f"{total:,}")
col2.metric("Jumlah Lokasi", df['place_name'].nunique())
col3.metric("Positif", f"{pos:,}", delta="👍")
col4.metric("Netral", f"{neu:,}", delta="😐", delta_color="off")
col5.metric("Negatif", f"{neg:,} ({neg_rate:.1f}%)", delta="-👎", delta_color="inverse")

st.divider()

# --- TABS UTAMA ---
tab_map, tab_detail, tab_manual = st.tabs(["🗺️ Peta Sebaran", "🔍 Analisis Detail", "🧪 Uji Coba Model"])

# === TAB 1: PETA SEBARAN (HEATMAP BISA DI-FILTER) ===
with tab_map:
    # Bagi layar: Peta (Kiri/Tengah) dan Info/Statistik (Kanan)
    c_map, c_info = st.columns([3, 1.2])
    
    with c_info:
        st.subheader("🎛️ Kontrol & Statistik")
        
        # 1. PILIHAN HEATMAP
        jenis_heatmap = st.selectbox(
            "Tampilkan Heatmap:",
            [
                "Negatif", 
                "Positif", 
                "Netral", 
                "Semua"
            ]
        )
        
        st.markdown("---")
        
        # Hitung Statistik per Lokasi dulu biar bisa dipakai di Peta & Tabel
        loc_stats = df.groupby(['place_name', 'lat', 'lon']).apply(
            lambda x: pd.Series({
                'Positif': (x['sentiment'] == 'Positif').sum(),
                'Netral': (x['sentiment'] == 'Netral').sum(),
                'Negatif': (x['sentiment'] == 'Negatif').sum(),
                'Total': len(x)
            })
        ).reset_index()
        
        # Tambahkan kolom Persentase untuk Sorting
        loc_stats['Pos_Pct'] = (loc_stats['Positif'] / loc_stats['Total']) * 100
        loc_stats['Neg_Pct'] = (loc_stats['Negatif'] / loc_stats['Total']) * 100
        
        # Filter: Hanya tampilkan di tabel jika ulasan > 5 (biar tidak bias)
        valid_stats = loc_stats[loc_stats['Total'] > 5]

        # 2. TABEL TOP NEGATIF (KRITIS)
        st.write("🔴 **Top 5 Paling Banyak Komplain:**")
        top_neg = valid_stats.sort_values('Neg_Pct', ascending=False).head(5)
        st.dataframe(
            top_neg[['place_name', 'Neg_Pct']],
            hide_index=True,
            column_config={
                'place_name': 'Lokasi',
                'Neg_Pct': st.column_config.ProgressColumn('Negatif', format='%.1f%%', min_value=0, max_value=100)
            }
        )
        
        # 3. TABEL TOP POSITIF (TERBAIK)
        st.write("🟢 **Top 5 Paling Disukai:**")
        top_pos = valid_stats.sort_values('Pos_Pct', ascending=False).head(5)
        st.dataframe(
            top_pos[['place_name', 'Pos_Pct']],
            hide_index=True,
            column_config={
                'place_name': 'Lokasi',
                'Pos_Pct': st.column_config.ProgressColumn('Positif', format='%.1f%%', min_value=0, max_value=100)
            }
        )

    with c_map:
        # Inisialisasi Peta
        m = folium.Map(location=[-7.0, 113.2], zoom_start=9, tiles="CartoDB positron")
        
        # LOGIKA HEATMAP DINAMIS
        heat_df = pd.DataFrame()
        heat_gradient = {}
        
        if "Negatif" in jenis_heatmap:
            heat_df = df[df['sentiment'] == 'Negatif']
            heat_gradient = {0.4: 'blue', 1: 'red'} # Merah = Masalah
            
        elif "Positif" in jenis_heatmap:
            heat_df = df[df['sentiment'] == 'Positif']
            heat_gradient = {0.4: 'blue', 1: 'lime'} # Hijau = Bagus
            
        elif "Netral" in jenis_heatmap:
            heat_df = df[df['sentiment'] == 'Netral']
            heat_gradient = {0.4: 'blue', 1: 'gray'} # Abu = Biasa
            
        else: # Semua
            heat_df = df
            heat_gradient = {0.4: 'cyan', 0.6: 'lime', 1: 'red'} # Pelangi
            
        # Render Heatmap
        if not heat_df.empty:
            heat_data = heat_df[['lat', 'lon']].values.tolist()
            HeatMap(heat_data, radius=15, gradient=heat_gradient, blur=15).add_to(m)
        
        # LOGIKA MARKER (TOOLTIP LENGKAP)
        for _, row in loc_stats.iterrows():
            total = row['Total']
            if total == 0: continue
            
            pos, neu, neg = row['Positif'], row['Netral'], row['Negatif']
            pos_pct = (pos/total)*100
            neu_pct = (neu/total)*100
            neg_pct = (neg/total)*100
            
            # Warna Marker
            neg_ratio = neg / total
            if neg_ratio > 0.3: color = '#e74c3c' # Merah
            elif neg_ratio > 0.15: color = '#f39c12' # Oranye
            else: color = '#2ecc71' # Hijau
            
            # Tooltip HTML
            tooltip_html = f"""
            <div style="font-family: sans-serif; min-width: 180px;">
                <h4 style="margin:0; padding-bottom:5px; border-bottom:1px solid #ccc;">{row['place_name']}</h4>
                <div style="margin-top:5px; font-size:13px;">
                    <span style="color:green;"><b>● Positif:</b> {int(pos)} ({pos_pct:.1f}%)</span><br>
                    <span style="color:gray;"><b>● Netral:</b> {int(neu)} ({neu_pct:.1f}%)</span><br>
                    <span style="color:red;"><b>● Negatif:</b> {int(neg)} ({neg_pct:.1f}%)</span>
                </div>
                <hr style="margin:5px 0;">
                <div style="font-weight:bold; font-size:12px;">Total: {int(total)}</div>
            </div>
            """
            
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=6 + (total/100),
                color=color, fill=True, fill_color=color, fill_opacity=0.8,
                tooltip=tooltip_html
            ).add_to(m)
            
        st_folium(m, height=600, use_container_width=True)

# === TAB 2: ANALISIS DETAIL (UPDATE: ALL SENTIMENTS) ===
with tab_detail:
    lokasi = st.selectbox("Pilih Lokasi:", sorted(df['place_name'].unique()))
    df_loc = df[df['place_name'] == lokasi]
    
    # --- BARIS 1: SENTIMEN PIE & ASPEK STACKED ---
    c1, c2 = st.columns([1, 2])
    
    # 1. PIE CHART SENTIMEN
    with c1:
        st.subheader("Komposisi Sentimen")
        counts = df_loc['sentiment'].value_counts()
        color_map = {'Positif': '#2ecc71', 'Negatif': '#e74c3c', 'Netral': '#95a5a6'}
        colors = [color_map.get(x, '#000') for x in counts.index]
        
        if not counts.empty:
            fig1, ax1 = plt.subplots()
            ax1.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=colors, startangle=90)
            st.pyplot(fig1)

    # 2. STACKED BAR CHART (ASPEK VS SENTIMEN) - FITUR UTAMA BARU
    with c2:
        st.subheader("Analisis Topik per Sentimen")
        
        # Explode aspek agar bisa dihitung
        df_exploded = df_loc.explode('aspects')
        # Buang aspek 'umum' atau 'tidak-terdeteksi' agar grafik bersih
        df_exploded = df_exploded[~df_exploded['aspects'].isin(['umum', 'tidak-terdeteksi'])]
        
        if not df_exploded.empty:
            # Hitung frekuensi aspek per sentimen
            aspect_sentiment = df_exploded.groupby(['aspects', 'sentiment']).size().reset_index(name='count')
            
            # Plotting
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            sns.barplot(
                data=aspect_sentiment, 
                x='count', 
                y='aspects', 
                hue='sentiment', 
                palette=color_map, # Pakai warna konsisten (Hijau/Merah/Abu)
                ax=ax2
            )
            ax2.set_title(f"Apa yang dibicarakan di {lokasi}?")
            ax2.set_xlabel("Jumlah Mentions")
            ax2.set_ylabel("Aspek")
            st.pyplot(fig2)
        else:
            st.info("Belum ada aspek spesifik yang terdeteksi di lokasi ini.")

    # --- BARIS 2: TABEL DATA ---
    st.subheader("Data Ulasan Lengkap")
    
    # Filter Default: SEMUA (Positif, Netral, Negatif)
    pilihan_sentimen = st.multiselect(
        "Filter Sentimen:", 
        ['Positif', 'Netral', 'Negatif'], 
        default=['Positif', 'Netral', 'Negatif'] # Default terpilih semua
    )
    
    df_table = df_loc[df_loc['sentiment'].isin(pilihan_sentimen)]
    
    st.dataframe(
        df_table[['published_at_date', 'name', 'review_text', 'aspects', 'sentiment']].sort_values('published_at_date', ascending=False), 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "published_at_date": "Tanggal",
            "name": "Nama",
            "review_text": "Ulasan",
            "aspects": "Aspek",
            "sentiment": "Klasifikasi"
        }
    )

# === TAB 3: UJI COBA MODEL (PLAYGROUND) ===
with tab_manual:
    st.header("🧪 Uji Coba Prediksi Sentimen")
    st.write("Gunakan fitur ini untuk menguji model AI dengan kalimat ulasan baru secara manual.")

    if UTILS_AVAILABLE:
        with st.container(border=True):
            # Input User
            input_text = st.text_area(
                "Masukkan ulasan baru:", 
                height=100, 
                placeholder="Contoh: Pantainya indah banget, airnya jernih, tapi sayang parkirnya mahal..."
            )

            if st.button("🔍 Prediksi Sekarang", type="primary"):
                if input_text.strip():
                    # Panggil fungsi dari utils.py
                    sentiment_result = predict_sentiment_ai(input_text)
                    aspects_result = detect_aspects(input_text)
                    clean_text_result = preprocess_text_complete(input_text)

                    # Layout Hasil
                    col_res1, col_res2 = st.columns([1, 2])

                    with col_res1:
                        st.subheader("Prediksi Sentimen")
                        # Visualisasi warna berdasarkan hasil
                        if sentiment_result == "Positif":
                            st.success(f"### {sentiment_result} 😊")
                        elif sentiment_result == "Negatif":
                            st.error(f"### {sentiment_result} 😠")
                        else:
                            st.warning(f"### {sentiment_result} 😐")

                    with col_res2:
                        st.subheader("Aspek Terdeteksi")
                        if aspects_result:
                            # Menampilkan aspek sebagai tags
                            for aspect in aspects_result:
                                st.markdown(
                                    f'<span style="background-color:#e0e0e0; padding:5px 10px; border-radius:15px; margin-right:5px; color:black;">{aspect}</span>', 
                                    unsafe_allow_html=True
                                )
                        else:
                            st.info("Tidak ada aspek spesifik yang terdeteksi.")

                    # Tampilkan Preprocessing (Untuk Debugging/Analisa)
                    st.divider()
                    with st.expander("ℹ️ Lihat Hasil Preprocessing Text"):
                        st.markdown("**Original Text:**")
                        st.text(input_text)
                        st.markdown("**Cleaned Text (Masuk ke Model):**")
                        st.code(clean_text_result, language='text')
                        st.caption("Model memprediksi berdasarkan 'Cleaned Text' di atas.")
                else:
                    st.warning("⚠️ Mohon masukkan teks ulasan terlebih dahulu!")
    else:
        st.error("Fitur ini dimatikan karena `utils.py` tidak ditemukan.")