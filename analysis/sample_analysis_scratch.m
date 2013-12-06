% scratchpad for working out some sample plots of behavior

%% setup paths
addpath('~/code/pupil/analysis')
addpath('~/code/pupil/analysis/utils')
addpath('~/code/electrophysiology')
ddir = '~/Dropbox/pupil/data/';

%% load data
[dfile, newdir, was_success] = uigetfile([ddir '*.mat']);

%% prepare data
if was_success
    prepdata
else
    warning('You must select a valid file!');
end

%% try some plotting
offtimes = us2secs([data.offtime], t0);

tpre = -0.3;
tpost = 8;
[pmat, binT] = evtsplit(pupil, offtimes, tpre, tpost, sr);

% baseline normalize
pmat = basenorm(pmat, binT, [-inf 0]);

plot(binT, pmat', 'linewidth', 2.0)
xlim([tpre tpost])
title('Pupillary light reflex','fontsize', 20, 'fontweight', 'bold')
xlabel('Time from flash (seconds)', 'fontsize', 16, 'fontweight', 'bold')
ylabel('Normalized pupil size (arb units)', 'fontsize', 16, 'fontweight', 'bold')
legend({'.25', '.50', '.75', '1.00'}, 'location', 'southeast')

%% load data
dfile = '0.1.revlearn.pupiltest.mat';
load(fullfile(ddir, dfile))

%% munge data
lpup = cleanseries(eyedata.lefteye(:, 12));
rpup = cleanseries(eyedata.righteye(:, 12));
mpup = nanmean([lpup; rpup]);
pupil = mpup;

% get timestamps: convert microseconds to seconds
t0 = min(eyedata.timestamp);
taxis = (eyedata.timestamp - t0)/1e6;  
sr = 60;  % sampling rate of Tobii = 60 Hz

%% try some plotting
etimes = double(uint64([data.soundtime]) - t0)/1e6;
wascorr = logical([data.correct]);
tpre = -0.3;
tpost = 8;
[pmat, binT] = evtsplit(pupil, etimes, tpre, tpost, sr);

% separate by pupil following correct vs incorrect responses
ppmat(1, :) = nanmean(pmat(wascorr, :));
ppmat(2, :) = nanmean(pmat(~wascorr, :));
pmat = ppmat;

% baseline normalize
zbin = find(binT == 0);
normalizer = nanmean(pmat(:, 1:(zbin - 1)), 2);
pmat = bsxfun(@minus, pmat, normalizer);

plot(binT, pmat', 'linewidth', 2.0)
xlim([tpre tpost])
title('Pupillary response to negative feedback','fontsize', 20, 'fontweight', 'bold')
xlabel('Time from buzzer (seconds)', 'fontsize', 16, 'fontweight', 'bold')
ylabel('Normalized pupil size (arb units)', 'fontsize', 16, 'fontweight', 'bold')
legend({'Correct', 'Incorrect'}, 'location', 'southeast')