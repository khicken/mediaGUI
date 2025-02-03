# worker.py

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
        
        # GPU capabilities detection
        self.use_gpu = False
        try:
            if platform.system() != 'Darwin' and cv2.cuda.getCudaEnabledDeviceCount() > 0:
                self.use_gpu = True
                self.cuda_device = cv2.cuda.Device(0)
                self.cuda_stream = cv2.cuda.Stream()
                print("CUDA GPU acceleration available")
        except Exception as e:
            print(f"GPU detection error: {e}")

    def gpu_extract_frames(self, video_path, frame_indices, width, height):
        frames = []
        cap = cv2.cuda.VideoReader_GPU(str(video_path))
        
        for frame_idx in frame_indices:
            try:
                # GPU-accelerated frame reading
                gpu_frame = cap.read(frame_idx)
                
                # Resize on GPU
                if gpu_frame.size()[0] != height or gpu_frame.size()[1] != width:
                    gpu_resizer = cv2.cuda.createResize((width, height))
                    gpu_frame = gpu_resizer.compute(gpu_frame, self.cuda_stream)
                
                # Download frame to CPU
                frame = gpu_frame.download()
                frames.append(frame)
            except Exception as e:
                print(f"GPU frame extraction error: {e}")
        
        return frames

    def cpu_extract_frames(self, video_path, frame_indices, width, height):
        frames = []
        cap = cv2.VideoCapture(str(video_path))
        
        for frame_idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            
            if not ret:
                break
            
            if frame.shape[1] != width or frame.shape[0] != height:
                frame = cv2.resize(frame, (width, height))
            
            frames.append(frame)
        
        cap.release()
        return frames

    def run(self):
        try:
            # First video properties detection
            first_video = cv2.VideoCapture(str(self.video_files[0]))
            width = int(first_video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(first_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            first_video.release()

            # Codec configuration (previous implementation)
            if self.output_format.lower() == 'mp4':
                fourcc = cv2.VideoWriter_fourcc(*('avc1' if platform.system() == 'Darwin' else 
                                                  'H264' if platform.system() == 'Windows' else 
                                                  'mp4v'))
            elif self.output_format.lower() == 'avi':
                fourcc = cv2.VideoWriter_fourcc(*('XVID' if platform.system() == 'Windows' else 'MJPG'))
            else:
                raise Exception(f"Unsupported output format: {self.output_format}")

            out = cv2.VideoWriter(str(self.output_path), fourcc, self.output_fps, (width, height))
            
            total_frames = len(self.video_files) * self.frames_per_video
            processed_frames = 0

            # Frame extraction logic
            for video_path in self.video_files:
                cap = cv2.VideoCapture(str(video_path))
                total_video_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                cap.release()

                frame_indices = list(range(total_video_frames)) if total_video_frames < self.frames_per_video \
                    else list(np.linspace(0, total_video_frames - 1, self.frames_per_video, dtype=int))

                # Choose extraction method based on GPU availability
                extract_func = self.gpu_extract_frames if self.use_gpu else self.cpu_extract_frames
                frames = extract_func(video_path, frame_indices, width, height)

                for frame in frames:
                    out.write(frame)
                    processed_frames += 1
                    self.progress.emit(int((processed_frames / total_frames) * 100))

            out.release()
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
        finally:
            try:
                out.release()
            except:
                pass