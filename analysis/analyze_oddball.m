% analyze_oddball.m
% scratch code for analysis of oddball task

etimes = us2secs([data.soundtime], t0);
wasodd = trialvec == 1;
tpre = -0.3;
tpost = 8;
[pmat, binT] = evtsplit(pupil, etimes, tpre, tpost, sr);

pcorr = basenorm(pmat(wasodd, :), binT, [-inf 0]);
pinc = basenorm(pmat(~wasodd, :), binT, [-inf 0]);

type = 1;
plot_with_sem(pcorr, 0, 1/sr, type, binT, [0 1 0])
plot_with_sem(pinc, 0, 1/sr, type, binT, [1 0 0])

%plot(binT, pmat', 'linewidth', 2.0)
xlim([tpre tpost])
title('Pupillary response to oddball','fontsize', 20, 'fontweight', 'bold')
xlabel('Time from sound (seconds)', 'fontsize', 16, 'fontweight', 'bold')
ylabel('Normalized pupil size (arb units)', 'fontsize', 16, 'fontweight', 'bold')
legend({'Oddball', '', 'Standard', ''}, 'location', 'southeast')