% analyze_revlearn.m
% scratch code for analysis of reversal learning

etimes = us2secs([data.soundtime], t0);
wascorr = logical([data.correct]);
tpre = -0.3;
tpost = 8;
[pmat, binT] = evtsplit(pupil, etimes, tpre, tpost, sr);

pcorr = basenorm(pmat(wascorr, :), binT, [-inf 0], normtype);
pinc = basenorm(pmat(~wascorr, :), binT, [-inf 0], normtype);

type = 1;
plot_with_sem(pcorr, 0, 1/sr, type, binT, [0 1 0])
plot_with_sem(pinc, 0, 1/sr, type, binT, [1 0 0])

%plot(binT, pmat', 'linewidth', 2.0)
xlim([tpre tpost])
title('Pupillary response to negative feedback','fontsize', 20, 'fontweight', 'bold')
xlabel('Time from buzzer (seconds)', 'fontsize', 16, 'fontweight', 'bold')
ylabel('Normalized pupil size (arb units)', 'fontsize', 16, 'fontweight', 'bold')
legend({'Correct', '', 'Incorrect', ''}, 'location', 'southeast')