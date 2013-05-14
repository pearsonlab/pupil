function condition_status = check_status(conditions_array, max_wait, tim_interv, desired_value);
% condition_status = check_status(cond, max_wait, tim_interv, des)
% Check the status of the tobii thread based on the 'GET_STATUS' command.
% cond -> choose which flags to test. 
% max_wait*tim_interv -> approximate the total time of waiting the system
% to reach a desired state. For example, it is for 'max_wait' times the system
% status is checked whether it has been connected succesfully to the TET
% server. Each time, the script waits for 'tim_interv' in secs before
% re-trying. 
% des -> desired value of the condition 'cond'. (0 or 1)
% cond_res returns the latest status reported by the GET_STATUS
%
% Use help talk2tobii for more information on what 'GET_STATUS' returns

numCond = length(conditions_array);
condition_status = zeros(1,numCond); % stores the statuses of requested conditions


count = 1;
fprintf('checking conditions:');
for i=1:numCond
    fprintf('%d \n',conditions_array(i));
end

while 1
    fprintf('.');
    status = talk2tobii('GET_STATUS');
    for current_condition = 1:numCond
        if( status( conditions_array(current_condition) ) )
            condition_status(current_condition) = 1;
        else
            condition_status(current_condition) = 0;
        end
    end
    
    tmp = find(condition_status ~= desired_value);
    if( isempty( tmp ) )
        disp('  break up 1: success, conditions met');
        break;
    end
   

    if(max_wait<count) %give up
        disp('  break up 2: timeout');
        break;
    end
    WaitSecs(tim_interv);
    count = count+1;
end

fprintf('\n');

