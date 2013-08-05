function plotoddrev(outdat,trialvec,srtbins,eyedata,task,twoeye,plotwhat)
% Plots for either oddball or revlearn data.
% plotwhat is which data we want to plot from outdat (ex. 'average', 'averagenorm',
% etc.)

% Extract oddball data or incorrect data
oddavg = outdat.(plotwhat)(:,logical(trialvec));
sizeo = size(oddavg);
normavg = outdat.(plotwhat)(:,(find(trialvec==0)));
sizen = size(normavg);

% Plot vertical event lines: for oddball or incorrect choice
for i = 1:length(trialvec)
    if trialvec(i) == 0
        %line([srtbins(i) srtbins(i)],[min(eyedata.lefteye(:,12)-0.25) max(eyedata.lefteye(:,12)+0.25)]);
    else
        y = line([srtbins(i) srtbins(i)],[min(outdat.average(:)-0.25) max(outdat.average(:)+0.25)],'Color', 'k','linewidth',2);
    end
end
ylim([min(outdat.average(:)-0.25) max(outdat.average(:)+0.25)]);

% Average normal and oddball lefteye data and then plot on new figure

normavg(normavg == 0) = NaN;
oddavg(oddavg == 0) = NaN;

for i=1:length(normavg)
    plot2odd(i,1) = nanmean(normavg(i,:));
    plot2odd(i,2) = nanmean(oddavg(i,:));
    plot2odd(i,3) = plot2odd(i,1)-nanstd(normavg(i,:))/sqrt(sizen(2));
    plot2odd(i,4) = plot2odd(i,1)+nanstd(normavg(i,:))/sqrt(sizen(2));
    plot2odd(i,5) = plot2odd(i,2)-nanstd(oddavg(i,:))/sqrt(sizeo(2));
    plot2odd(i,6) = plot2odd(i,2)+nanstd(oddavg(i,:))/sqrt(sizeo(2));
end

figure;
% Plot averages of pupil responses following normal/odd or
% correct/incorrect
plot(plot2odd(:,1:2),'linewidth',2);
hold on
% Plot standard deviations from mean
plot(plot2odd(:,3:6),'--','Color','k');
set(gca,'XTick',0:60:length(outdat));
set(gca,'XTickLabel',{-1:1:3});
set(gca,'FontSize',14);
% Plot event line
line([60 60],[min(plot2odd(:)-0.25) max(plot2odd(:)+0.25)],'Color','k','linewidth',2);
ylim([min(plot2odd(:)-0.25) max(plot2odd(:)+0.25)]);

end
