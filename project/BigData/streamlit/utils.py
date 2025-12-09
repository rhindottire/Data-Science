import re
import os
import pickle
import pandas as pd
import nltk
from nltk.corpus import stopwords
from langdetect import detect, LangDetectException
from symspellpy import SymSpell, Verbosity
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# --- 1. SETUP LIBRARY PENDUKUNG ---

# A. Download NLTK Stopwords (Cek dulu biar gak download terus)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Mendownload NLTK Stopwords...")
    nltk.download('stopwords', quiet=True)

# B. Import Kamus Lokal
try:
    # Catatan: Hapus 'arc.' karena file kamus_slang.py ada di folder yang sama
    from kamus_slang import kamus_slang
    from aspek import aspects
except ImportError:
    kamus_slang = {}
    aspects = {}

# --- 2. LOAD MODEL AI ---
try:
    with open('tfidf_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    with open('logreg_sentiment_model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    vectorizer = None
    model = None

# --- 3. KONFIGURASI PREPROCESSING (PERSIS SEPERTI NOTEBOOK) ---

# A. Setup Stemmer (Sastrawi)
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# B. Setup Stopwords (CUSTOM LOGIC KAMU)
# Ambil list bawaan NLTK
list_stopwords = stopwords.words('indonesian')

# Kata penting yang TIDAK BOLEH dihapus (PENTING BUAT SENTIMEN)
kata_penting = {'tidak', 'kurang', 'jangan', 'bukan', 'tapi', 'sangat', 'jauh', 'baik', 'belum'}
list_stopwords = [stopword for stopword in list_stopwords if stopword not in kata_penting]

# Tambahan noise words (slang/sampah)
list_stopwords.extend([
    'aja', 'amp', 'biar', 'bikin', 'bilang', 'broo', 'coyy', 'cuy', 'd',
    'deh', 'dg', 'dgn', 'dri', 'eh', 'euy', 'gaes', 'ges', 'guys', 'hehe',
    'hehehe', 'hai', 'halo', 'jgn', 'karna', 'ke', 'kok', 'mah', 'n', 'nah',
    'nih', 'nya', 'pas', 'sdh', 'sih', 't', 'tau', 'tuh', 'utk', 'wkwk',
    'wkwkwk', 'ya', 'yah', 'yee', 'yuhuuuu'
])

# Ubah ke Set biar pencarian cepat
set_stopwords = set(list_stopwords)

# C. Setup SymSpell (Typo Correction)
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
corpus_path = 'kamus_corpus_pantai.txt'

if os.path.exists(corpus_path):
    sym_spell.load_dictionary(corpus_path, term_index=0, count_index=1)
    print("✅ SymSpell & Custom Stopwords Loaded.")
else:
    print("⚠️ WARNING: 'kamus_corpus_pantai.txt' tidak ditemukan. Koreksi typo OFF.")


# ==========================================================
# FUNGSI PIPELINE (5 TAHAP)
# ==========================================================

def basic_clean(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def correct_typos(text):
    if not os.path.exists(corpus_path): return text
    tokens = text.split()
    corrected_tokens = []
    for token in tokens:
        suggestions = sym_spell.lookup(token, Verbosity.TOP, max_edit_distance=2)
        if suggestions:
            corrected_tokens.append(suggestions[0].term)
        else:
            corrected_tokens.append(token)
    return ' '.join(corrected_tokens)

def normalize_slang(text):
    tokens = text.split()
    normalized_tokens = [kamus_slang.get(token, token) for token in tokens]
    return ' '.join(normalized_tokens)

def stem_text(text):
    return stemmer.stem(text)

def remove_stopwords(text):
    tokens = text.split()
    # Pakai set_stopwords yang sudah kita custom di atas
    stopped_tokens = [word for word in tokens if word not in set_stopwords]
    return ' '.join(stopped_tokens)

# --- FUNGSI WRAPPER UTAMA ---
def preprocess_text_complete(text):
    """Pipeline Cleaning Lengkap"""
    text = basic_clean(text)         # 1. Clean
    text = correct_typos(text)       # 2. Typo
    text = normalize_slang(text)     # 3. Slang
    text = stem_text(text)           # 4. Stemming
    text = remove_stopwords(text)    # 5. Stopword (Custom)
    return text

# ==========================================================
# FUNGSI UNTUK APLIKASI
# ==========================================================

def predict_sentiment_ai(text):
    if model is None or vectorizer is None:
        return "Error: Model Missing"
    
    clean_txt = preprocess_text_complete(text)
    
    if not clean_txt: return "Netral"

    text_vector = vectorizer.transform([clean_txt])
    prediction = model.predict(text_vector)[0]
    return prediction

def detect_aspects(text):
    # Untuk aspek, kita pakai teks bersih sebelum stemming (opsional) 
    # atau sesudah stemming. Agar konsisten, kita pakai hasil preprocessing lengkap.
    clean_txt = preprocess_text_complete(text)
    
    found_aspects = []
    for aspect_name, keywords in aspects.items():
        if any(k in clean_txt for k in keywords):
            found_aspects.append(aspect_name)
            
    return found_aspects if found_aspects else ['tidak termasuk dalam 5 aspek']