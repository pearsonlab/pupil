function plotoddrev(outdat,outdat2,trialvec,srtbins,eyedata,task,twoeye)


% Extract oddball data.
oddavg = outdat(:,logical(trialvec));
sizeo = size(oddavg);
normavg = outdat(:,(find(trialvec==0)));
sizen = size(normavg);


% Plot vertical lines for normal (blue) vs. odd sounds (red) on figure 1.

for i = 1:length(trialvec)
    if trialvec(i) == 0
        %line([srtbins(i) srtbins(i)],[min(eyedata.lefteye(:,12)-0.25) max(eyedata.lefteye(:,12)+0.25)]);
            %line([srtbins(i) srtbins(i)],[0 5]);

    else
        %y = line([srtbins(i) srtbins(i)],[min(eyedata.lefteye(:,12)-0.25) max(eyedata.lefteye(:,12)+0.25)]);
                y = line([srtbins(i) srtbins(i)],[2 5]);

        set(y, 'Color', 'k','linewidth',2);
    end
end

% Average normal and oddball lefteye data and then plot on new figure

normavg(normavg == 0) = NaN;
oddavg(oddavg == 0) = NaN;

for i=1:length(normavg)
    plot2odd(i,2) = nanmean(normavg(i,:));
    plot2odd(i,1) = nanmean(oddavg(i,:));
    plot2odd(i,3) = plot2odd(i,1)-nanstd(normavg(i,:))/sizen(2);
    plot2odd(i,4) = plot2odd(i,1)+nanstd(normavg(i,:))/sizen(2);
    plot2odd(i,5) = plot2odd(i,2)-nanstd(oddavg(i,:))/sizeo(2);
    plot2odd(i,6) = plot2odd(i,2)+nanstd(oddavg(i,:))/sizeo(2);
end

figure;
plot(plot2odd(:,1:2),'linewidth',2);
hold on
plot(plot2odd(:,3:6),'--','Color','k');
    set(gca,'XTick',0:60:length(outdat));
    set(gca,'XTickLabel',{'-1','0','1','2','3'});
    set(gca,'FontSize',14);
    line([60 60],[-0.4 0.4],'Color','k','linewidth',2);

end
