%%%% Hello world! Little tiny plotting function. 
function cleanplot(filename)
load('filename')


data.lefteye(data.lefteye(:,13)~=0,12) = NaN;
data.righteye(data.righteye(:,13)~=0,12) = NaN;
combin=horzcat(data.lefteye(:,12), data.righteye(:,12));
plot(combin);

