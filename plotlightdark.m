function plotlightdark(srtbins,testdata,chopmat,task)

for i = 1:length(srtbins)
    line([srtbins(i) srtbins(i)],[min(testdata.lefteye(:,12)-0.25) max(testdata.lefteye(:,12)+0.25)]);
end

% hleg1 = legend('First Stimulus','Second Stimulus', 'Third Stimulus');

figure;
if strcmp(task, 'darktest')==1
plot(chopmat(:,1:3));
else
    plot(chopmat(:,1:4))

end
