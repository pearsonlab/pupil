% analyze_darktest.m
% run analyses and make plots of darktest data

% sync to time of stimulus onset
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