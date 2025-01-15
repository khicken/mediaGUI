from PyQt6.QtCore import QThread, pyqtSignal

import cv2, platform

class VideoConcatenationWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, video_files, output_path, frame_step=1):
        super().__init__()
        self.video_files = video_files
        self.output_path = output_path
        self.frame_step = frame_step

    def run(self):
        try:
            # Get properties of first video
            first_video = cv2.VideoCapture(str(self.video_files[0]))
            if not first_video.isOpened():
                raise Exception(f"Could not open video file: {self.video_files[0]}")
            
            # Keep original FPS regardless of step size
            fps = first_video.get(cv2.CAP_PROP_FPS)
            width = int(first_video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(first_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            first_video.release()

            # Choose codec based on platform
            if platform.system() == 'Darwin':
                fourcc = cv2.VideoWriter_fourcc(*'avc1')
            elif platform.system() == 'Windows':
                fourcc = cv2.VideoWriter_fourcc(*'H264')
            else:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')

            out = cv2.VideoWriter(str(self.output_path), fourcc, fps, (width, height))
            if not out.isOpened():
                raise Exception("Failed to create output video file")

            total_frames = 0
            # First pass: count frames that will be included
            for video_path in self.video_files:
                cap = cv2.VideoCapture(str(video_path))
                if not cap.isOpened():
                    raise Exception(f"Could not open video file: {video_path}")
                frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                # Calculate how many frames we'll actually use
                included_frames = (frames + self.frame_step - 1) // self.frame_step
                total_frames += included_frames
                cap.release()

            processed_frames = 0
            
            # Second pass: process videos
            for video_path in self.video_files:
                cap = cv2.VideoCapture(str(video_path))
                total_video_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                
                # Calculate which frame indices to keep for this video
                frames_to_keep = range(0, total_video_frames, self.frame_step)
                
                for target_frame in frames_to_keep:
                    # Set the frame position directly
                    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
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
