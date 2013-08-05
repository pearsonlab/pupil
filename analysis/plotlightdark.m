function plotlightdark(srtbins,testdata,outdat,task,twoeye,datamat,plotwhat)

for i = 1:length(srtbins)
    line([srtbins(i) srtbins(i)],[min(datamat(:,4)-0.25) max(datamat(:,4)+0.25)],'Color','k','linewidth',2);
end

% hleg1 = legend('First Stimulus','Second Stimulus', 'Third Stimulus');

sizeout = size(outdat.(plotwhat));

figure;

plot(outdat.(plotwhat)(:,1:sizeout(2)),'linewidth',2);
line([60 60],[min(outdat.(plotwhat)(:)-0.25) max(outdat.(plotwhat)(:)+0.25)],'Color','k','linewidth',2);

ylim([min(outdat.(plotwhat)(:)-0.25) max(outdat.(plotwhat)(:)+0.25)]);
set(gca,'XTick',0:60:length(outdat));
set(gca,'XTickLabel',{'-1','0','1','2','3'});
set(gca,'FontSize',14);

if twoeye==1
    hold on
    plot(outdat.leftnorm(:,1:3),'Color','g','linewidth',2);
    hold on
    plot(outdat.rightnorm(:,1:3),'Color','b','linewidth',2);
end

  
end
