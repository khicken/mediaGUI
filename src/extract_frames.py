import os
import cv2
import numpy as np

def iteration_steps(total_frames, labeled_frames):
    """
    Calculate iteration steps for frame extraction.
    
    Args:
        total_frames (int): Total number of frames in the video
        labeled_frames (int): Number of frames to extract
    
    Returns:
        numpy.ndarray: Array of frame indices to extract
    """
    step_size = (total_frames - 1) / (labeled_frames - 1)
    iteration_values = [round((i - 1) * step_size) for i in range(1, labeled_frames + 1)]
    return iteration_values

def extract_frames_from_video(video_file_path, output_folder, num_frames_to_extract):
    """
    Extract evenly distributed frames from a video.
    
    Args:
        video_file_path (str): Path to the input video file
        output_folder (str): Directory to save extracted frames
        num_frames_to_extract (int): Number of frames to extract
    """
    # Open video capture
    vid_obj = cv2.VideoCapture(video_file_path)
    
    # Get total number of frames
    total_frames = int(vid_obj.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = vid_obj.get(cv2.CAP_PROP_FPS)
    
    print(f'Total number of frames in the video: {total_frames}')
    
    # Determine frame indices to extract
    indices = np.round(np.linspace(1, total_frames, num_frames_to_extract)).astype(int)
    
    # Calculate iteration values
    iteration_values = iteration_steps(total_frames, num_frames_to_extract)
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Extract and save frames
    for i, (frame_index, iteration_value) in enumerate(zip(indices, iteration_values), 1):
        vid_obj.set(cv2.CAP_PROP_POS_FRAMES, frame_index - 1)
        ret, frame = vid_obj.read()
        
        if ret:
            image_name = os.path.join(output_folder, f'img{iteration_value:05d}.png')
            cv2.imwrite(image_name, frame)
        else:
            print(f'Could not read frame {frame_index}')
    
    vid_obj.release()
    print('Frames extracted and saved successfully.')

# Example usage
if __name__ == "__main__":
    video_path = "path/to/your/video.avi"
    output_dir = "path/to/output/folder"
    num_frames = 180
    
    extract_frames_from_video(video_path, output_dir, num_frames)