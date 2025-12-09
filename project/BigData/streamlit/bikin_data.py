import pandas as pd
import json
import os
from langdetect import detect, LangDetectException
from utils import predict_sentiment_ai, detect_aspects

print("🚀 Memulai proses Pre-computation...")

# ==========================================
# 1. LOAD DATA & FILTER BAHASA (LOGIKA NOTEBOOK)
# ==========================================

# Sesuaikan nama file jika ada di folder root
file_path = 'all-task-3-detailed-reviews.csv' 

if not os.path.exists(file_path):
    print(f"❌ Error: File {file_path} tidak ditemukan.")
    exit()

print(f"📂 Membaca file: '{file_path}'")
df_reviews = pd.read_csv(file_path)
print(f"   Total baris data mentah: {len(df_reviews)}")

# 1.1 Hapus Missing Value
df_reviews.dropna(subset=['review_text'], inplace=True)
print(f"   Total setelah hapus NaN: {len(df_reviews)}")

# 1.2 Filter Bahasa (PERSIS SEPERTI KODEMU)
print("🌍 Sedang mendeteksi bahasa (Ini agak lama, mohon bersabar)...")

def detect_lang(text):
    try:
        return detect(text)
    except LangDetectException:
        return 'error'

# Kita terapkan filter
df_reviews['bahasa'] = df_reviews['review_text'].astype(str).apply(detect_lang)

total_sebelum = len(df_reviews)
# Ambil hanya yang 'id' (Indonesia)
df_reviews = df_reviews[df_reviews['bahasa'] == 'id'].copy()

print(f"✅ Filter Selesai. Dari {total_sebelum} ulasan -> Tersisa {len(df_reviews)} ulasan (Bahasa Indonesia).")

# ==========================================
# 2. MERGE KOORDINAT
# ==========================================
print("🗺️ Menggabungkan data lokasi...")
df_places = pd.read_csv('all-task-3.csv')

def parse_coord(x):
    try:
        x = x.replace("'", '"')
        data = json.loads(x)
        return data.get('latitude'), data.get('longitude')
    except:
        return None, None

df_places[['lat', 'lon']] = df_places['coordinates'].apply(lambda x: pd.Series(parse_coord(x)))

# Gabungkan Data
df_final = pd.merge(df_reviews, df_places[['place_id', 'lat', 'lon']], on='place_id', how='left')
df_final = df_final.dropna(subset=['lat', 'lon'])

# ==========================================
# 3. PREDIKSI SENTIMEN (AI)
# ==========================================
print("🤖 Menjalankan AI (Stemming + Prediksi)...")

# Panggil fungsi dari utils.py
df_final['sentiment'] = df_final['review_text'].astype(str).apply(predict_sentiment_ai)
df_final['aspects'] = df_final['review_text'].astype(str).apply(detect_aspects)

# ==========================================
# 4. SIMPAN HASIL
# ==========================================
output_file = 'data_final_dashboard.csv'
df_final.to_csv(output_file, index=False)

print(f"\n🎉 SUKSES! File '{output_file}' berhasil dibuat.")
print(f"👉 Sekarang jalankan: streamlit run app.py")