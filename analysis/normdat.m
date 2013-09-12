function [outdat] = normdat(evt,normtime,sr,outdat,datamat)

% Normalize data by subtracting avg. of normtime s before

nnorm = ceil(normtime*sr); % Number of bins to normalize over

for ind = 1:length(evt)
outdat.leftnorm(:,ind) = outdat.left(:,ind)-(nanmean(datamat((evt(ind)-nnorm):evt(ind),1)));
outdat.rightnorm(:,ind) = outdat.right(:,ind)-(nanmean(datamat((evt(ind)-nnorm):evt(ind),2)));
outdat.averagenorm(:,ind) = outdat.average(:,ind)-(nanmean(datamat((evt(ind)-nnorm):evt(ind),4)));
end

end