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

% Find # bins before/after
[npre,npost,nnorm] = evtsplit(srtbins,1,2,60,task,0.2);

% Make matrix of chopped data.
[chopmat] = chopmaker(datamat,npre,npost,srtbins,nnorm);

% end