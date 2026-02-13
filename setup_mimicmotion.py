import os
import subprocess
import sys

def run_command(command):
    print(f"Running: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        print(line, end="")
    process.wait()
    if process.returncode != 0:
        print(f"Error running command: {command}")
        # sys.exit(1) # Don't exit, maybe it's just a warning

def setup():
    print("--- Memulai Setup AI Full Body Video Generator (MimicMotion) ---")

    # 1. Kloning Repositori
    if not os.path.exists("MimicMotion"):
        run_command("git clone https://github.com/Tencent/MimicMotion.git")

    # Masuk ke direktori
    os.chdir("MimicMotion")

    # 2. Instalasi Dependensi
    print("Menginstal pustaka yang dibutuhkan... Ini mungkin memakan waktu beberapa menit.")
    dependencies = [
        "diffusers==0.27.0",
        "transformers==4.32.1",
        "decord==0.6.0",
        "einops",
        "omegaconf",
        "onnxruntime-gpu",
        "opencv-python",
        "imageio",
        "imageio-ffmpeg",
        "gradio",
        "safetensors"
    ]
    run_command(f"pip install {' '.join(dependencies)}")

    # 3. Pengunduhan Model (Weights)
    print("Mengunduh model (Weights)...")
    if not os.path.exists("models"):
        os.makedirs("models")

    # DWPose
    if not os.path.exists("models/DWPose"):
        os.makedirs("models/DWPose")

    dwpose_files = {
        "yolox_l.onnx": "https://huggingface.co/yzd-v/DWPose/resolve/main/yolox_l.onnx?download=true",
        "dw-ll_ucoco_384.onnx": "https://huggingface.co/yzd-v/DWPose/resolve/main/dw-ll_ucoco_384.onnx?download=true"
    }

    for filename, url in dwpose_files.items():
        filepath = os.path.join("models/DWPose", filename)
        if not os.path.exists(filepath):
            print(f"Mengunduh {filename}...")
            run_command(f"wget '{url}' -O {filepath}")

    # MimicMotion Checkpoint
    checkpoint_url = "https://huggingface.co/tencent/MimicMotion/resolve/main/MimicMotion_1-1.pth"
    checkpoint_path = "models/MimicMotion_1-1.pth"
    if not os.path.exists(checkpoint_path):
        print("Mengunduh MimicMotion Checkpoint...")
        run_command(f"wget '{checkpoint_url}' -O {checkpoint_path}")

    print("\n--- Setup Selesai! ---")
    print("Sekarang kamu bisa menjalankan inference menggunakan script run_inference.py")

if __name__ == "__main__":
    setup()
