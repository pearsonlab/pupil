function [ output_args ] = tstatus()
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

[status,history] = talk2tobii('GET_STATUS');

for i = 1:12
    
    
    switch i
        case 1
            if status(i)
                fprintf('connection has been requested\n');
            end
        case 2
            if status(i)
                fprintf('tobii is connected\n')
            else
                fprintf('tobii is not connected\n')
            end
        case 3
            if status(i)
                fprintf('tobii is disconnecting\n')
            end
        case 4
            if status(i)
                fprintf('tobii is beginning calibration\n')
            end
        case 5
            if status(i)
                fprintf('tobii is calibrating\n')
            end
        case 6
            if status(i)
                fprintf('a request for tobii to record data has been made\n')
            end
        case 7
            if status(i)
                fprintf('tobii is recording data\n')
            end
        case 8
            if status(i)
                fprintf('a request for tobii to stop recording has been made\n')
            end
        case 9
            if status(i)
                fprintf('the tobii thread has exited\n')
            end
        case 10
            if status(i)
                fprintf('clock synchronisation hase been requested\n')
            end
        case 11
            if status(i)
                fprintf('calibration has finished\n')
            end
        case 12
            if status(i)
                fprintf('clocks have been syncronized\n')
            end
    end
    
    
end

end

