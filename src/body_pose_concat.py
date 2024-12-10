import os
from concat_frames import concat_frames

def main():
    # Input video files
    input_video_files = [
        r"I:\data\LRI-110044\Sep24\090224_TC\GBM_group2_baseline1\132\processed data\body\132_body_concat.avi",
        r"I:\data\LRI-110044\Sep24\090224_TC\GBM_group2_baseline1\235\processed data\body\235_body_concat.avi",
        r"I:\data\LRI-110044\Sep24\090224_TC\GBM_group2_baseline1\244\processed data\body\244_body_concat.avi",
        r"I:\data\LRI-110044\Sep24\090224_TC\GBM_group2_baseline1\264\processed data\body\264_body_concat.avi",
        r"I:\data\LRI-110044\Sep24\090224_TC\GBM_group2_baseline1\321\processed data\body\321_body_concatnew.avi",
        # Add the rest of the input video files from the MATLAB script
        # ... (truncated for brevity)
        r"I:\data\LRI-110044\Oct24\100824_FB\GBM_Group3_Baseline5\Animal 316\processed data\body\316_body_concat.avi"
    ]
    
    # Specify the Directory of the Output Video for Initial Concatenation
    output_video_path = r"I:\Protocols\Body_Pose_Model_v2\Baseline_2_3"
    output_file_name = 'Body_Pose_Concat_p2'
    
    # Call the function to combine extracted frames
    concat_frames(input_video_files, output_video_path, output_file_name)

if __name__ == "__main__":
    main()