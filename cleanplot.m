%%%% Hello world! Little tiny plotting function.
% With Love, Annas
function cleanplot(filename)
%% Explanations
%%% datamat = 3-column matrix vertcatting lefteye(1), righteye(2), and
% timestamp(3)

%%

%figure out how to add path of file.
%load(filename);
%[pathstr, name] = fileparts(filename);


%% Data Cleaning PreLims
dataorg;

% case pst

% Plot the average of the left and right pupil - raw data.
a1=axes;
pst=plot((datamat(:,1)+(datamat(:,2)))/2, 'Color', 'g');
%linspace(0,duration,length(datamat));
xlabel('Time(sec)')
ylabel('Pupil size(mm)') % is it in mm?
hold on

% Plot the average of the left and right pupil - raw data.
plot((datamat(:,1)+(datamat(:,2)))/2, 'Color', 'g');
hold on


%% Oddball

% Explanations %
%%% chopmat_odd = matrix of chopped data per each sound trial (to be
% layered.
%%% normavg = matrix with columns containing chopped data from chopmat_odd
% (for left eye currently) for normal sounds only
%%% oddavg = same as normavg but for odd sounds.
dataorg;

%%%%%%
%
%         % Find timebins where any sound occurred, including normal and odd.
%         for ind=1:length(data); % 1:25
%             for i=1:length(datamat); %1:6499
%                 tofindbins(i,ind)=data(ind).soundtime-datamat(i,3);
% 
%                 % Find the timestamp bin corresponding time of sound
%                 %stimulus.
%                 [n timebin(ind)]=min(abs(tofindbins(:,ind)));
% 
%             end
%         end
%%%%%

% Extract oddball data.
oddavg = chopmat(:,logical(trialvec));
sizeo = size(oddavg);
normavg = chopmat(:,(find(trialvec==0)));
sizen = size(normavg);

% Plot vertical lines for normal (blue) vs. odd sounds (red) on figure 1.

for i = 1:length(trialvec)
    if trialvec(i) == 0
        line([bb(i) bb(i)],[min(testdata.lefteye(:,12)-0.25) max(testdata.lefteye(:,12)+0.25)]);
    else
        y = line([bb(i) bb(i)],[min(testdata.lefteye(:,12)-0.25) max(testdata.lefteye(:,12)+0.25)]);
        set(y, 'Color', 'r');
    end
end

% Average normal and oddball lefteye data and then plot on new figure

normavg(normavg == 0) = NaN;
oddavg(oddavg == 0) = NaN;

for i=1:length(normavg)
    plot2odd(i,1) = nanmean(normavg(i,:));
    plot2odd(i,2) = nanmean(oddavg(i,:));
    plot2odd(i,3) = nanstd(normavg(i,:))/sizen(2);
    plot2odd(i,4) = nanstd(oddavg(i,:))/sizeo(2);
end

figure;
plot(plot2odd(:,1:2));
hold on
plot(plot2odd(:,3:4),'--');


%% Reversal Learning
%elseif strfind(name,'revlearn')
for i=1:length(data);
    mtrials(i)=data(i).correct==0;
end
mispos=find(mtrials==1);
corpos=find(mtrials~=1);
%%fourth column in datamat is now average of left and right eye
datamat(:,4)=(datamat(:,1)+(datamat(:,2)))/2;
%%this finds the eyedata for the incorrect trials
for q=1:length(mispos);
    for z=1:length(datamat);
        ze(z,q)=data(mispos(q)).soundtime-datamat(z,3);
    end
    [num pos(q)]=min(abs(ze(:,q)));
end

revlearnmat=datamat((pos(q)-120):(pos(q)+120),4); %%since the tracker takes stamps at a rate of 60Hz this finds a second before the stimulus onset and 2 seconds after

%this plots the eye data for the trials that were correct
for w=1:length(corpos);
    for z=1:length(datamat);
        ze(z,w)=data(corpos(w)).soundtime-datamat(z,3);
    end
    [num correctpos(w)]=min(abs(ze(:,w)));
end
revlearnmat(:,2)=datamat((correctpos(w)-120):(correctpos(w)+120),4);
plot(revlearnmat);
hleg1 = legend('Incorrect Trials','Correct Trials');

%% Light Dark Test
% elseif strfind(name,'darktest') | strfind(name,'lighttest');
for i = 1:length(bb)
    line([bb(i) bb(i)],[min(testdata.lefteye(:,12)-0.25) max(testdata.lefteye(:,12)+0.25)]);
end
% hleg1 = legend('First Stimulus','Second Stimulus', 'Third Stimulus');

figure;
plot(chopmat(:,1:2));

end