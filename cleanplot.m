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
if ~exist('task')
    testdata=data;
else
    testdata=eyedata;
end

% Replace bad eye data with NaN (Column 13 values of either -1 or 4 are
%bad).
testdata.lefteye(testdata.lefteye(:,13)~=0,12) = NaN;
testdata.righteye(testdata.righteye(:,13)~=0,12) = NaN;



%make into seconds
testerdata.timestamp=(double(eyedata.timestamp))/1000000


% Create a matrix the size of longest eyedata to combine left, right,
% and timestamp data into 3 columns in 1 matrix, called datamat.
datamat = repmat((NaN), length(testdata.lefteye),3);
datamat(:,1)=testdata.lefteye(:,12);
datamat(:,2)=testdata.righteye(:,12);
datamat(:,3)=testdata.timestamp;

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

chopmat_odd = [];
normavg = [];
oddavg = [];

% Fourth column in datamat is now average of left and right eye
datamat(:,4)=(datamat(:,1)+(datamat(:,2)))/2;

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
%%%%%%

% Find timebins where any sound occurred, including normal and odd.
st = [data.soundtime];
ts = eyedata.timestamp;

for i=1:length(st)
    tt = st(i);
    [~,bb(i)] = min(abs(uint64(tt)-uint64(ts)));
end
% Note - bb gives different bins than timebin by +1 bin.


% Create matrix of chopped data - each column contains
% eye data from 60 bins (1 sec) before through 120 bins after the sound time
% bin of that particular trial.

% Use evtsplit as better way to make chopmat -

for ind = 1:length(data)
    chopmat_odd(:,ind) = datamat((bb(ind)-60):(bb(ind)+120),1);
end

% Extract oddball data.
oddavg = chopmat_odd(:,logical(trialvec));
normavg = chopmat_odd(:,(find(trialvec==0)));

% Plot vertical lines for normal (blue) vs. odd sounds (red) on figure 1.
for i = length(trialvec)
    if trialvec(i) == 0
        line([bb(i) bb(i)],[(min(eyedata.lefteye(:,12))-0.5) max(eyedata.lefteye(:,12)+0.5)]);
        hold on
    else
        line([bb(i) timebin(i)],[(min(eyedata.lefteye(:,12))-0.5) max(eyedata.lefteye(:,12)+0.5)]);
        set(y, 'Color', 'r');
    end
end

% Average normal and oddball lefteye data and then plot on new figure

normavg(normavg == 0) = NaN;
oddavg(oddavg == 0) = NaN;

for i=1:length(normavg)
    plot2odd(i,1) = nanmean(normavg(i,:));
    plot2odd(i,2) = nanmean(oddavg(i,:));
end
figure;
plot(plot2odd);

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
elseif strfind(name,'darktest') | strfind(name,'lighttest')
    
    chopmat=[];
    
    %%this spits out the bins that contain the position of each onset of the
    %%stimulus
    for ind = 1:length(data);
        for i=1:length(datamat);
            differenceontime(i)=data(ind).ontime-(datamat(i,3));
        end
        [n onbin(ind)]=min(abs(differenceontime));
        %%since the tracker takes stamps at a rate of 60Hz this finds a second before the stimulus onset and 2 seconds after
        
        chopmat(:,ind+3)=datamat((onbin(ind)-60):(onbin(ind)+120),2);
    end
    
    
    chopmat(:,7)=(chopmat(:,1)+chopmat(:,4)/2); %these are the average of left and right eye
    chopmat(:,8)=(chopmat(:,2)+chopmat(:,5)/2);
    chopmat(:,9)=(chopmat(:,3)+chopmat(:,6)/2);
    plot(chopmat(:,7:9));
    hleg1 = legend('First Stimulus','Second Stimulus', 'Third Stimulus');
end