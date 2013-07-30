%%%% Hello world! Little tiny plotting function.
% With Love, Annas

% Plots graph of averaged raw data 
function cleanplot(filename)

load(filename);

%% Adjust for cases
if strcmp(task,'revlearn')==1
    trialvec = [data.correct];
elseif strcmp(task, 'darktest') | strcmp(task, 'lighttest')==1
    trialvec=[];
end
    
% Right now we have to define twoeye, whicheye, and norm prior to running
% dataorg.

% twoeye = 1(plots both right and left eye); 0(plots only whatever we input
% in whicheye)
% whicheye = 1(left eye), 2(right eye), 4(avg.)
% norm = 1: normalizes. 

twoeye=0;
whicheye=4;
norm=1;

%% Data PreLims
[outdat,outdat2,trialvec,srtbins,testdata,whicheye,datamat] = dataorg(data,eyedata,task,trialvec,whicheye,twoeye,norm);
hold on

%% Oddball

if strcmp(task,'oddball')==1
    
    plotoddrev(outdat,outdat2,trialvec,srtbins,testdata,task,twoeye);
    
%% Reversal Learning
    
    
elseif strcmp(task,'revlearn')==1
    
    plotoddrev(outdat,trialvec,srtbins,testdata);
    
    %% Light Dark Test
elseif strcmp(task, 'darktest') | strcmp(task, 'lighttest')==1;
    plotlightdark(srtbins,testdata,outdat,outdat2,task,twoeye,datamat);
    
end
end