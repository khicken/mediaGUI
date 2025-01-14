import os
import cv2
import numpy as np
def concat_frames(input_video_files, output_video_path, output_file_name):
    """
    Combine extracted frames from multiple videos into a single video.
    
    Args:
        input_video_files (list): List of input video file paths
        output_video_path (str): Directory to save the output video
        output_file_name (str): Name of the output video file
    """
    # Config
    frames_to_extract = 330
    all_extracted_frames = []
    
    # Extract frames from each video file
    for video_path in input_video_files:
        v = cv2.VideoCapture(video_path)
        total_frames = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Extract frames evenly
        extracted_frames = []
        for i in range(frames_to_extract):
            frame_index = round((i - 1) * (total_frames - 1) / (frames_to_extract - 1)) + 1
            v.set(cv2.CAP_PROP_POS_FRAMES, frame_index - 1)
            ret, frame = v.read()
            if ret:
                extracted_frames.append(frame)
            else:
                print(f'Could not read frame {frame_index} from {video_path}')
        
        v.release()
        all_extracted_frames.extend(extracted_frames)
    
    # Combine extracted frames into one output video file
    os.makedirs(output_video_path, exist_ok=True)
    output_file_path = os.path.join(output_video_path, f'{output_file_name}.avi')
    
    fourcc = cv2.VideoWriter_fourcc(*'UNCOMPRESSED')
    out = cv2.VideoWriter(output_file_path, fourcc, 30, 
                           (all_extracted_frames[0].shape[1], all_extracted_frames[0].shape[0]))
    
    for frame in all_extracted_frames:
        out.write(frame)
    
    out.release()
    print(f'Combined and saved all extracted frames to {output_file_path}')

# Example usage
if __name__ == "__main__":
    input_videos = [
        "path/to/video1.avi",
        "path/to/video2.avi",
        # Add more video paths
    ]
    output_path = "path/to/output/directory"
    output_name = "Body_Pose_Concat_p2"
    
    concat_frames(input_videos, output_path, output_name)