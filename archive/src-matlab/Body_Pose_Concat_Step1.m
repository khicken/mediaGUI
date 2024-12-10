clc
clear
close all

% Body Pose Supermodel Concatenation
    % Insert the desired videos
    inputVideoFiles = {
"I:\data\LRI-110044\Sep24\090224_TC\GBM_group2_baseline1\132\processed data\body\132_body_concat.avi"
"I:\data\LRI-110044\Sep24\090224_TC\GBM_group2_baseline1\235\processed data\body\235_body_concat.avi"
"I:\data\LRI-110044\Sep24\090224_TC\GBM_group2_baseline1\244\processed data\body\244_body_concat.avi"
"I:\data\LRI-110044\Sep24\090224_TC\GBM_group2_baseline1\264\processed data\body\264_body_concat.avi"
"I:\data\LRI-110044\Sep24\090224_TC\GBM_group2_baseline1\321\processed data\body\321_body_concatnew.avi"
"I:\data\LRI-110044\Sep24\090324_FB\GBM_Group2_Baseline1_3animals\Animal 314\processed data\body\314_body_concat.avi"
"I:\data\LRI-110044\Sep24\090324_FB\GBM_Group2_Baseline1_3animals\Animal 335\processed data\body\335_body_concat.avi"
"I:\data\LRI-110044\Sep24\090324_FB\GBM_Group2_Baseline1_3animals\Animal 380\processed data\body\380_body_concat.avi"
"I:\data\LRI-110044\Sep24\090324_TC\GBM_Group2_baseline2\132\processed data\body\132_body_concat.avi"
"I:\data\LRI-110044\Sep24\090324_TC\GBM_Group2_baseline2\235\processed data\body\235_body_concat.avi"
"I:\data\LRI-110044\Sep24\090324_TC\GBM_Group2_baseline2\244\processed data\body\244_body_concat.avi"
"I:\data\LRI-110044\Sep24\090324_TC\GBM_Group2_baseline2\264\processed data\body\264_body_concat.avi"
"I:\data\LRI-110044\Sep24\090324_TC\GBM_Group2_baseline2\321\processed data\body\321_body_concat.avi"
"I:\data\LRI-110044\Sep24\090424_TC\GBM_Baseline_session2_group2_3ani\314\processed data\body\314_body_concat.avi"
"I:\data\LRI-110044\Sep24\090424_TC\GBM_Baseline_session2_group2_3ani\335\processed data\body\335_body_concat.avi"
"I:\data\LRI-110044\Sep24\090424_TC\GBM_Baseline_session2_group2_3ani\380\processed data\body\380_body_concat.avi"
"I:\data\LRI-110044\Sep24\090424_TC\GBM_Baseline_session3_group2\132\processed data\body\132_body_concat.avi"
"I:\data\LRI-110044\Sep24\090424_TC\GBM_Baseline_session3_group2\235\processed data\body\235_body_concatnew.avi"
"I:\data\LRI-110044\Sep24\090424_TC\GBM_Baseline_session3_group2\244\processed data\body\244_body_concat.avi"
"I:\data\LRI-110044\Sep24\090424_TC\GBM_Baseline_session3_group2\264\processed data\body\264_body_concat.avi"
"I:\data\LRI-110044\Sep24\090424_TC\GBM_Baseline_session3_group2\314\processed data\body\314_body_concat.avi"
"I:\data\LRI-110044\Sep24\090424_TC\GBM_Baseline_session3_group2\321\processed data\body\321_body_concat.avi"
"I:\data\LRI-110044\Sep24\090424_TC\GBM_Baseline_session3_group2\335\processed data\body\335_body_concat.avi"
"I:\data\LRI-110044\Sep24\090424_TC\GBM_Baseline_session3_group2\380\processed data\body\380_body_concat.avi"
"I:\data\LRI-110044\Sep24\090524_FB\GBM_BaselineSess4_group2_3ani\Animal 314\Processed data\Body\314_body_concat.avi"
"I:\data\LRI-110044\Sep24\090524_FB\GBM_BaselineSess4_group2_3ani\Animal 335\Processed Data\Body\335_body_concat.avi"
"I:\data\LRI-110044\Sep24\090524_FB\GBM_BaselineSess4_group2_3ani\Animal 380\processed data\Body\380_body_concat.avi"
"I:\data\LRI-110044\Sep24\090524_TC\GBM_Baseline_sess4_group2\132\processed data\body\132_body_concat.avi"
"I:\data\LRI-110044\Sep24\090524_TC\GBM_Baseline_sess4_group2\235\processed data\body\235_body_concat.avi"
"I:\data\LRI-110044\Sep24\090524_TC\GBM_Baseline_sess4_group2\244\processed data\body\244_body_concat.avi"
"I:\data\LRI-110044\Sep24\090524_TC\GBM_Baseline_sess4_group2\264\processed data\body\264_body_concat.avi"
"I:\data\LRI-110044\Sep24\090524_TC\GBM_Baseline_sess4_group2\321\processed data\body\321_body_concat.avi"
"I:\data\LRI-110044\Sep24\090624_TC\GBM_Group2_Baseline_Sess5\132\processed data\body\132_body_concat.avi"
"I:\data\LRI-110044\Sep24\090624_TC\GBM_Group2_Baseline_Sess5\235\processed data\body\235_body_concat.avi"
"I:\data\LRI-110044\Sep24\090624_TC\GBM_Group2_Baseline_Sess5\244\processed data\body\244_body_concat.avi"
"I:\data\LRI-110044\Sep24\090624_TC\GBM_Group2_Baseline_Sess5\264\processed data\body\264_body_concat.avi"
"I:\data\LRI-110044\Sep24\090624_TC\GBM_Group2_Baseline_Sess5\314\processed data\body\314_body_concat.avi"
"I:\data\LRI-110044\Sep24\090624_TC\GBM_Group2_Baseline_Sess5\321\processed data\body\321_body_concat.avi"
"I:\data\LRI-110044\Sep24\090624_TC\GBM_Group2_Baseline_Sess5\335\processed data\body\335_body_concat.avi"
"I:\data\LRI-110044\Sep24\090624_TC\GBM_Group2_Baseline_Sess5\380\processed data\body\380_body_concat.avi"
"I:\data\LRI-110044\Sep24\090624_TC\GBM_Group2_Baseline_Sess6\132\processed data\body\132_body_concat.avi"
"I:\data\LRI-110044\Sep24\090624_TC\GBM_Group2_Baseline_Sess6\235\processed data\body\235_body_concat.avi"
"I:\data\LRI-110044\Sep24\090624_TC\GBM_Group2_Baseline_Sess6\244\processed data\body\244_body_concat.avi"
"I:\data\LRI-110044\Sep24\090624_TC\GBM_Group2_Baseline_Sess6\264\processed data\body\264_body_concat.avi"
"I:\data\LRI-110044\Sep24\090624_TC\GBM_Group2_Baseline_Sess6\314\processed data\body\314_body_concat.avi"
"I:\data\LRI-110044\Sep24\090624_TC\GBM_Group2_Baseline_Sess6\321\processed data\body\321_body_concat.avi"
"I:\data\LRI-110044\Sep24\090624_TC\GBM_Group2_Baseline_Sess6\335\processed data\body\335_body_concat.avi"
"I:\data\LRI-110044\Sep24\090624_TC\GBM_Group2_Baseline_Sess6\380\processed data\body\380_body_concat.avi"
"I:\data\LRI-110044\Oct24\100224_FB\GBM_Group3_Baseline1_40Hz\Animal 316\processed data\Body\316_body_concat.avi"
"I:\data\LRI-110044\Oct24\100324_FB\GBM_Group3_Baseline2\Animal 316\processed data\Body\316_body_concat.avi"
"I:\data\LRI-110044\Oct24\100424_FB\GBM_Group3_Baseline3_40Hz\Animal 316\processed data\body\316_body_concat.avi"
"I:\data\LRI-110044\Oct24\100724_FB\GBM_Group3_Baseline4_40Hz\Animal 316\processed data\Body\316_body_concat.avi"
"I:\data\LRI-110044\Oct24\100824_TC\GBM_Group3_Baseline3_100Hz\316\processed data\body\316_body_concat.avi"
"I:\data\LRI-110044\Oct24\100824_FB\GBM_Group3_Baseline5\Animal 316\processed data\body\316_body_concat.avi"
    };
    
    % Specify the Directory of the Output Video for Initial Concatenation
    outputVideoPath = "I:\Protocols\Body_Pose_Model_v2\Baseline_2_3";
    outputFileName = 'Body_Pose_Concat_p2';
    combineExtractedFrames(inputVideoFiles, outputVideoPath, outputFileName)
