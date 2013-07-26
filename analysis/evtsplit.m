
function [outdat,outdat2,whicheye] = evtsplit(evt,task,datamat,whicheye,twoeye,norm)

%splits the time series data into a matrix of snippets with one row for 
%each event timestamp in evt;  time is a list
%of times for each bin relative to the entries in evt
%whicheye allows for choice of which eyes to plot: 1(left eye), 2(right
%eye),4(avg of 2 eyes). 
%to plot both insert optional argument twoeye 
%to normalize insert optional argument norm

[npre,npost,nnorm,numevt,dt] = defbin(evt,1,2,60,task,0.2,1);

weye=whicheye;

% evtrel = evt - starttime;
if twoeye==1 % If we want two eyes
    outdat2= nan(numevt,npre+npost+1); 
    whicheye=1;
else
    outdat2=[];
end

outdat = nan(numevt,npre+npost+1); %npre+npost+0 bin

for ind = 1:numevt
    bins_to_grab = (-npre:npost) + evt(ind);

%now take care of ends of time series
if bins_to_grab(1) < 1  %if we're at the start of series...
    bins_to_grab = bins_to_grab(bins_to_grab >= 1); %truncate
    outdat(ind,(end-length(bins_to_grab)+1):end) = datamat(bins_to_grab,whicheye);
if twoeye==1 % If we want two eyes
    outdat2(ind,(end-length(bins_to_grab)+1):end) = datamat(bins_to_grab,whicheye+1);
end

elseif bins_to_grab(end) > length(datamat) %if we're at the end...
    bins_to_grab = bins_to_grab(bins_to_grab <= length(datamat)); %truncate
    outdat(ind,1:length(bins_to_grab)) = datamat(bins_to_grab,whicheye);
if twoeye==1 % If we want two eyes
    outdat2(ind,1:length(bins_to_grab)) = datamat(bins_to_grab,whicheye+1);
end
else
    outdat(ind,1:length(bins_to_grab)) = datamat(bins_to_grab,whicheye);
    if twoeye==1
    outdat2(ind,1:length(bins_to_grab)) = datamat(bins_to_grab,whicheye+1);
    end
end


end

outdat = outdat';
if twoeye==1
    outdat2=outdat2';
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

