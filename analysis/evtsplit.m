function [outdat,time] = evtsplit(data,evt,startT,endT,sr,starttime)
% splits the time series data in data with sampling rate sr into a matrix of
% snippets with one row for each event timestamp in evt; startT and
% endT are the times relative to evt to grab; time is a list
% of times for each bin relative to the entries in evt
% starttime is the timestamp of the first bin in data

% define frequency if it isn't supplied
if ~exist('sr','var')
    sr = 1;
end

% if start time isn't specified, assume it's 0
if ~exist('starttime','var')
    starttime = 0;
end

numevt=numel(evt); %number of event timestamps
dt = 1/sr; %time bin size
nstart = ceil(startT*sr); %number of bins to grab before
nend = ceil(endT*sr); %number of bins to grab after

evtrel = evt - starttime; %relative event time

% preallocate output matrix
outdat = nan(numevt,abs(nstart)+abs(nend)+1); %npre+npost+0 bin
for ind = 1:numevt
    bins_to_grab = (nstart:nend) + round( evtrel(ind)/dt );
    
    %now take care of ends of time series
    if bins_to_grab(1) < 1  %if we're at the start of series...
        bins_to_grab = bins_to_grab(bins_to_grab >= 1); %truncate
        outdat(ind,(end-length(bins_to_grab)+1):end) = data(bins_to_grab);
    elseif bins_to_grab(end) > length(data) %if we're at the end...
        bins_to_grab = bins_to_grab(bins_to_grab <= length(data)); %truncate
        outdat(ind,1:length(bins_to_grab)) = data(bins_to_grab);
    else
        outdat(ind,:) = data(bins_to_grab);
    end
    
end

time = (nstart:nend)*dt;

