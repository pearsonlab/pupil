function plotlightdark(srtbins,testdata,outdat,outdat2,task,twoeye,datamat)

for i = 1:length(srtbins)
    line([srtbins(i) srtbins(i)],[min(datamat(:,4)-0.25) max(datamat(:,4)+0.25)],'Color','k','linewidth',2);
end

% hleg1 = legend('First Stimulus','Second Stimulus', 'Third Stimulus');

figure;

if strcmp(task, 'darktest')==1
plot(outdat(:,1:3),'linewidth',2);
line([60 60],[-1 1],'Color','k','linewidth',2);

set(gca,'XTick',0:60:length(outdat));
set(gca,'XTickLabel',{'-1','0','1','2','3'});
set(gca,'FontSize',14);

if twoeye==1
    hold on
    plot(outdat2(:,1:3),'Color','g','linewidth',2);
end
else
    plot(outdat(:,1:4),'linewidth',2);
    set(gca,'XTick',0:60:length(outdat));
    set(gca,'XTickLabel',{'-1','0','1','2','3'});
    set(gca,'FontSize',14);
    line([60 60],[-2.5 1],'Color','k','linewidth',2);

    
    if twoeye==1
        hold on
        plot(outdat2(:,1:4),'Color','g','linewidth',2);
    end
  
end
