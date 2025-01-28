# worker.py

from PyQt6.QtCore import QThread, pyqtSignal

import cv2, platform
import numpy as np

class VideoConcatenationWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, video_files, output_path, frame_limit=0, output_fps=30, output_format='mp4'):
        super().__init__()
        self.video_files = video_files
        self.output_path = output_path
        self.frames_per_video = frame_limit
        self.output_fps = output_fps
        self.output_format=output_format

    def run(self):
        # bazinga
        self.extract_x_frames()
    
    def extract_x_frames(self):
        try:
            # Get properties of first video
            first_video = cv2.VideoCapture(str(self.video_files[0]))
            if not first_video.isOpened():
                raise Exception(f"Could not open video file: {self.video_files[0]}")
            
            width = int(first_video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(first_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            first_video.release()

            # Choose codec based on format and platform
            if self.output_format.lower() == 'mp4':
                if platform.system() == 'Darwin':
                    fourcc = cv2.VideoWriter_fourcc(*'avc1')
                elif platform.system() == 'Windows':
                    fourcc = cv2.VideoWriter_fourcc(*'H264')
                else:
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            elif self.output_format.lower() == 'avi':
                if platform.system() == 'Windows':
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                else:
                    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            else:
                raise Exception(f"Unsupported output format: {self.output_format}")

            out = cv2.VideoWriter(str(self.output_path), fourcc, self.output_fps, (width, height))
            if not out.isOpened():
                raise Exception("Failed to create output video file")

            total_frames = len(self.video_files) * self.frames_per_video
            processed_frames = 0
            
            # Process each video
            for video_path in self.video_files:
                cap = cv2.VideoCapture(str(video_path))
                if not cap.isOpened():
                    raise Exception(f"Could not open video file: {video_path}")

                # Get total frames in this video
                total_video_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                
                if total_video_frames < self.frames_per_video:
                    # If video has fewer frames than requested, use all frames
                    frame_indices = list(range(total_video_frames))
                else:
                    # Calculate evenly spaced frame indices
                    frame_indices = np.linspace(0, total_video_frames - 1, 
                                            self.frames_per_video, dtype=int)
                
                # Extract the selected frames
                for frame_idx in frame_indices:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                    ret, frame = cap.read()
                    
                    if not ret:
                        break
                    
                    # Ensure frame matches output dimensions
                    if frame.shape[1] != width or frame.shape[0] != height:
                        frame = cv2.resize(frame, (width, height))
                    
                    out.write(frame)
                    processed_frames += 1
                    progress = int((processed_frames / total_frames) * 100)
                    self.progress.emit(progress)
                
                cap.release()

            out.release()
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
        finally:
            try:
                out.release()
            except:
                pass