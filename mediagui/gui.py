# gui.py

import sys
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QListWidget, QFileDialog, QLabel, 
                            QProgressBar, QSpinBox, QGroupBox)
from worker import VideoConcatenationWorker

class MainWindow(QMainWindow):
    def __init__(self, mode=0):
        super().__init__()
        self.setWindowTitle("mediaGUI")
        self.setMinimumSize(400, 400)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # List widget for selected files
        self.file_list = QListWidget()
        layout.addWidget(QLabel("Selected Videos:"))
        layout.addWidget(self.file_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Videos")
        self.add_button.clicked.connect(self.add_videos)
        button_layout.addWidget(self.add_button)
        
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.remove_selected)
        button_layout.addWidget(self.remove_button)
        layout.addLayout(button_layout)
        
        if mode == 0:
            # Frame extraction controls group
            extract_group = QGroupBox("Frame Extraction")
            extract_layout = QHBoxLayout()
            extract_layout.setContentsMargins(4, 4, 4, 4)
            extract_group.setLayout(extract_layout)
            
            # Create a sub-layout for the spinbox and its label
            spinbox_layout = QHBoxLayout()
            spinbox_layout.setSpacing(10)
            extract_label = QLabel("Extract")
            extract_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            spinbox_layout.addWidget(extract_label)
            
            self.frame_count_spinbox = QSpinBox()
            self.frame_count_spinbox.setRange(1, 1000)
            self.frame_count_spinbox.setValue(100)
            self.frame_count_spinbox.setMinimumWidth(70)
            self.frame_count_spinbox.setSuffix(" frames")
            spinbox_layout.addWidget(self.frame_count_spinbox)
            spinbox_layout.addWidget(QLabel(" per video"))
            
            extract_layout.addLayout(spinbox_layout)
            
            # Add note about output
            extract_layout.addStretch()
            output_note = QLabel("Output will be played at 30 FPS")
            output_note.setStyleSheet("color: #666; font-style: italic; margin: 0px;")
            extract_layout.addWidget(output_note)
            
            layout.addWidget(extract_group)
        elif mode == 1:
            # Frame step controls group
            step_group = QGroupBox()
            step_layout = QHBoxLayout()
            step_group.setLayout(step_layout)

            # Frame step spinbox
            step_layout.addWidget(QLabel("Process every"))
            self.frame_step_spinbox = QSpinBox()
            self.frame_step_spinbox.setRange(1, 100)  # Allow steps from 1 to 100
            self.frame_step_spinbox.setValue(1)
            def update_step_value(value):
                if value == 1: self.frame_step_spinbox.setSuffix(" frame")
                else: self.frame_step_spinbox.setSuffix(" frames")
            update_step_value(1)
            self.frame_step_spinbox.valueChanged.connect(update_step_value)
            step_layout.addWidget(self.frame_step_spinbox)
            
            layout.addWidget(step_group)

            # Add speed multiplier label
            step_layout.addSpacing(20)  # Add some space between controls
            self.speed_label = QLabel("(1x speed)")
            self.speed_label.setStyleSheet("color: #666;")  # Subtle gray color
            step_layout.addWidget(self.speed_label)
        
        

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Concatenate!
        self.concat_button = QPushButton("Concatenate")
        self.concat_button.clicked.connect(self.concat_videos)
        layout.addWidget(self.concat_button)
        
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        if mode == 1:
            layout.addWidget(step_group)
        
        self.mode = mode
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
            self.frame_step_spinbox.setEnabled(False)
            
            self.worker = VideoConcatenationWorker(
                self.video_files, 
                output_path,
                mode=self.mode,
                output_fps=self.output_fps,
                param=self.frame_step_spinbox.value()
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
        """Update the spinbox suffix and speed indicator based on the value"""
        suffix = " frame" if value == 1 else " frames"
        self.frame_step_spinbox.setSuffix(suffix)
        
        # Update speed multiplier label
        speed_text = "Normal speed" if value == 1 else f"{value}x faster"
        self.speed_label.setText(f"({speed_text})")
        
        # Make the speed label red when speed is high (>10x)
        if value > 10:
            self.speed_label.setStyleSheet("color: #e74c3c;")  # Red for high speeds
        else:
            self.speed_label.setStyleSheet("color: #666;")  # Normal gray
        
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
        self.frame_step_spinbox.setEnabled(True)
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