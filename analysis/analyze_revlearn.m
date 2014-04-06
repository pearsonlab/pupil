% analyze_revlearn.m
% scratch code for analysis of reversal learning

corr_color = [0 1 0];
inc_color = [1 0 0];

etimes = us2secs([data.soundtime], t0);
wascorr = logical([data.correct]);
tpre = -0.3;
tpost = 8;
[pmat, binT] = evtsplit(pupil, etimes, tpre, tpost, sr);

pcorr = basenorm(pmat(wascorr, :), binT, [-inf 0], normtype);
pinc = basenorm(pmat(~wascorr, :), binT, [-inf 0], normtype);

plot_with_sem(pcorr, 0, 1/sr, plottype, binT, corr_color)
plot_with_sem(pinc, 0, 1/sr, plottype, binT, inc_color)

%plot(binT, pmat', 'linewidth', 2.0)
xlim([tpre tpost])
title('Pupillary response to negative feedback','fontsize', 20, 'fontweight', 'bold')
xlabel('Time from buzzer (seconds)', 'fontsize', 16, 'fontweight', 'bold')
ylabel('Normalized pupil size (arb units)', 'fontsize', 16, 'fontweight', 'bold')

switch plottype
    case 0
        legend_str = {'Correct', 'Incorrect'};
    case 1
        legend_str = {'Correct', '', 'Incorrect', ''};
    case 2
        legend_str = {'Correct', '', 'Incorrect', ''};
end

if diffwave
    plot_with_sem(nanmean(pinc) - nanmean(pcorr), 0, 1/sr, 0, binT, [0 0 0]);
    legend_str{end + 1} = 'Difference';
end

legend(legend_str, 'location', 'southeast')
