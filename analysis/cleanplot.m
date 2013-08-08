%%%% Hello world! Little tiny plotting function.
% With Love, Annas

function cleanplot(filename,plotwhat)
% 
% This function is skeleton function for plotting graphs of data.
% Input filename such as: '0.2.oddball.pupiltest.mat' (include quotes)
% Input plotwhat as
% 'left','right','average','leftnorm','rightnorm','averagenorm' (include
% quotes). plotwhat tells cleanplot which chopped data to plot in the
% overlaid graph. It also controls what raw data is plotted. 

load(filename);

%% Case PST
if ~exist('task')
    testdata = data;
    [datamat] = makemat(testdata);
    twoeye=0;
    plotraw(datamat,plotwhat);
else
%% Adjust for cases
if strcmp(task,'revlearn')==1
    trialvec = [data.correct];
    % Organize trialvec so it 1 corresponds with incorrect response
    trialvec=trialvec-1;
    trialvec(find(trialvec==-1))=1;
elseif strcmp(task, 'darktest') | strcmp(task, 'lighttest')==1 | strcmp(task,'pst')==1
    trialvec=[];
end

%% Data PreLims
[outdat,trialvec,srtbins,testdata,datamat] = dataorg(data,eyedata,task,trialvec);
hold on

%% Plot Raw Data Sequentially
% Plot raw data (which data depends on your plotwhat)
twoeye=0;
plotraw(datamat,plotwhat);

%% Plot Overlaid Data
% Case Oddball or Reversal Learning

if strcmp(task,'oddball')==1 | strcmp(task,'revlearn')==1
    
    plotoddrev(outdat,trialvec,srtbins,testdata,task,plotwhat);
    
    
% Case Light Dark Test
elseif strcmp(task, 'darktest') | strcmp(task, 'lighttest')==1;
    plotlightdark(srtbins,testdata,outdat,task,twoeye,datamat,plotwhat);
    
end
end

end