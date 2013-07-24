%%%% Hello world! Little tiny plotting function.
% With Love, Annas
function cleanplot(task)

%% Data PreLims

dataorg(data,eyedata,task,trialvec);


%% Oddball

if strcmp(task,'oddball')==1

% Explanations %
%%% chopmat_odd = matrix of chopped data per each sound trial (to be
% layered.
%%% normavg = matrix with columns containing chopped data from chopmat_odd
% (for left eye currently) for normal sounds only
%%% oddavg = same as normavg but for odd sounds.

oddplot = plotoddrev(outdat,trialvec,srtbins,testdata);


%% Reversal Learning
elseif strcmp(task,'revlearn')==1

trialvec = [data.correct];
revplot = plotoddrev(outdat,trialvec,srtbins,testdata);

%% Light Dark Test
elseif strcmp(task, 'darktest') | strcmp(task, 'lighttest')==1;
plotlightdark(srtbins,testdata,outdat);

end
end