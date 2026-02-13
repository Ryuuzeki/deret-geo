# 🕺 AI Full Body Video Generator (MimicMotion)

Repositori ini berisi cetak biru (blueprint) dan skrip untuk membangun **AI Full Body Video Generator** Anda sendiri menggunakan Google Colab, berdasarkan model **MimicMotion**.

## 🚀 Fitur Utama
* **Pose Transfer:** Mengikuti gerakan tarian, jalan, atau lari dari video sumber dengan akurasi tinggi.
* **Temporal Consistency:** Menjaga agar baju atau wajah tidak berubah-ubah (flicker) selama video.
* **Privacy-First:** Berjalan di lingkungan cloud sementara (Google Colab), tanpa watermark dan data bisa langsung dihapus.

## 🛠️ Cara Penggunaan di Google Colab

### Langkah 1: Persiapan (Setup Phase)
1. Buka [Google Colab](https://colab.research.google.com/).
2. Buat Notebook baru dan pastikan Runtime diatur ke **GPU (T4)**.
3. Jalankan perintah berikut untuk mengkloning repositori ini dan memulai setup:

```bash
!git clone https://github.com/username/your-repo.git
%cd your-repo
!python setup_mimicmotion.py
```

Skrip `setup_mimicmotion.py` akan secara otomatis menginstal semua library yang dibutuhkan dan mengunduh model AI (Weights) yang diperlukan (sekitar 5GB+).

### Langkah 2: Menjalankan Antarmuka (Execution Phase)
Setelah setup selesai, jalankan antarmuka berbasis web (Gradio) dengan perintah:

```bash
!python run_gradio.py
```

1. Klik link **public URL** (berakhiran `.gradio.live`) yang muncul di output.
2. Unggah **1 Foto Target** (Full Body/Seluruh Tubuh).
3. Unggah **1 Video Referensi** (Gerakan yang ingin diikuti).
4. Klik tombol **Mulai Generate Video**.
5. Tunggu proses inference selesai (sekitar 5-10 menit untuk 16 frame pada GPU T4).

## 🏗️ Teknologi yang Digunakan
* **Model Utama:** [MimicMotion](https://github.com/Tencent/MimicMotion)
* **Backbone:** Stable Diffusion Video (SVD)
* **Pose Tracker:** DWPose
* **Interface:** Gradio

---
*Catatan: Repositori ini awalnya dibuat untuk tugas deret geometri, namun kini telah dikembangkan menjadi generator video AI sesuai blueprint.*
