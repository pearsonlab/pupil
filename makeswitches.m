function out = makeswitches(nswitch, minrun, maxrun,seed)
% creates a pseudo-random distribution of runs of 0s and 1s
% nswitch is the number of switches, minrun is the minimum run length
% maxrun is the maximum run length
% seed is an optional random number seed

if ~exist('seed','var')
    seed = 12345;
end

% set random number stream
rng(seed);

% span of runs
delta = maxrun-minrun;

% run lengths (nswitch+1 runs for nswitch switches)
lens = randi(delta, [1 nswitch+1])+ minrun; 

% calculate switches
switchtrials = cumsum([1 lens]); %which are the switch trials
isswitch = zeros(1,switchtrials(end)); 
isswitch(switchtrials(1:end-1)) = 1;

% values in each run
vals = zeros(1,nswitch+1);
vals(2:2:end) = 1; %make all even values 1

% expand
whichval = cumsum(isswitch);
trials = vals(whichval);

% now, decide whether or not we begin with 0 or 1
if round(rand)
    out = trials;
else
    out = 1 - trials;
end