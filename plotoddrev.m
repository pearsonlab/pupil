function oddrevplot = plotoddrev(chopmat,trialvec,srtbins,testdata,task)


% Extract oddball data.
oddavg = chopmat(:,logical(trialvec));
sizeo = size(oddavg);
normavg = chopmat(:,(find(trialvec==0)));
sizen = size(normavg);

% Plot vertical lines for normal (blue) vs. odd sounds (red) on figure 1.

for i = 1:length(trialvec)
    if trialvec(i) == 0
        line([srtbins(i) srtbins(i)],[min(testdata.lefteye(:,12)-0.25) max(testdata.lefteye(:,12)+0.25)]);
    else
        y = line([srtbins(i) srtbins(i)],[min(testdata.lefteye(:,12)-0.25) max(testdata.lefteye(:,12)+0.25)]);
        set(y, 'Color', 'r');
    end
end

% Average normal and oddball lefteye data and then plot on new figure

normavg(normavg == 0) = NaN;
oddavg(oddavg == 0) = NaN;

for i=1:length(normavg)
    plot2odd(i,1) = nanmean(normavg(i,:));
    plot2odd(i,2) = nanmean(oddavg(i,:));
    plot2odd(i,3) = nanstd(normavg(i,:))/sizen(2);
    plot2odd(i,4) = nanstd(oddavg(i,:))/sizeo(2);
end

figure;
plot(plot2odd(:,1:2));
hold on
plot(plot2odd(:,3:4),'--');

end
