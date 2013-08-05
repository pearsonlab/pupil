function figure1 = plotraw(datamat,whicheye,twoeye)
figure1 = figure

if twoeye==1
    plot(datamat(:,1),'Color','g');
    hold on
    plot(datamat(:,2),'Color','b');
end
 
plot(datamat(:,whicheye),'Color','r','linewidth',2);
set(gca,'XTick',0:360:length(datamat));
set(gca,'XTickLabel',{0:6:200});
set(gca,'FontSize',10);

end