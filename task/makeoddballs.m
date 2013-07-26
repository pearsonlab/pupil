function trialvec = makeoddballs(noddballs, minrun, maxrun, seed)
% creates a pseudo-random distribution of oddballs (1s) on a background of
% zeros
% nswitch is the number of switches, minrun is the minimum run length
% maxrun is the maximum run length
% seed is an optional random number seed

if ~exist('seed','var')
    seed = 12345;
end

% set random number stream
rand('seed',seed); %to be deprecated in future
%rng(seed); %correct syntax in future
%current worry is that Psychtoolbox relies on the older syntax

% span of runs
delta = maxrun-minrun;

% run lengths (noddballs+1 runs for noddballs oddballs)
%note that randi draws from [1,delta+1], so add minrun-1;
lens = randi(delta+1, [1 noddballs+1]) + minrun-1; 

% calculate oddballs
oddtrials = cumsum(lens); %which are the switch trials
isodd = zeros(1,oddtrials(end)); 
isodd(oddtrials(1:end-1)) = 1;

trialvec = isodd;