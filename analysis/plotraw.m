function figure1 = plotraw(datamat,whicheye,twoeye)
figure1 = figure

if twoeye==1
    plot(datamat(:,1),'Color','g');
    hold on
    plot(datamat(:,2),'Color','b');
end
 
plot(datamat(:,whicheye),'Color','r','linewidth',2);
set(gca,'XTick',0:360:length(datamat));
set(gca,'XTickLabel',{'0','3','6','9','12','15','18','21','24','27','30','33','36','39','42','45','48','51','54','57','60','63','66','69','72','75'});
set(gca,'FontSize',10);

end