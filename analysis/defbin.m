%%% Defines bins to take before and after event
% Pretime and posttime are the times prior to and following evt to grab;
% Starttime is the timestamp of the first bin in data;
% Sampling rate sr (frequency = 60)

function [npre,npost,numevt,dt] = defbin(evt,pretime,posttime,sr,task,starttime)

% Define frequency if not supplied
if ~exist('sr','var')
    sr = 1;
end

% Define starttime if not supplied
if ~exist('starttime','var')
    starttime = 0;
end

numevt=numel(evt); %number of event timestamps
dt = 1/sr; %time bin size
npre = ceil(pretime*sr); %number of bins to grab before
npost = ceil(posttime*sr); %number of bins to grab after

end
