%%% Makes "datamat," matrix of vertically concatenated eye/timestamp data
% 4 columns, same length: left, right, timestamp, avg. right and left

function [datamat] = makemat(testdata)

% Replace bad eye data with NaN (Column 13 values of either -1 or 4 are
    %bad).
    testdata.lefteye(testdata.lefteye(:,13)~=0,12) = NaN;
    testdata.righteye(testdata.righteye(:,13)~=0,12) = NaN;
    
      % Create a matrix the size of longest eyedata to combine left, right,
    % and timestamp data into 3 columns in 1 matrix, called datamat.
    datamat = repmat((NaN), length(testdata.lefteye),3);
    datamat(:,1)=testdata.lefteye(:,12);
    datamat(:,2)=testdata.righteye(:,12);
    datamat(:,3)=testdata.timestamp;
    
      % Fourth column in datamat is now average of left and right eye
    datamat(:,4)=(datamat(:,1)+(datamat(:,2)))/2;
end