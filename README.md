# 🎤 Your Voice is Yours (AI Song Cover Studio)

Proyek ini adalah antarmuka web (Web UI) berbasis **Streamlit** dan sekumpulan **Jupyter Notebook** yang dirancang untuk mempermudah proses pengubahan suara (Inference) dan pelatihan suara (Training) menggunakan teknologi **RVC (Retrieval-based Voice Conversion)**.

Dengan proyek ini, Anda dapat mengkloning suara, mengubah vokal penyanyi asli menjadi suara Anda sendiri, atau melatih AI untuk mengenali karakter suara baru.

---

## 🚀 Fitur Utama

- **Web UI yang Ramah Pengguna**: Mengubah suara vokal lagu hanya dengan beberapa klik melalui antarmuka web Streamlit.
- **Manajemen Model**: Mengunggah, menyimpan, dan memilih file model `.pth` beserta file `.index` langsung dari web.
- **Jupyter Notebook Tersedia**:
  - `RVC_Training.ipynb`: Panduan lengkap _step-by-step_ untuk melatih dataset suara baru (bisa dijalankan di Google Colab atau lokal).
  - `RVC_Inference.ipynb`: Skrip murni untuk melakukan konversi suara secara massal tanpa menggunakan Web UI.
- **Deteksi Otomatis**: Folder `models`, `input`, dan `output` akan otomatis terdeteksi atau dibuat jika belum ada.

---

## 🛠️ Persiapan dan Instalasi (Setup)

### 1. Kloning Repositori

Buka terminal Anda dan _clone_ repositori ini:

```bash
git clone https://github.com/Asenn4/Your-Voice-is-Yours.git
cd Your-Voice-is-Yours
```

### 2. Buat Virtual Environment (Sangat Disarankan)

Gunakan Python 3.9 - 3.10.

```bash
python -m venv myenv
# Untuk Windows:
myenv\Scripts\activate
# Untuk Mac/Linux:
source myenv/bin/activate
```

### 3. Instalasi Dependencies

Instal semua modul yang dibutuhkan (termasuk PyTorch dengan CUDA):

```bash
pip install -r requirements.txt
```

_(Catatan: Jika Anda mendapati error module `torchaudio` saat menjalankan aplikasi, silakan jalankan `pip install torchaudio` secara terpisah)._

---

## 🎮 Cara Penggunaan

### 1. Menjalankan Aplikasi Web (AI Cover Studio)

Pastikan Anda sudah berada di dalam folder proyek dan _virtual environment_ menyala. Jalankan perintah:

```bash
streamlit run app.py
```

Browser akan otomatis membuka `http://localhost:8501`.

- Tambahkan model suara (`.pth`) Anda pada tombol **Tambah Model Baru**.
- Upload file _acapella_ atau vokal murni Anda.
- Atur nada (_Pitch_) dan klik **Convert Vokal Sekarang!**

### 2. Melatih Suara Sendiri (Training Model Baru)

Jika Anda belum memiliki file `.pth` dan ingin membuat AI meniru suara Anda sendiri:

1. Buka file `RVC_Training.ipynb`.
2. Jika Anda memiliki GPU NVIDIA (VRAM 6GB+), Anda bisa menjalankannya langsung di VSCode/Jupyter lokal.
3. **Jika tidak punya GPU (Laptop Kentang)**: Unggah file `RVC_Training.ipynb` ke [Google Colab](https://colab.research.google.com/), nyalakan GPU dari menu _Runtime_, dan ikuti instruksi sel kodenya di sana.
4. Setelah selesai, pindahkan hasil file `.pth` dan `.index` ke dalam folder `models/` di proyek ini.

---

## 📁 Struktur Direktori Penting

- `app.py`: File utama untuk Web UI Streamlit.
- `inference_wrapper.py`: Logika di balik layar yang menghubungkan Web UI dengan _engine_ RVC.
- `models/`: Tempat Anda meletakkan folder file `.pth` dan `.index`.
- `input/`: Tempat berkumpulnya file audio asli yang siap di-_convert_.
- `output/`: Hasil suara AI akan tersimpan di sini.

---

**Disclaimer**: Proyek ini dibuat untuk tujuan pembelajaran, seni, dan eksperimen pribadi. Pastikan Anda memiliki izin saat mengkloning atau menggunakan suara orang lain!
