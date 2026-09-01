import os
import torch

# Patch untuk PyTorch 2.6+ agar kompatibel dengan RVC (Fairseq dkk)
original_torch_load = torch.load
def patched_torch_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return original_torch_load(*args, **kwargs)
torch.load = patched_torch_load

# pyright: ignore [reportMissingImports]
from rvc_python.infer import RVCInference

# Inisialisasi Engine RVC
device = "cuda:0" if torch.cuda.is_available() else "cpu:0"
rvc = RVCInference(device=device)

def get_model_version(model_path):
    try:
        cpt = torch.load(model_path, map_location="cpu")
        if "version" in cpt:
            return cpt["version"]
        emb_shape = cpt.get("weight", {}).get("enc_p.emb_phone.weight", None)
        if emb_shape is not None:
            if emb_shape.shape[1] == 256:
                return "v1"
            elif emb_shape.shape[1] == 768:
                return "v2"
    except:
        pass
    return "v2"

def load_model(model_path, index_path=""):
    """
    Memuat model suara RVC (.pth).
    """
    version = get_model_version(model_path)
    rvc.load_model(model_path, version=version, index_path=index_path)

def convert_audio(input_audio_path, output_audio_path, pitch=0):
    """
    Mengubah audio menggunakan model RVC yang sudah dimuat.
    pitch: Integer semitones (+12 naik satu oktaf, -12 turun satu oktaf)
    """
    try:
        # Cek apakah index aktif untuk model saat ini
        idx_rate = 0.0
        if rvc.current_model:
            model_info = rvc.models.get(rvc.current_model, {})
            if model_info.get("index"):
                idx_rate = 0.75

        rvc.set_params(
            f0up_key=pitch,
            f0method="rmvpe",
            index_rate=idx_rate,
            filter_radius=3,
            resample_sr=0,
            rms_mix_rate=0.25,
            protect=0.33
        )
        rvc.infer_file(input_path=input_audio_path, output_path=output_audio_path)
        return True, ""
    except Exception as e:
        import traceback
        err_msg = traceback.format_exc()
        print(f"Error saat inference RVC:\n{err_msg}")
        return False, err_msg
