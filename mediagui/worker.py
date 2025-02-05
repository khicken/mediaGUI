# worker.py
# Last Modified: 2025-02-05

import cv2
import numpy as np
import platform
from PyQt6.QtCore import QThread, pyqtSignal

class VideoConcatenationWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, video_files, output_path, frames_per_video=0, output_fps=30, output_format='mp4'):
        super().__init__()
        self.video_files = video_files
        self.output_path = output_path
        self.frames_per_video = frames_per_video
        self.output_fps = output_fps
        self.output_format = output_format

        self.total_frames_read = 0
        self.total_frames_wrote = 0
        self.total_frames = len(self.video_files) * self.frames_per_video
        
        # GPU capabilities detection
        self.use_gpu = False
        try:
            if platform.system() != 'Darwin' and cv2.cuda.getCudaEnabledDeviceCount() > 0:
                self.use_gpu = True
                self.cuda_device = cv2.cuda.Device(0)
                self.cuda_stream = cv2.cuda.Stream()
                print("CUDA GPU acceleration available")
            else:
                print("CUDA GPU acceleration not available")
        except Exception as e:
            print(f"GPU detection error: {e}")

    def gpu_extract_frames(self, video_path, frame_indices, width, height):
        frames = []
        cap = cv2.cuda.VideoReader_GPU(str(video_path))
        
        gpu_resizer = cv2.cuda.createResize((width, height))

        for frame_idx in frame_indices:
            try:
                # GPU-accelerated frame reading
                gpu_frame = cap.read(frame_idx)

                if not gpu_frame:
                    print(f'Failed to read frame {frame_idx}!')
                    continue
                
                # Resize on GPU
                if gpu_frame.size()[0] != height or gpu_frame.size()[1] != width:
                    gpu_frame = gpu_resizer.compute(gpu_frame, self.cuda_stream)
                
                # Download frame to CPU
                frame = gpu_frame.download()
                frames.append(frame)
            except Exception as e:
                print(f"GPU frame extraction error: {e}")
        
        # Sync the CUDA stream
        self.cuda_stream.waitForCompletion()

        return frames

    def cpu_extract_frames(self, video_path, frame_indices, total_frames, width, height):
        frames = []
        cap = cv2.VideoCapture(str(video_path))
        
        frame_interval = frame_indices[1] - frame_indices[0]  # Assuming evenly spaced frames
        next_frame_to_extract = frame_indices[0]
        
        current_frame_idx = 0
        
        while current_frame_idx <= max(frame_indices):
            ret, frame = cap.read()
            
            if not ret:
                break
            
            if current_frame_idx == next_frame_to_extract:
                if frame.shape[1] != width or frame.shape[0] != height:
                    frame = cv2.resize(frame, (width, height))
                
                frames.append(frame)
                self.total_frames_read += 1
                self.updateProgressBar()
                
                next_frame_to_extract += frame_interval

            current_frame_idx += 1

        cap.release()
        return frames
    
    def updateProgressBar(self):
        stage_one = int((self.total_frames_read / self.total_frames) * 80)
        stage_two = int((self.total_frames_wrote / self.total_frames) * 20)
        self.progress.emit(stage_one + stage_two)

    def run(self):
        try:
            # Get width and height from the first video
            first_video = cv2.VideoCapture(str(self.video_files[0]))
            if not first_video.isOpened():
                raise Exception(f"Failed to open video: {self.video_files[0]}")
            width = int(first_video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(first_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            first_video.release()

            # Codec configuration
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
                raise Exception(f"Failed to open output video: {self.output_path}")

            # Process videos
            for video_path in self.video_files:
                cap = cv2.VideoCapture(str(video_path))
                if not cap.isOpened():
                    raise Exception(f"Failed to open video: {video_path}")
                total_video_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                cap.release()

                # If the video has less frames than the desired frames per video, extract all frames
                if total_video_frames < self.frames_per_video:
                    frame_indices = list(range(total_video_frames))
                # Otherwise, extract evenly spaced frames
                else:
                    frame_indices = list(np.linspace(0, total_video_frames - 1, self.frames_per_video, dtype=int))

                # Select extract frames based on GPU availability
                extract_func = self.gpu_extract_frames if self.use_gpu else self.cpu_extract_frames
                frames = extract_func(video_path, frame_indices, self.total_frames, width, height)

                # Write frames to output video
                for frame in frames:
                    out.write(frame)
                    self.total_frames_wrote += 1
                    self.updateProgressBar()

            out.release()
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
        finally:
            try:
                out.release()
            except:
                pass