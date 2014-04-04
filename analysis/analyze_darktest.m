% analyze_darktest.m
% run analyses and make plots of darktest data

% get instances when screen went black
offtimes = us2secs([data.ontime], t0);

tpre = -0.3;
tpost = 8;
[pmat, binT] = evtsplit(pupil, offtimes, tpre, tpost, sr);

% baseline normalize
pmat = basenorm(pmat, binT, [-inf 0], normtype);

plot(binT, pmat', 'linewidth', 2.0)
xlim([tpre tpost])
title('Pupillary dark reflex','fontsize', 20, 'fontweight', 'bold')
xlabel('Time from blank (seconds)', 'fontsize', 16, 'fontweight', 'bold')
ylabel('Normalized pupil size (arb units)', 'fontsize', 16, 'fontweight', 'bold')
legend({'1', '2', '3'}, 'location', 'southeast')
