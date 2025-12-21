## Business Understanding

***Business Context***
- **Sektor:** Pariwisata
- **Lokasi:** Pulau Madura
- **Sumber Data:** [Ulasan Google Maps wisata pantai](https://github.com/omkarcloud/google-maps-scraper)
- **Periode Data:** Real-time ulasan pengunjung

### 1. Define the Problem
**Masalah Bisnis:**
Potensi pariwisata pantai di Pulau Madura belum tergali secara maksimal karena kurangnya pemahaman mendalam mengenai persepsi dan pengalaman wisatawan yang sesungguhnya. Hal ini menyebabkan kesulitan dalam menentukan strategi pengembangan yang efektif.

**Problem Statement:**
"Bagaimana kita dapat memahami sentimen wisatawan terhadap destinasi pantai di Madura secara komprehensif dan mengubah data ulasan digital menjadi wawasan yang dapat ditindaklanjuti?"

### 2. Set Objectives
**Tujuan Proyek Analisis Sentimen:**

**Primary Objectives:**
- Mengklasifikasikan sentimen ulasan wisata pantai Madura menjadi positif, negatif, dan netral
- Mengidentifikasi aspek-aspek kritikal yang mempengaruhi kepuasan wisatawan
- Membuat sistem yang menganalisis sentimen dan aspek dari satu komentar

**Secondary Objectives:**
- Memberikan rekomendasi spesifik untuk peningkatan kualitas destinasi
- Mengetahui dari ke-3 model mana yang lebih bagus untuk sentimen analisis

### 3. Identify Stakeholders
**Primary Stakeholders:**
- **Dinas Pariwisata Kabupaten** - Sebagai regulator dan pengembang kebijakan
- **Pengelola Destinasi Wisata** - Sebagai operator langsung
- **Wisatawan** - Sebagai end-user dan sumber data

**Secondary Stakeholders:**
- **Pelaku Usaha Lokal** - Hotel, restoran, tour guide
- **Masyarakat Lokal** - Penerima dampak ekonomi pariwisata
- **Investor Pariwisata** - Pihak yang berkepentingan dengan pengembangan

**Expectations Mapping:**
| Stakeholder | Expectations |
|-------------|--------------|
| Dinas Pariwisata | Data-driven insights untuk perencanaan strategis |
| Pengelola Destinasi | Umpan balik spesifik untuk improvement |
| Wisatawan | Pengalaman berwisata yang lebih baik |

### 4. Define Success Criteria
**Technical Success Metrics:**
- **Accuracy**: > 80% untuk klasifikasi sentimen
- **Precision & Recall**: > 75% untuk setiap kelas sentimen
- **F1-Score**: > 0.75 (macro average)
- **Aspect Coverage**: Minimal 4 dari 5 aspek teridentifikasi dengan baik

**Business Success Metrics:**
- **Actionable Insights**: Minimal 5 rekomendasi spesifik yang dapat diimplementasikan
- **Stakeholder Adoption**: Laporan diterima dan digunakan oleh Dinas Pariwisata
- **Time to Insight**: < 2 minggu dari data collection sampai insight delivery

**Project Success Indicators:**
- ✅ Model dapat mengklasifikasikan 3.455 ulasan dengan akurasi tinggi
- ✅ Identifikasi 5 aspek utama yang mempengaruhi kepuasan wisatawan
- ✅ Dashboard visualisasi yang mudah dipahami oleh non-technical stakeholders
- ✅ Dokumentasi proses yang dapat direplikasi untuk destinasi lain

### Project Scope
**In Scope:**
- Analisis sentimen ulasan teks dari 4 kabupaten di Madura
- 5 aspek analisis: Keamanan, Kebersihan, Keindahan, Fasilitas, Aksesibilitas
- 3 model machine learning: Logistic Regression, Naive Bayes, SVM
- Visualisasi hasil dalam format dashboard

**Out of Scope:**
- Analisis data real-time streaming
- Integrasi dengan sistem booking/pemesanan
- Analisis kompetitor destinasi luar Madura
- Implementasi sistem production grade

### Constraints & Limitations
**Technical Constraints:**
- Data terbatas pada ulasan Google Maps
- Bahasa Indonesia dengan variasi dialek lokal
- Data tidak seimbang (dominasi rating positif)

**Business Constraints:**
- Waktu proyek terbatas
- Sumber daya komputasi terbatas
- Akses terbatas ke data internal Dinas Pariwisata