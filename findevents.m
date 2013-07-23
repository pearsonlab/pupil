%%%finding vectors of events
function [timestamp, srtbins,correctspots]=findevents(eyedata,data,task)
timestamp = eyedata.timestamp;

if strcmp(task, 'revlearn')==1 | strcmp(task, 'oddball')==1;
    stimon=[data.soundtime];
    if strcmp(task, 'revlearn')==1
    correctspots = [data.correct];
    end
elseif strcmp(task, 'darktest') | strcmp(task, 'lighttest')==1;
    stimon=[data.ontime];
    stimoff=[data.offtime];
    
end

for i=1:length(stimon)
    % find bins corresponding to sound or screen stimulus onset.
    [~,srtbins(i)] = min(abs(uint64(stimon(i))-uint64(timestamp)));
    %[~,stpbins(i)] = min(abs(uint64(stimoff(i))-uint64(ts)));
end

