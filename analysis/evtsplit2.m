%%this function is going to create a chopped structure that has the left eye, right
%%eye and average of both
function [chopmat]=makealleyestruct(npre,npost,evt,whateveridontremembercurrently,datamat?)
[npre,npost,nnorm,numevt,dt] = defbin(evt,1,2,60,task,0.2,1);

outdat = nan(numevt,npre+npost+1); %npre+npost+0 bin

%%we want to grab from column 1,2 and 4, I'm sure there's a nicer way to do
%%this but this is what I thought of at the moment and it appears to work
index=[1 2 4];


for i=index(1):index(end);
for ind = 1:numevt
    bins_to_grab = (-npre:npost) + evt(ind);

%now take care of ends of time series
if bins_to_grab(1) < 1  %if we're at the start of series...
    bins_to_grab = bins_to_grab(bins_to_grab >= 1); %truncate
    outdat(ind,(end-length(bins_to_grab)+1):end) = datamat(bins_to_grab,i);
elseif bins_to_grab(end) > length(datamat) %if we're at the end...
    bins_to_grab = bins_to_grab(bins_to_grab <= length(datamat)); %truncate
    outdat(ind,1:length(bins_to_grab)) = datamat(bins_to_grab,i);
else
    outdat(ind,1:length(bins_to_grab)) = datamat(bins_to_grab,i);
end

outdat = outdat';

end
if i==1
chopmat.left=outdat;
elseif i==2
    chopmat.right=outdat;
elseif i==4
    chopmat.average=outdat;
end
end


if norm==1
% normalize with 
for ind = 1:length(evt)
outdat(:,ind) = outdat(:,ind)-(nanmean(datamat((evt(ind)-nnorm):evt(ind),whicheye)));
if twoeye==1
 outdat2(:,ind) = outdat2(:,ind)-(nanmean(datamat((evt(ind)-nnorm):evt(ind),whicheye+1)));   
end
end

whicheye=weye;

end

time = (-npre:npost)*dt;
