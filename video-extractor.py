#requirements 
#MSVC v14.x
#Windows 10 SDK
#C++ CMake tools for Windows are listed (they are by default).

import cv2
import glob
import os
import insightface
from insightface.app import FaceAnalysis

# Get the directory of the current script
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

            # Use aligned image if available, else fallback to bbox crop
            if aligned is not None and aligned.size > 0:
                out_img = aligned
            else:
                print(f"Warning: Empty aligned face on frame {frame_count}, face {i}. Falling back to bbox crop.")
                x1, y1, x2, y2 = face.bbox.astype(int)

                # Clamp coordinates to frame size
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(frame.shape[1], x2)
                y2 = min(frame.shape[0], y2)

                out_img = frame[y1:y2, x1:x2]

            # Save image if valid
            if out_img is not None and out_img.size > 0:
                out_path = os.path.join(output_dir, f'frame{frame_count:05}_face{i}.png')
                cv2.imwrite(out_path, out_img)
            else:
                print(f"Error: Could not save face image from frame {frame_count}, face {i}")

        frame_count += 1
finally:
    cap.release()

print("Face extraction completed.")

