%%%% Hello world! Little tiny plotting function.
% With Love, Annas
function cleanplot(filename)

%% Data PreLims
dataorg;

% case pst

% Plot the average of the left and right pupil - raw data.
a1=axes;
pst=plot((datamat(:,1)+(datamat(:,2)))/2, 'Color', 'g');
%linspace(0,duration,length(datamat));
xlabel('Time(sec)')
ylabel('Pupil size(mm)') % is it in mm?
hold on

%% Oddball

% Explanations %
%%% chopmat_odd = matrix of chopped data per each sound trial (to be
% layered.
%%% normavg = matrix with columns containing chopped data from chopmat_odd
% (for left eye currently) for normal sounds only
%%% oddavg = same as normavg but for odd sounds.

oddplot = plotoddrev(chopmat,trialvec,srtbins,testdata);


%% Reversal Learning
%elseif strfind(name,'revlearn')

trialvec = [data.correct];

revplot = plotoddrev(chopmat,trialvec,srtbins,testdata);

%% Light Dark Test
% elseif strfind(name,'darktest') | strfind(name,'lighttest');
plotlightdark(srtbins,testdata,chopmat);

end