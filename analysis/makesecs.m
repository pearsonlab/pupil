    % Convert timestamps into seconds
    
    function [datamat] = makesecs(datamat)
    datamat(:,3)=(double(datamat(:,3)))/1000000;
    end