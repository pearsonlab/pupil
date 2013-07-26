%%%%% This function organizes data.

function [outdat,outdat2,trialvec,srtbins,testdata,whicheye] = dataorg(data,testdata,task,trialvec,whicheye,twoeye,norm)

% Find either sound or onscreen stimuli onset bins.
[~,srtbins] = findevents(testdata,data,task);

% Make matrix of L, R, timestamp, avg. L and R
[datamat] = makemat(testdata);

% Convert datamat time --> seconds.
[datamat] = makesecs(datamat);

% Find # bins before/after, make matrix of chopped data called 'outdat'
[outdat,outdat2,whicheye] = evtsplit(srtbins,task,datamat,whicheye,twoeye,norm);

% Plot raw data (avg. right and left eye)
plotraw(datamat,whicheye,twoeye);

end