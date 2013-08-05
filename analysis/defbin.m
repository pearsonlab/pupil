function [npre,npost,numevt,dt] = defbin(evt,pretime,posttime,sr,task,starttime)

% defines bins to take before and after event; defines normalization period
% pretime and posttime are the times prior to and following evt to grab;
% starttime is the timestamp of the first bin in data;
% sampling rate sr

%define frequency if it isn't supplied
if ~exist('sr','var')
    sr = 1;
end

if ~exist('starttime','var')
    starttime = 0;
end

numevt=numel(evt); %number of event timestamps
dt = 1/sr; %time bin size
npre = ceil(pretime*sr); %number of bins to grab before
npost = ceil(posttime*sr); %number of bins to grab after

end
