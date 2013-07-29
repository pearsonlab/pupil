function plotlightdark(srtbins,testdata,outdat,outdat2,task,twoeye)

for i = 1:length(srtbins)
    line([srtbins(i) srtbins(i)],[min(testdata.lefteye(:,12)-0.25) max(testdata.lefteye(:,12)+0.25)]);
end

% hleg1 = legend('First Stimulus','Second Stimulus', 'Third Stimulus');

figure;

if strcmp(task, 'darktest')==1
plot(outdat(:,1:3));
if twoeye==1
    hold on
    plot(outdat2(:,1:3),'Color','g');
end
else
    plot(outdat(:,1:4))
    if twoeye==1
        hold on
        plot(outdat2(:,1:4),'Color','g');
    end
    
end
