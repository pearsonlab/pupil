% Makes matrix 'chopmat' with columns of data corresponding to each event. 
% Data are normalized 
% Data columns are chopped to x seconds before and y seconds after.

function [chopmat] = chopmaker(datamat,npre,npost,srtbins)

   chopmat = [];
   
    for ind = 1:length(srtbins)
        chopmat(:,ind) = datamat((srtbins(ind)-npre):(srtbins(ind)+npost),4);
        % Normalize by subtracting out avg of 200ms before
        chopmat(:,ind) = chopmat(:,ind)-(nanmean(datamat((srtbins(ind)-12):srtbins(ind),4)));
    end
    
end