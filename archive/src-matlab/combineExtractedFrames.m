function combineExtractedFrames(inputVideoFiles, outputVideoPath, outputFileName)
    % Initialize variables
    framesToExtract = 330;
    allExtractedFrames = cell(1, numel(inputVideoFiles));
    numVideos = numel(inputVideoFiles);

    % Extract frames from each video file
    for vIndex = 1:numVideos
        v = VideoReader(inputVideoFiles{vIndex});
        numFrames = v.NumFrames;
        extractedFrames = zeros(v.Height, v.Width, 3, framesToExtract, 'uint8');

        % Extract frames evenly
        for i = 1:framesToExtract
            frameIndex = round((i - 1) * (numFrames - 1) / (framesToExtract - 1)) + 1;
            extractedFrames(:, :, :, i) = read(v, frameIndex);
        end

        allExtractedFrames{vIndex} = extractedFrames;
    end

    % Combine extracted frames into one output video file
    outputFilePath = fullfile(outputVideoPath, [outputFileName '.avi']);  % Ensure the output is an AVI file
    vWriter = VideoWriter(outputFilePath, 'Uncompressed AVI');  % Specify 'Uncompressed AVI' format
    open(vWriter);

    for vIndex = 1:numVideos
        extractedFrames = allExtractedFrames{vIndex};
        numFrames = size(extractedFrames, 4);
        for i = 1:numFrames
            writeVideo(vWriter, extractedFrames(:, :, :, i));
        end
    end

    close(vWriter);

    disp(['Combined and saved all extracted frames to ' outputFilePath]);
end
