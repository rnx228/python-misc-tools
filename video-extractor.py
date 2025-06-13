import os
import cv2
import subprocess
import face_alignment
import numpy as np
from glob import glob

# === CONFIGURATION ===
video_folder = "videos"  # Folder containing input videos
temp_frames = "temp_frames"
output_faces = "aligned_faces"  # Final output folder
fps = 1  # Extract 1 frame per second
start_counter = 0

# Create folders
os.makedirs(temp_frames, exist_ok=True)
os.makedirs(output_faces, exist_ok=True)

# Initialize face alignment
fa = face_alignment.FaceAlignment(face_alignment.LandmarksType.TWO_D, flip_input=False)

# === FUNCTION TO EXTRACT FRAMES FROM VIDEO ===
def extract_frames(video_path, frame_dir, fps=1):
    os.makedirs(frame_dir, exist_ok=True)
    cmd = [
        "ffmpeg", "-i", video_path, "-vf", f"fps={fps}",
        os.path.join(frame_dir, "%04d.jpg")
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# === PROCESS ALL VIDEOS ===
for video in sorted(glob(os.path.join(video_folder, "*.mp4"))):
    print(f"[INFO] Processing video: {video}")
    video_name = os.path.splitext(os.path.basename(video))[0]
    frame_dir = os.path.join(temp_frames, video_name)

    extract_frames(video, frame_dir, fps)

    for frame_file in sorted(glob(os.path.join(frame_dir, "*.jpg"))):
        img = cv2.imread(frame_file)
        if img is None:
            continue

        preds = fa.get_landmarks(img)
        if preds is None:
            continue

        for face in preds:
            x_min = max(int(np.min(face[:, 0])) - 20, 0)
            y_min = max(int(np.min(face[:, 1])) - 20, 0)
            x_max = min(int(np.max(face[:, 0])) + 20, img.shape[1])
            y_max = min(int(np.max(face[:, 1])) + 20, img.shape[0])

            aligned_face = img[y_min:y_max, x_min:x_max]
            aligned_face = cv2.resize(aligned_face, (224, 224))

            out_path = os.path.join(output_faces, f"{start_counter:05d}.jpg")
            cv2.imwrite(out_path, aligned_face)
            start_counter += 1

print(f"\n✅ Done! Total aligned faces saved to: {output_faces}")


