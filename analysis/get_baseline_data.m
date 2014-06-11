% this script asks for a directory and then recursively finds data files in
% all subdirectories
% for each file, it calculates a table of baseline pupil measures

data_dir = uigetdir([start_dir '*.mat'], 'Select a directory to search for data');

pupildata = traverse(data_dir);

% organize data and save

for ind = 1:length(pupildata)
    baseline = pupildata(ind).baseline;
    
    pupildata(ind).mean = nanmean(baseline);
    pupildata(ind).median = nanmedian(baseline);
    pupildata(ind).std = nanstd(baseline);
    pupildata(ind).cv = nanstd(baseline) / nanmean(baseline);
    pupildata(ind).range = max(baseline) - min(baseline);
end

uisave({'pupildata'})