%%%% Hello world! Little tiny plotting function. 
function cleanplot(filename)
load('filename')


datamat = repmat((NaN), max([length(data(1).lefteye),length(data(2).lefteye),length(data(3).lefteye)]),7);


for i = 1:length(data)
    
    data(i).lefteye(data(i).lefteye(:,13)~=0,12) = NaN;
    data(i).righteye(data(i).righteye(:,13)~=0,12) = NaN;
    
    datamat(1:length(data(i).lefteye),i)=data(i).lefteye(:,12);
   % datamat{1:length(data(i).righteye),i}=data(i).righteye(:,12);
  

end


combin=horzcat(data.lefteye(:,12), data.righteye(:,12));
plot(combin);

