function out = traverse(directory, result)
    
    if exist('result', 'var')
        out = result;
    end  
    
    listing = dir(directory);
    disp(directory)
    
    % loop through .mat files
    matfiles = dir(fullfile(directory, '*.mat'));
    for ind = 1:length(matfiles)
        % set these variables so prepdata can do its magic
        newdir = directory;
        dfile = matfiles(ind).name;
        try
            prepdata;
            thisdata.filename = fname;
            thisdata.subject = subj;
            thisdata.dataset = dset;
            thisdata.task = task;
            thisdata.pupil = pupil;
            thisdata.baseline = slowpupil;
            thisdata.smoothing_window = Tsmooth;
            thisdata.sr = sr;
            
            if exist('out', 'var')
                out(end+1) = thisdata;
            else
                out = thisdata;
            end
        end
    end
    
    % traverse subdirectories: start at 3 to skip . and ..
    for ind = 3:length(listing)
        if listing(ind).isdir
            if exist('out', 'var')
                out = traverse(fullfile(directory, listing(ind).name), out);
            else
                out = traverse(fullfile(directory, listing(ind).name));
            end
        end
    end
    
    
end