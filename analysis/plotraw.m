function figure1 = plotraw(datamat,whicheye,twoeye)
figure1 = figure

if twoeye==1
    plot(datamat(:,1),'Color','g');
    hold on
    plot(datamat(:,2),'Color','b');
end

plot(datamat(:,whicheye),'Color','r');

end