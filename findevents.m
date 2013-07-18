%%%finding vectors of events
ts = eyedata.timestamp;
if strcmp(task, 'revlearn')==1 | strcmp(task, 'oddball')==1;
    stimulustime=[data.soundtime];
    if strcmp(task, 'revlearn')==1
    correctspots = [data.correct];
    end
elseif strcmp(task, 'darktest') | strcmp(task, 'lighttest')==1;
    stimlustime=[data.offtime]-[data.ontime]
end



    for i=1:length(stimulustime)
    %if correctspots(i)==1
    [~,evtbins(i)] = min(abs(uint64(stimulustime(i))-uint64(ts)));
    %else
    %[~,incorsoundbins(i)] = min(abs(uint64(stimulustime(i))-uint64(ts)));
    end
 
    

