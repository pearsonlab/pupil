function plotlightdark(srtbins,testdata,chopmat,task,chopmat2)

for i = 1:length(srtbins)
    line([srtbins(i) srtbins(i)],[min(testdata.lefteye(:,12)-0.25) max(testdata.lefteye(:,12)+0.25)]);
end

% hleg1 = legend('First Stimulus','Second Stimulus', 'Third Stimulus');

figure;

if strcmp(task, 'darktest')==1
plot(chopmat(:,1:3));
if exist('chopmat2')
    hold on
    plot(chopmat2(:,1:3),'Color','g');
end
else
    plot(chopmat(:,1:4))
    if exist('chopmat2')
        hold on
        plot(chopmat2(:,1:4),'Color','g');
    end
    

end
