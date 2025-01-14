import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QPushButton, QListWidget, QFileDialog, QLabel, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import cv2
import platform

class VideoConcatenationWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, video_files, output_path):
        super().__init__()
        self.video_files = video_files
        self.output_path = output_path

    def run(self):
        try:
            # Get properties of first video
            first_video = cv2.VideoCapture(str(self.video_files[0]))  # Convert Path to string
            if not first_video.isOpened():
                raise Exception(f"Could not open video file: {self.video_files[0]}")
            
            fps = first_video.get(cv2.CAP_PROP_FPS)
            width = int(first_video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(first_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            first_video.release()

            # Choose codec based on platform
            if platform.system() == 'Darwin':  # macOS
                fourcc = cv2.VideoWriter_fourcc(*'avc1')  # H.264 codec
            elif platform.system() == 'Windows':
                fourcc = cv2.VideoWriter_fourcc(*'H264')  # H.264 codec
            else:  # Linux and others
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Default to mp4v

            # Create video writer with platform-specific codec
            out = cv2.VideoWriter(str(self.output_path), fourcc, fps, (width, height))
            if not out.isOpened():
                raise Exception("Failed to create output video file")

            total_frames = 0
            # First pass: count total frames
            for video_path in self.video_files:
                cap = cv2.VideoCapture(str(video_path))
                if not cap.isOpened():
                    raise Exception(f"Could not open video file: {video_path}")
                total_frames += int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                cap.release()

            processed_frames = 0
            # Second pass: process videos
            for video_path in self.video_files:
                cap = cv2.VideoCapture(str(video_path))
                
                while True:
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
            # Ensure all resources are released
            try:
                out.release()
            except:
                pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Formatter")
        self.setMinimumSize(600, 400)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # List widget for selected files
        self.file_list = QListWidget()
        layout.addWidget(QLabel("Selected Videos:"))
        layout.addWidget(self.file_list)
        
        # Buttons
        self.add_button = QPushButton("Add Videos")
        self.add_button.clicked.connect(self.add_videos)
        layout.addWidget(self.add_button)
        
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.remove_selected)
        layout.addWidget(self.remove_button)
        
        self.concatenate_button = QPushButton("Concatenate Videos")
        self.concatenate_button.clicked.connect(self.concatenate_videos)
        layout.addWidget(self.concatenate_button)

        self.extract_button = QPushButton("Extract Frames")
        self.extract_button.clicked.connect(self.extract_frames)
        layout.addWidget(self.extract_button)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        
        self.video_files = []

    def add_videos(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Videos",
            str(Path.home()),  # Start in user's home directory
            "Video Files (*.mp4 *.avi *.mov *.mkv);;All Files (*.*)"
        )
        
        if files:
            # Convert to Path objects for better cross-platform compatibility
            self.video_files.extend([Path(f) for f in files])
            self.file_list.clear()
            self.file_list.addItems([f.name for f in self.video_files])

    def remove_selected(self):
        selected_items = self.file_list.selectedItems()
        for item in selected_items:
            idx = self.file_list.row(item)
            del self.video_files[idx]
        
        self.file_list.clear()
        self.file_list.addItems([f.name for f in self.video_files])

    def concatenate_videos(self):
        if not self.video_files:
            self.status_label.setText("Please select videos first!")
            return

        default_name = "concatenated_video.mp4"
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Concatenated Video",
            str(Path.home() / default_name),  # Default to user's home directory
            "MP4 Video (*.mp4)"
        )
        
        if output_path:
            output_path = Path(output_path)
            if output_path.suffix.lower() != '.mp4':
                output_path = output_path.with_suffix('.mp4')
                
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.add_button.setEnabled(False)
            self.remove_button.setEnabled(False)
            self.concatenate_button.setEnabled(False)
            
            self.worker = VideoConcatenationWorker(self.video_files, output_path)
            self.worker.progress.connect(self.update_progress)
            self.worker.finished.connect(self.concatenation_finished)
            self.worker.error.connect(self.concatenation_error)
            self.worker.start()
    
    def extract_frames(self):
        

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        
    def concatenation_finished(self):
        self.status_label.setText("Concatenation completed successfully!")
        self.reset_ui()
        
    def concatenation_error(self, error_message):
        self.status_label.setText(f"Error: {error_message}")
        self.reset_ui()
    
    def extraction_finished(self):
        self.status_label.setText("Frame extraction completed successfully!")
        self.reset_ui()
        
    def reset_ui(self):
        self.progress_bar.setVisible(False)
        self.add_button.setEnabled(True)
        self.remove_button.setEnabled(True)
        self.concatenate_button.setEnabled(True)
        self.extract_button.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()