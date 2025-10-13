# Courseworks

## Tugas 1
1. Mencari data di kaggle
2. Install
    - https://exploratory.io/
    - https://orangedatamining.com/download/
    - https://www.microsoft.com/en-us/power-platform/products/power-bi/downloads
3. Setup https://jupyterbook.org/en/stable/intro.html

## Tugas 2
1. Buat database Iris di MySQL dan PostgreSQL lalu ditarik pakai power BI
2. Data sudah dideskripsikan sesuai dengan tipe data
3. Data sudah dieksplorasi data
    - min max dari setiap kolom
    - rata rata dari setiap kolom
    - jumlah setiap kelas ditampilkan dalam grafik batang

## Tugas 3
1. Table iris dipecah dan dimasukkan ke dalam databse berbeda.
    - mysql: SepalLengthCm, SepalWidthCm
    - postgre: PetalLengthCm, PetalWidthCm
    - datanya ditarik menggunakan script
    - datanya digabung menggunakan power BI (Transform data)
2. Mengumpulkan data
    - mengetahui jumlah data dan kolom
    - mengecheck tipe data setiap kolom (Jenis Variabel)
    - mendeteksi apakah ada nilai yang tidak masuk akal dari variabel
    - menentukan sumber data - Sumber Web
3. Melihat 10 baris pertama data menggunakan script python head()
4. Install library pycaret (pip install pycaret)

## Tugas 4
1. Download dataset ecoli dari UCI https://archive.ics.uci.edu/dataset/39/ecoli
2. Simpan didatabase MySQL
3. Tampilkan data dalam scatter plot menggunakan PCA.
    - PCA mentransformasi data menjadi dimensi rendah (2)
4. Lakukan penyeimbangan data menggunakan ADASYN
5. Ploting data dari data yang diimbangkan menggunakan PCA, tandai data data hasil generatenya

## Tugas 5  
Klasifikasi menggunakan Naive Bayes
1. Data belum diseimbangkan
2. Data diseimbangkan menggunakan smote
3. Data diseimbangkan menggunakan adasyn

## PRA-UTS
1. Melakukan pengumpulan data postgresql
2. Melakukan analisa data untuk klasifikasi tool knime
3. Membangun script python untuk analisis data pada knime
    - Download [Knime](https://www.knime.com/downloads)
    - Download [driver postgresql](https://jdbc.postgresql.org/)
    - Install JDK minimum 9
    - Install Python conda / Miniforgem minimum 3.9

## UTS
Dataset penyakit tiroid dari repositori UCI Machine Learning adalah dataset i yang cocok untuk pelatihan klasifikas. Dataset ini memiliki 3.772 data objek data latih dan 3.428 data objek data uji. Terdapat 15 atribut kategorikal dan 6 atribut numerik (real). Permasalahannya adalah menentukan apakah seorang pasien yang dirujuk ke klinik menderita hipotiroid. Oleh karena itu, dibentuk tiga kelas: normal (tidak hipotiroid), hiperfungsi, dan fungsi subnormal. Untuk deteksi outlier, digunakan 3.772 instance pelatihan dengan hanya 6 atribut numerik. Kelas hiperfungsi dianggap sebagai kelas outlier, sedangkan kedua kelas lainnya dianggap sebagai inlier, karena hiperfungsi merupakan kelas minoritas. [Sumber data](https://archive.ics.uci.edu/dataset/102/thyroid+disease).

(Gunakan Knime)
1.	Silahkan dataset dipecah menjadi 2 bagian untuk fitur kategorical disimpan di postgresql untuk  dan untuk atribut numerik dan label  simpan di database mysql
2.	Gabungkan 2 dataset tersebut
3.	Lakukan preprocessing 
4.	Lakukan modelling klasifikasi ( gunakan 3 model klasifikasi )
5.	Evaluasi hasil dari 3 model ( tentukan mana yang terbaik)