#requirements 
#MSVC v14.x
#Windows 10 SDK
#C++ CMake tools for Windows are listed (they are by default).

import cv2
import glob
import os
import insightface
from insightface.app import FaceAnalysis

# Get the directory of the current .py script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Automatically find the video file named 'input.*' in the script directory
video_files = glob.glob(os.path.join(script_dir, 'input.*'))
if not video_files:
    raise FileNotFoundError("No file named 'input.*' found in the script directory.")
video_path = video_files[0]
print(f"Using video file: {video_path}")

# Load video
cap = cv2.VideoCapture(video_path)

# Load face detector
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=-1)  # Use -1 for CPU

# Create output directory in the script location
output_dir = os.path.join(script_dir, 'faces')
os.makedirs(output_dir, exist_ok=True)

# Process each frame and extract faces
frame_count = 0
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = app.get(frame)
        for i, face in enumerate(faces):
            aligned = face.aligned
            out_path = os.path.join(output_dir, f'frame{frame_count:05}_face{i}.png')
            cv2.imwrite(out_path, aligned)

        frame_count += 1
finally:
    cap.release()

print("Face extraction completed.")
