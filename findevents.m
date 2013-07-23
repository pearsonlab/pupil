%%%finding vectors of events
ts = eyedata.timestamp;
if strcmp(task, 'revlearn')==1 | strcmp(task, 'oddball')==1;
    stimtime=[data.soundtime];
    if strcmp(task, 'revlearn')==1
    correctspots = [data.correct];
    end
elseif strcmp(task, 'darktest') | strcmp(task, 'lighttest')==1;
    stimon=[data.ontime];
    stimoff=[data.offtime];
    for i=1:length(stimon)
   
    [~,srtbins(i)] = min(abs(uint64(stimon(i))-uint64(ts)));
    [~,stpbins(i)] = min(abs(uint64(stimoff(i))-uint64(ts)));
    %else
    %[~,incorsoundbins(i)] = min(abs(uint64(stimulustime(i))-uint64(ts)));
    end
 
    
end
