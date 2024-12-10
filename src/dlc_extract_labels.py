import os
import cv2

video_file_path = r"C:\Users\OZDEMIK2\Desktop\Body_Pose_Supermodel_v2-Kemal-2024-12-08\videos\Body_Pose_Supermodel.avi"
output_folder = r"C:\Users\OZDEMIK2\Desktop\Body_Pose_Supermodel_v2-Kemal-2024-12-08\labeled-data\Body_Pose_Supermodel"

def extract_frames_from_video(video_file_path, output_folder, num_frames_to_extract):
    """
    Extract frames from a video for DeepLabCut labeling.
    
    Args:
        video_file_path (str): Path to the input video file
        output_folder (str): Directory to save extracted frames
        num_frames_to_extract (int): Number of frames to extract
    """
    # Open video capture
    vid_obj = cv2.VideoCapture(video_file_path)
    
    # Get total number of frames
    total_frames = int(vid_obj.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f'Total number of frames in the video: {total_frames}')
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Calculate frame indices to extract
    frame_indices = [int(i) for i in list(range(0, total_frames, total_frames // num_frames_to_extract))[:num_frames_to_extract]]
    
    # Extract and save frames
    for i, frame_index in enumerate(frame_indices, 1):
        vid_obj.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = vid_obj.read()
        
        if ret:
            # Save frame with zero-padded 5-digit naming convention
            image_name = os.path.join(output_folder, f'img{i-1:05d}.png')
            cv2.imwrite(image_name, frame)
        else:
            print(f'Could not read frame {frame_index}')
    
    vid_obj.release()
    print('Frames extracted and saved successfully.')

def main():
    num_frames_to_extract = 180
    
    extract_frames_from_video(video_file_path, output_folder, num_frames_to_extract)

if __name__ == "__main__":
    main()