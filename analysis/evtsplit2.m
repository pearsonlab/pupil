%%this function is going to create a chopped structure that has the left eye, right
%%eye and average of both
function [outdat] = evtsplit2(evt,task,datamat)

% Define bins to grab before/after
[npre,npost,numevt,dt] = defbin(evt,1,2,60,task,1);

%%we want to grab from column 1,2 and 4, I'm sure there's a nicer way to do
%%this but this is what I thought of at the moment and it appears to work
index=[1 2 4];

for i=index(1):index(end);
    
    chopmat = nan(numevt,npre+npost+1); %npre+npost+0 bin
    
    for ind = 1:numevt 
        bins_to_grab = (-npre:npost) + evt(ind);
        
        %now take care of ends of time series
        if bins_to_grab(1) < 1  %if we're at the start of series...
            bins_to_grab = bins_to_grab(bins_to_grab >= 1); %truncate
            chopmat(ind,(end-length(bins_to_grab)+1):end) = datamat(bins_to_grab,i);
        elseif bins_to_grab(end) > length(datamat) %if we're at the end...
            bins_to_grab = bins_to_grab(bins_to_grab <= length(datamat)); %truncate
            chopmat(ind,1:length(bins_to_grab)) = datamat(bins_to_grab,i);
        else
            chopmat(ind,1:length(bins_to_grab)) = datamat(bins_to_grab,i);
        end     
    end
    
    chopmat = chopmat'; % Rows become columns
    
    % Create struct of chopped data corresponding to R, L, and avg. 
    if i==1
        outdat.left=chopmat;
    elseif i==2
        outdat.right=chopmat;
    elseif i==4
        outdat.average=chopmat;
    end
    
end

end

% time = (-npre:npost)*dt;
