import os
import sys
import torch
import gradio as gr
from pathlib import Path

# Masuk ke direktori MimicMotion jika ada
if os.path.exists("MimicMotion"):
    os.chdir("MimicMotion")
else:
    print("Error: Direktori MimicMotion tidak ditemukan. Jalankan setup_mimicmotion.py terlebih dahulu.")
    sys.exit(1)

# Tambahkan direktori saat ini ke sys.path
sys.path.append(os.getcwd())

from inference import preprocess, run_pipeline, create_pipeline
from mimicmotion.utils.utils import save_to_mp4
from omegaconf import OmegaConf

# Konfigurasi Default
DEFAULT_CONFIG = {
    "base_model_path": "stabilityai/stable-video-diffusion-img2vid-xt-1-1",
    "ckpt_path": "models/MimicMotion_1-1.pth",
    "test_case": [] # Akan diisi saat runtime
}

pipeline = None
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model():
    global pipeline
    if pipeline is None:
        print("Sedang memuat model ke GPU... Ini bisa memakan waktu.")
        conf = OmegaConf.create(DEFAULT_CONFIG)
        pipeline = create_pipeline(conf, device)
    return pipeline

def generate_video(image_path, video_path, resolution, num_frames, fps, seed):
    try:
        os.makedirs("outputs", exist_ok=True)
        pipe = load_model()

        # Pastikan seed adalah integer
        seed = int(seed)

        task_config = OmegaConf.create({
            "ref_video_path": video_path,
            "ref_image_path": image_path,
            "num_frames": int(num_frames),
            "resolution": int(resolution),
            "frames_overlap": 6,
            "fps": int(fps),
            "noise_aug_strength": 0.02,
            "guidance_scale": 2.0,
            "sample_stride": 2,
            "seed": seed
        })

        print(f"Memproses video: {video_path} dan gambar: {image_path}")
        pose_pixels, image_pixels = preprocess(
            task_config.ref_video_path, task_config.ref_image_path,
            resolution=task_config.resolution, sample_stride=task_config.sample_stride
        )

        print("Menjalankan AI Inference...")
        _video_frames = run_pipeline(
            pipe,
            image_pixels, pose_pixels,
            device, task_config
        )

        output_filename = f"outputs/output_{seed}.mp4"
        save_to_mp4(_video_frames, output_filename, fps=fps)
        print(f"Video berhasil disimpan di: {output_filename}")
        return output_filename
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"

# Antarmuka Gradio
def interface():
    with gr.Blocks(title="AI Full Body Video Generator") as demo:
        gr.Markdown("# 🕺 AI Full Body Video Generator (MimicMotion)")
        gr.Markdown("Gunakan skrip ini di Google Colab untuk membuat video animasi dari satu foto.")

        with gr.Row():
            with gr.Column():
                input_image = gr.Image(type="filepath", label="1. Unggah Foto Target (Full Body)")
                input_video = gr.Video(label="2. Unggah Video Referensi (Gerakan)")

                with gr.Accordion("Pengaturan Lanjutan", open=False):
                    resolution = gr.Slider(minimum=256, maximum=1024, value=576, step=64, label="Resolusi")
                    num_frames = gr.Slider(minimum=8, maximum=72, value=16, step=8, label="Jumlah Frame (Max 72)")
                    fps = gr.Slider(minimum=1, maximum=30, value=15, step=1, label="FPS")
                    seed = gr.Number(value=42, label="Seed (Angka Acak)")

                btn = gr.Button("Mulai Generate Video", variant="primary")

            with gr.Column():
                output_video = gr.Video(label="Hasil Video")

        btn.click(
            generate_video,
            inputs=[input_image, input_video, resolution, num_frames, fps, seed],
            outputs=output_video
        )

        gr.Markdown("### Petunjuk Penggunaan:")
        gr.Markdown("1. Tunggu hingga model dimuat (pertama kali running akan agak lama).")
        gr.Markdown("2. Gunakan resolusi 576 untuk performa terbaik di T4 GPU.")
        gr.Markdown("3. Setelah selesai, jangan lupa unduh hasil videonya.")

    print("Meluncurkan antarmuka Gradio...")
    demo.launch(share=True, debug=True)

if __name__ == "__main__":
    interface()
