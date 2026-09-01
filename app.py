import streamlit as st
import os
import inference_wrapper

# Configuration
MODELS_DIR = "models"
INPUT_DIR = "input"
OUTPUT_DIR = "output"

for directory in [MODELS_DIR, INPUT_DIR, OUTPUT_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

st.set_page_config(page_title="AI Cover Studio", page_icon="", layout="wide")

if 'loaded_model' not in st.session_state:
    st.session_state.loaded_model = None
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = None


@st.dialog("➕ Tambah Model Baru")
def tambah_model_dialog():
    with st.form("tambah_model_form", clear_on_submit=True):
        new_model_name = st.text_input("Nama Model (Pisahkan dengan spasi atau underscore)")
        new_pth = st.file_uploader("Upload File Model (.pth)", type=['pth'])
        new_index = st.file_uploader("Upload File Index (.index)", type=['index'])
        new_image = st.file_uploader("Upload Gambar Cover (.png / .jpg)", type=['png', 'jpg', 'jpeg'])
        
        submit_btn = st.form_submit_button("Simpan Model")
        if submit_btn:
            if not new_model_name:
                st.error("Nama model wajib diisi!")
            elif not new_pth:
                st.error("File .pth wajib di-upload!")
            else:
                model_folder = os.path.join(MODELS_DIR, new_model_name.strip())
                if not os.path.exists(model_folder):
                    os.makedirs(model_folder)
                
                with open(os.path.join(model_folder, new_pth.name), "wb") as f:
                    f.write(new_pth.getbuffer())
                
                if new_index:
                    with open(os.path.join(model_folder, new_index.name), "wb") as f:
                        f.write(new_index.getbuffer())
                        
                if new_image:
                    ext = new_image.name.split('.')[-1]
                    with open(os.path.join(model_folder, f"cover.{ext}"), "wb") as f:
                        f.write(new_image.getbuffer())
                
                st.success(f"Model '{new_model_name}' berhasil ditambahkan!")
                st.rerun()

st.title("🎤 AI Song Cover Studio")

left_col, right_col = st.columns(2, gap="large")

with left_col:
    st.subheader(" Pengaturan Hardware")
    import torch
    gpu_available = torch.cuda.is_available()
    
    if not gpu_available:
        use_gpu = st.toggle(" Gunakan GPU (Disarankan)", value=False, disabled=True, help="GPU tidak terdeteksi.")
    else:
        use_gpu = st.toggle(" Gunakan GPU (Disarankan)", value=True, help="Otomatis Menyala jika GPU terdeteksi.")
    
    changed = inference_wrapper.set_device(use_gpu)
    if changed:
        st.session_state.loaded_model = None
        st.toast("⚙️ Hardware diubah. Menyiapkan ulang model...")

    st.subheader("⚙️ 1. Pengaturan Model")
    
    # Tombol Tambah Model (Popup)
    if st.button("➕ Tambah Model Baru", use_container_width=True):
        tambah_model_dialog()

    st.markdown("---")
    
    # Load Model (Deteksi folder)
    available_models = [d for d in os.listdir(MODELS_DIR) if os.path.isdir(os.path.join(MODELS_DIR, d))]
    

    if available_models and st.session_state.selected_model not in available_models:
        st.session_state.selected_model = available_models[0]

    if available_models:
        # Proses Loading Model di awal
        load_success = False
        if st.session_state.selected_model and st.session_state.loaded_model != st.session_state.selected_model:
            with st.spinner(f"Memuat model '{st.session_state.selected_model}' ke Mesin..."):
                model_folder = os.path.join(MODELS_DIR, st.session_state.selected_model)
                pth_file = ""
                index_file = ""
                for file in os.listdir(model_folder):
                    if file.endswith(".pth"):
                        pth_file = os.path.join(model_folder, file)
                    elif file.endswith(".index"):
                        index_file = os.path.join(model_folder, file)
                
                if not pth_file:
                    st.error("File .pth tidak ditemukan di dalam folder model!")
                else:
                    inference_wrapper.load_model(pth_file, index_path=index_file)
                    st.session_state.loaded_model = st.session_state.selected_model
                    load_success = True
        elif st.session_state.loaded_model == st.session_state.selected_model:
            load_success = True

        # Tampilkan Judul dan Status Aktif berjejer
        head_col1, head_col2 = st.columns([0.4, 0.6])
        with head_col1:
            st.markdown("### Pilih Model:")
        with head_col2:
            if load_success:
                st.markdown(f"<div style='margin-top: 22px;'><span style='background-color: rgba(0, 255, 0, 0.15); color: #00ff00; padding: 6px 12px; border-radius: 6px; font-weight: bold; font-size: 13px;'>✅ '{st.session_state.selected_model}' Aktif & Siap!</span></div>", unsafe_allow_html=True)
        
        # Buat grid 5 kolom agar lebih ringkas
        cols = st.columns(5)
        for idx, model_name in enumerate(available_models):
            with cols[idx % 5]:
                model_folder = os.path.join(MODELS_DIR, model_name)
                cover_image = None
                for file in os.listdir(model_folder):
                    if file.startswith("cover."):
                        cover_image = os.path.join(model_folder, file)
                        break
                
                is_selected = (st.session_state.selected_model == model_name)
                
                # Tampilkan Cover dengan ukuran lebih kecil (70px)
                if cover_image:
                    import base64
                    with open(cover_image, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode()
                    ext = cover_image.split('.')[-1]
                    st.markdown(f'<div style="text-align: center;"><img src="data:image/{ext};base64,{b64}" width="70" style="border-radius: 8px; object-fit: cover; aspect-ratio: 1/1;"></div>', unsafe_allow_html=True)
                else:
                    st.markdown("<div style='text-align: center; font-size: 30px; background:#222; border-radius:8px; padding:5px;'>🎤</div>", unsafe_allow_html=True)
                
                # Tampilkan Nama Model
                if is_selected:
                    st.markdown(f"<p style='text-align: center; color: #00ff00; font-weight: bold; font-size: 12px;'>{model_name[:10]} ✅</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='text-align: center; font-size: 12px;'>{model_name[:12]}</p>", unsafe_allow_html=True)
                    
                # Tombol Pilih
                if not is_selected:
                    if st.button("Pilih", key=f"btn_{model_name}", use_container_width=True):
                        st.session_state.selected_model = model_name
                        st.rerun()
                else:
                    # Dummy button agar layout rata
                    st.button("Terpilih", key=f"btn_{model_name}", use_container_width=True, disabled=True)
                    
        st.markdown("---")
    else:
        st.warning("⚠️ Belum ada model! Silakan tambah model baru di atas.")

with right_col:
    st.subheader("🎵 2. Upload Vokal & Convert")
    
    uploaded_file = st.file_uploader("Upload Vokal Asli (WAV/MP3)", type=['wav', 'mp3'])
    input_path = ""
    
    if uploaded_file is not None:
        input_path = os.path.join(INPUT_DIR, uploaded_file.name)
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    
    # Atur Pitch
    pitch = st.slider("Atur Pitch (Semitones)", -24, 24, 0, 1, help="Ubah ke +12 jika vokal asli Pria dan model Wanita. Ubah ke -12 jika vokal asli Wanita dan model Pria. Biarkan 0 jika gendernya sama.")
    
    with st.expander("🛠️ Pengaturan Lanjutan (Advanced)"):
        index_rate = st.slider("Index Rate (Pengaruh Aksen Model)", 0.0, 1.0, 0.75, 0.01, help="Turunkan jika hasil suara patah-patah/sember. (Hanya berfungsi jika model memiliki file .index)")
        protect = st.slider("Protect Voiceless Consonants", 0.0, 0.5, 0.33, 0.01, help="Menjaga suara napas/desis. Naikkan ke 0.5 jika suara napas terdengar seperti robot/elektronik.")
    
    if st.button("🚀 Convert Vokal Sekarang!", use_container_width=True):
        if not st.session_state.get('selected_model'):
            st.error("Pilih model di kolom kiri dulu!")
        elif not uploaded_file:
            st.error("Upload file vokal terlebih dahulu!")
        else:
            with st.spinner("Memproses AI Cover..."):
                output_name = f"Cover_{pitch}_{uploaded_file.name}".rsplit('.', 1)[0] + '.wav'
                output_path = os.path.join(OUTPUT_DIR, output_name)
                
                success, err_msg = inference_wrapper.convert_audio(input_path, output_path, pitch, index_rate, protect)
                
                if success and os.path.exists(output_path):
                    st.success("🎉 Selesai!")
                    st.audio(output_path, format="audio/wav")
                    with open(output_path, "rb") as file:
                        st.download_button("⬇️ Download AI Cover", data=file, file_name=output_name, mime="audio/wav", use_container_width=True)
                else:
                    st.error(f"❌ Gagal memproses audio.\n\nDetail:\n```\n{err_msg}\n```")
