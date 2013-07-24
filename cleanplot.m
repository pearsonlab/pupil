%%%% Hello world! Little tiny plotting function.
% With Love, Annas
function cleanplot(filename)

load(filename);

%% Adjust for cases
if strcmp(task,'revlearn')==1
    trialvec = [data.correct];
elseif strcmp(task, 'darktest') | strcmp(task, 'lighttest')==1
    trialvec=[];
end
    

%% Data PreLims
[outdat,trialvec,srtbins,testdata] = dataorg(data,eyedata,task,trialvec);


%% Oddball

if strcmp(task,'oddball')==1
    
    plotoddrev(outdat,trialvec,srtbins,testdata);
    
%% Reversal Learning
    
    
elseif strcmp(task,'revlearn')==1
    
    plotoddrev(outdat,trialvec,srtbins,testdata);
    
    %% Light Dark Test
elseif strcmp(task, 'darktest') | strcmp(task, 'lighttest')==1;
    plotlightdark(srtbins,testdata,outdat);
    
end
end