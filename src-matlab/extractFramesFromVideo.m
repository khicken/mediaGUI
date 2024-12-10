function extractFramesFromVideo(videoFilePath, outputFolder, numFramesToExtract)
    % Check if the number of input arguments is correct
    if nargin < 3
        error('Not enough input arguments. Please provide the video file path, output folder path, and number of frames to extract.');
    end

    % Create a VideoReader object
    vidObj = VideoReader(videoFilePath);

    % Determine the total number of frames in the video
    totalFrames = vidObj.NumFrames;

    % Print the total number of frames in the video
    fprintf('Total number of frames in the video: %d\n', totalFrames);

    % Determine the indices of frames to extract
    indices = round(linspace(1, totalFrames, numFramesToExtract));

    % Calculate the new naming indices based on iteration steps
    iterationValues = Iteration_Steps(totalFrames, numFramesToExtract);

    % Preallocate cell array to store extracted frames
    extractedFrames = cell(1, numFramesToExtract);

    % Create output folder if it doesn't exist
    if ~exist(outputFolder, 'dir')
        mkdir(outputFolder);
    end

    % Extract frames
    for i = 1:numFramesToExtract
        frameIndex = indices(i);
        vidObj.CurrentTime = (frameIndex - 1) / vidObj.FrameRate;
        extractedFrames{i} = readFrame(vidObj);
    end

    % Save extracted frames as individual images with new naming convention
    for i = 1:numFramesToExtract
        imageName = sprintf('img%05d.png', iterationValues(i));
        imwrite(extractedFrames{i}, fullfile(outputFolder, imageName));
    end

    disp('Frames extracted and saved successfully.');
end

function the_iteration_values = Iteration_Steps(total_frames, labeled_frames)
    % Find iteration step size using recursion. Divide by -1 of inputted labeled frames value
    % because we always extract frame 0.
    step_size = (total_frames-1)/(labeled_frames-1);
    iteration_values = zeros(labeled_frames, 1); % Initialize with zeros

    for i = 1:labeled_frames
        iteration_values(i) = round((i - 1) * step_size);
    end

    the_iteration_values = iteration_values;
end

