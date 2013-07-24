%%%%% This function organizes data.

% function dataorg(filename)

if ~exist('task')
    testdata=data;
else
    testdata=eyedata;
end

% Find either sound or onscreen stimuli onset bins.
[~,srtbins] = findevents(testdata,data,task);

% Make matrix of L, R, timestamp, avg. L and R
[datamat] = makemat(testdata);

% Convert datamat time --> seconds.
[datamat] = makesecs(datamat);

% Plot raw data (avg. right and left eye)
figure1 = plotraw(datamat);

% Find # bins before/after, make matrix of chopped data called 'outdat'
[npre,npost,nnorm,outdat] = evtsplit(srtbins,1,2,60,task,0.2,datamat);

% end