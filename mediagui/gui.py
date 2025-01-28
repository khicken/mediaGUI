# gui.py

import sys
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QListWidget, QFileDialog, QLabel,
                            QProgressBar, QSpinBox, QComboBox, QGroupBox)
from worker import VideoConcatenationWorker

# note: variable 'mode' does absolutely nothing

class MainWindow(QMainWindow):
    def __init__(self, mode=0):
        super().__init__()
        self.setWindowTitle("mediaGUI")
        self.setMinimumSize(400, 400)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        ## File Selection
        self.file_list = QListWidget()
        layout.addWidget(QLabel("Selected Videos:"))
        layout.addWidget(self.file_list)
        
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Videos")
        self.add_button.clicked.connect(self.add_videos)
        button_layout.addWidget(self.add_button)
        
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.remove_selected)
        button_layout.addWidget(self.remove_button)
        layout.addLayout(button_layout)
    
        ## Export Controls
        extract_layout = QHBoxLayout()
        output_fps_layout = QHBoxLayout()
        output_format_layout = QHBoxLayout()
        extract_layout.setContentsMargins(5, 0, 0, 0)
        output_fps_layout.setContentsMargins(5, 0, 0, 0)
        output_format_layout.setContentsMargins(5, 0, 0, 0)

        # First line: Extract frames
        self.frame_extract_spinbox = QSpinBox()
        self.frame_extract_spinbox.setRange(0, 1000)
        self.frame_extract_spinbox.setValue(100)
        self.frame_extract_spinbox.setMinimumWidth(50)
        extract_layout.addWidget(QLabel("Extract "))
        extract_layout.addWidget(self.frame_extract_spinbox)
        self.frame_extract_suffix = 'frames'
        extract_layout.addWidget(QLabel(f'{self.frame_extract_suffix} per video'))
        extract_layout.addStretch()  # Push widgets to the left
        self.frame_extract_spinbox.valueChanged.connect(self.update_step_suffix)

        # Second line: Output FPS
        self.output_fps_spinbox = QSpinBox()
        self.output_fps_spinbox.setRange(1, 120)
        self.output_fps_spinbox.setValue(30)
        self.output_fps_spinbox.setMinimumWidth(40)
        output_fps_layout.addWidget(QLabel("Output FPS: "))
        output_fps_layout.addWidget(self.output_fps_spinbox)
        output_fps_layout.addStretch()  # Push widgets to the left

        # Third line: Output format
        self.output_format_combobox = QComboBox()
        self.output_format_combobox.addItems(['mp4', 'avi'])
        output_format_layout.addWidget(QLabel("Output format: "))
        output_format_layout.addWidget(self.output_format_combobox)
        output_format_layout.addStretch()  # Push widgets to the left

        # Add all horizontal layouts to the main layout
        layout.addLayout(extract_layout)
        layout.addLayout(output_fps_layout)
        layout.addLayout(output_format_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Concatenate!
        self.concat_button = QPushButton("Process video(s)")
        self.concat_button.clicked.connect(self.concat_videos)
        layout.addWidget(self.concat_button)
        
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        
        self.mode = mode    # not needed
        self.video_files = []

    def add_videos(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Videos",
            str(Path.home()),
            "Video Files (*.mp4 *.avi *.mov *.mkv);;All Files (*.*)"
        )
        
        if files:
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

    def concat_videos(self):
        if not self.video_files:
            self.status_label.setText("Please select videos first!")
            self.concat_button.setEnabled(True)
            return

        default_name = "concatenated_video.mp4"
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Concatenated Video",
            str(Path.home() / default_name),
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
            self.frame_extract_spinbox.setEnabled(False)
            self.output_fps_spinbox.setEnabled(False)
            self.output_format_combobox.setEnabled(False)
            
            self.worker = VideoConcatenationWorker(
                self.video_files, 
                output_path,
                frame_limit=self.frame_extract_spinbox.value(),
                output_fps=self.output_fps_spinbox.value(),
                output_format=self.output_format_combobox.currentText()
            )
            self.worker.progress.connect(self.update_progress)
            self.worker.finished.connect(self.concatenation_finished)
            self.worker.error.connect(self.concatenation_error)
            self.worker.start()
        else:
            self.concat_button.setEnabled(True)

    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def update_step_suffix(self, value):
        self.frame_extract_suffix = "frame" if value == 1 else "frames"
        
    def concatenation_finished(self):
        self.status_label.setText("Concatenation complete!")
        self.reset_ui()
        
    def concatenation_error(self, error_message):
        self.status_label.setText(f"Error: {error_message}")
        self.reset_ui()
        
    def reset_ui(self):
        self.progress_bar.setVisible(False)
        self.add_button.setEnabled(True)
        self.remove_button.setEnabled(True)
        self.frame_extract_spinbox.setEnabled(True)
        self.output_fps_spinbox.setEnabled(True)
        self.output_format_combobox.setEnabled(True)
        self.concat_button.setEnabled(True)

def main(mode=0):
    app = QApplication(sys.argv)
    if mode:
        window = MainWindow(mode)
    else:
        window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()