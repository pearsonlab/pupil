function [outdat,time] = evtsplit(evt,pretime,posttime,sr,task,starttime)
%splits the time series data in data with sampling rate sr into a matrix of
%snippets with one row for each event timestamp in evt; pretime and
%posttime are the times prior to and following evt to grab; time is a list
%of times for each bin relative to the entries in evt
%starttime is the timestamp of the first bin in data



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

%kdata=data;
evtrel = evt - starttime;

if strcmp(task, 'darklight')==1;
for ind = 1:numevt
    bins_to_grab= evt(ind)+(-npre:npost) 
    outdat(:,ind)=bins_to_grab
end
end


time = (-npre:npost)*dt;

