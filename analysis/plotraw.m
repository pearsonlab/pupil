% Plot raw data (non-chopped) depending upon what plotwhat is.

function figure1 = plotraw(datamat,plotwhat)
figure;
hold on

if strcmp(plotwhat,'left') | strcmp(plotwhat,'leftnorm')==1
    plot(datamat(:,1),'Color','g');
    
elseif strcmp(plotwhat,'right') | strcmp(plotwhat,'rightnorm')==1
    plot(datamat(:,2),'Color','b');
    
elseif strcmp(plotwhat,'average') | strcmp(plotwhat,'averagenorm')==1
    plot(datamat(:,4),'Color','r','linewidth',2);
    
    set(gca,'XTick',0:360:length(datamat));
    set(gca,'XTickLabel',{0:6:200});
    set(gca,'FontSize',10);
    
end