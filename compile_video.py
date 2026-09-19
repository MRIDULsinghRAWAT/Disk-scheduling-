import os
import cv2
import shutil

FRAMES_DIR = "video_frames"
OUTPUT_VIDEO_PATH = "Disk_Scheduling_Simulation_Demo.mp4"
DESKTOP_PATH = r"C:\Users\Mridul\Desktop\Disk_Scheduling_Simulation_Demo.mp4"
FPS = 8.0

def compile_frames_to_mp4():
    if not os.path.exists(FRAMES_DIR):
        print("Frames directory not found!")
        return

    frames = sorted([f for f in os.listdir(FRAMES_DIR) if f.endswith('.jpg')])
    if not frames:
        print("No frames found!")
        return

    first_frame_path = os.path.join(FRAMES_DIR, frames[0])
    sample_img = cv2.imread(first_frame_path)
    height, width, layers = sample_img.shape
    print(f"Frame dimensions: {width}x{height}, Total frames: {len(frames)}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(OUTPUT_VIDEO_PATH, fourcc, FPS, (width, height))

    count = 0
    for frame_name in frames:
        frame_path = os.path.join(FRAMES_DIR, frame_name)
        img = cv2.imread(frame_path)
        if img is not None:
            video.write(img)
            count += 1

    video.release()
    print(f"Video created successfully: {OUTPUT_VIDEO_PATH} ({count} frames encoded)")

    # Copy to Desktop root
    shutil.copyfile(OUTPUT_VIDEO_PATH, DESKTOP_PATH)
    print(f"Video copied to Desktop: {DESKTOP_PATH}")

if __name__ == "__main__":
    compile_frames_to_mp4()
