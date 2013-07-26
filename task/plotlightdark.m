function plotlightdark(srtbins,testdata,chopmat)

for i = 1:length(srtbins)
    line([srtbins(i) srtbins(i)],[min(testdata.lefteye(:,12)-0.25) max(testdata.lefteye(:,12)+0.25)]);
end

% hleg1 = legend('First Stimulus','Second Stimulus', 'Third Stimulus');

figure;
plot(chopmat(:,1:3));

end
