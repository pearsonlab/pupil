%%%% Hello world! Little tiny plotting function.
% With Love, Annas

function cleanplot(filename)
% Input filename such as: '0.2.oddball.pupiltest.mat' (include quotes)
% This function is skeleton function for plotting graphs of data.

load(filename);

%% Adjust for cases
if strcmp(task,'revlearn')==1
    trialvec = [data.correct];
    % Organize trialvec so it 1 corresponds with incorrect response
    trialvec=trialvec-1;
    trialvec(find(trialvec==-1))=1;
elseif strcmp(task, 'darktest') | strcmp(task, 'lighttest')==1
    trialvec=[];
end

%% Data PreLims
[outdat,trialvec,srtbins,testdata,datamat] = dataorg(data,eyedata,task,trialvec);
hold on

%% Plot Raw Data Sequentially
% Plot raw data (avg. right and left eye)
% twoeye = 1(plots both right and left eye); 0(plots only whatever we input
% in whicheye)
% whicheye = 1(left), 2(right), 4(average of left and right)
twoeye=0;
whicheye=4;
plotraw(datamat,whicheye,twoeye);

%% Plot Overlaid Data
% Case Oddball or Reversal Learning

if strcmp(task,'oddball')==1 | strcmp(task,'revlearn')==1
    
    plotoddrev(outdat,trialvec,srtbins,testdata,task,twoeye,'averagenorm');
    
    
% Case Light Dark Test
elseif strcmp(task, 'darktest') | strcmp(task, 'lighttest')==1;
    plotlightdark(srtbins,testdata,outdat,task,twoeye,datamat,'averagenorm');
    
end
end