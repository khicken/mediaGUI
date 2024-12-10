% Extract Desired images

videoFilePath = "C:\Users\OZDEMIK2\Desktop\Body_Pose_Supermodel_v2-Kemal-2024-12-08\videos\Body_Pose_Supermodel.avi";
outputFolder = "C:\Users\OZDEMIK2\Desktop\Body_Pose_Supermodel_v2-Kemal-2024-12-08\labeled-data\Body_Pose_Supermodel";
numFramesToExtract = 180;

extractFramesFromVideo(videoFilePath, outputFolder, numFramesToExtract);

