%%%%% This function organizes data.

function dataorg(filename)

if ~exist('task')
    testdata=data;
else
    testdata=eyedata;
end

% Replace bad eye data with NaN (Column 13 values of either -1 or 4 are
%bad).
testdata.lefteye(testdata.lefteye(:,13)~=0,12) = NaN;
testdata.righteye(testdata.righteye(:,13)~=0,12) = NaN;

%make into seconds
testerdata.timestamp=(double(eyedata.timestamp))/1000000


% Create a matrix the size of longest eyedata to combine left, right,
% and timestamp data into 3 columns in 1 matrix, called datamat.
datamat = repmat((NaN), length(testdata.lefteye),3);
datamat(:,1)=testdata.lefteye(:,12);
datamat(:,2)=testdata.righteye(:,12);
datamat(:,3)=testdata.timestamp;

% Plot the average of the left and right pupil - raw data.
plot((datamat(:,1)+(datamat(:,2)))/2, 'Color', 'g');
hold on

% Fourth column in datamat is now average of left and right eye
datamat(:,4)=(datamat(:,1)+(datamat(:,2)))/2;

chopmat = [];

% Find timebins where any stimulus occurred.
st = [data.soundtime];
ts = eyedata.timestamp;

for i=1:length(st)
    tt = st(i);
    [~,bb(i)] = min(abs(uint64(tt)-uint64(ts)));
end

% Evt split?
for ind = 1:length(data)
    chopmat_odd(:,ind) = datamat((bb(ind)-60):(bb(ind)+120),4);
end

end