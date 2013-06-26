%% Behavior task 1
%% Initial attempt at task setup
%% 22-2-2013
%% Ali Bootwala
%% Initialize task
if exist('trialvec','var') == 1
    clear trialvec x xx
end

%% Create Task Vectors
numswitch = input('input number of switches for this trial:  ');
numargs = ceil(numswitch/2);
% Matrix created in 1's and 0's
% 1 corresponds to a left stimulus
% 0 corresponds to a right stimulus
if mod(numswitch, 2) == 0
    numargs = ceil(numswitch/2) +1;
end

switchpick = round(rand);
xx = 0;
if switchpick == 0
    for j = 1:ceil(numswitch/2)
        x = [rr(find(rr(:, j) == 0), j); rl(find(rl(:, j) == 1), j)];
        xx(j + 1) = xx(j)+length(x);
        trialvec((xx(j)+1):xx(j+1)) = x;
       % clear x
    end        
elseif switchpick == 1
    for j = 1:ceil(numswitch/2)
        x = [rl(find(rl(:, j) == 1), j); rr(find(rr(:, j) == 0), j)];
        xx(j + 1) = xx(j)+length(x);
        trialvec((xx(j)+1):xx(j+1)) = x;
       % clear x
    end
end
if mod(numswitch, 2) == 0 && switchpick == 0
    x = rr(find(rr(:, numargs) == 0), numargs);
    xx(end + 1) = xx(end) + length(x);
    trialvec((xx(end-1)+1):xx(end)) = x;
elseif mod(numswitch, 2) == 0 && switchpick == 1
    x = rl(find(rl(:, numargs) == 1), numargs);
    xx(end + 1) = xx(end) + length(x);
    trialvec((xx(end-1)+1):xx(end)) = x;
end

%% Setup matrix
% Prob = input('Probability that correct answer results in correct stimulus [0,1]: ');
% errorbounds = input('Error bounds on probability (i.e real probability is P +- errorbounds):  ');
%% Slightly more randomness??? I think
% while ceil(Prob*numtasks)+1 <= sum(ansvec == taskvec) || floor(Prob*numtasks)-1 >= sum(ansvec == taskvec)
%     ansvec = Shuffle(ansvec);
% end
%% Crude Probability inclusion
% while floor(Prob*numtasks) ~= sum(ansvec == taskvec)
%     ansvec = Shuffle(ansvec);
% end
%display('Press any key to begin behavior task')
%behaviortaskfcn