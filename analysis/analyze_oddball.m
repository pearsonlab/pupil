% analyze_oddball.m
% scratch code for analysis of oddball task

etimes = us2secs([data.soundtime], t0);
wasodd = trialvec == 1;
tpre = -0.3;
tpost = 8;
[pmat, binT] = evtsplit(pupil, etimes, tpre, tpost, sr);

pcorr = basenorm(pmat(wasodd, :), binT, [-inf 0], normtype);
pinc = basenorm(pmat(~wasodd, :), binT, [-inf 0], normtype);

plot_with_sem(pcorr, 0, 1/sr, plottype, binT, [0 1 0])
plot_with_sem(pinc, 0, 1/sr, plottype, binT, [1 0 0])

%plot(binT, pmat', 'linewidth', 2.0)
xlim([tpre tpost])
title('Pupillary response to oddball','fontsize', 20, 'fontweight', 'bold')
xlabel('Time from sound (seconds)', 'fontsize', 16, 'fontweight', 'bold')
ylabel('Normalized pupil size (arb units)', 'fontsize', 16, 'fontweight', 'bold')

switch plottype
    case 0
        legend({'Oddball', 'Standard'}, 'location', 'southeast')
    case 1
        legend({'Oddball', '', 'Standard', ''}, 'location', 'southeast')
    case 2
        legend({'Oddball', '', 'Standard', ''}, 'location', 'southeast')
end