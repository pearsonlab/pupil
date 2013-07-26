% pupiltest.m
% Created by Ali Bootwala
% 11/23/2012
% renamed jmp 2013-06-29
%% Initialize Workspace
clear; clc; sca

%% Take care of path
if ispc
    addpath('C:\Users\pearson\Documents\MATLAB\tobiiSDK')
    addpath('C:\Users\pearson\Documents\GitHub\pupil')
else
    addpath('/Applications/tobiiSDK/matlab/EyeTrackingSample');
    addpath('/Applications/tobiiSDK/matlab/EyeTrackingSample/functions');
    addpath('/Applications/tobiiSDK/matlab/tetio');
    addpath('/matlab/pupil');
    addpath('/matlab/pupil/task');
end

%% End where we begin
STARTDIR = pwd; %starting directory
if ispc
    DATADIR = 'C:\Users\pearson\Documents\data\pupil';
else
    DATADIR = fullfile(filesep,'data','pupil'); %data directory
end

%% get subject details, check to see if files exist
while 1
    subjstr = input(sprintf('Please enter subject number: '),'s');
    subjnum = uint16(str2double(subjstr)); %convert to integer
    
    % check to see whether subject directory exists
    subjdir = fullfile(DATADIR,subjstr);
    if exist(subjdir,'dir')
        disp('Warning: Subject directory already exists! Previous data will not be overwritten.')
        newsub = input('Do you wish to choose a new subject number (y/n)?:  ','s');
        
        switch lower(newsub)
            case 'y'
                continue
            case 'n'
                break
        end
    else
        mkdir(subjdir)
        break
    end
end

%% set up menus


menustr = sprintf(strcat('Please select an option:\n', ...
    '-------------------------------------------\n', ...
    '0) Calibrate Subject\n', ...
    '1) Dark Test\n', ...
    '2) Pupillary Sleep Test\n', ...
    '3) Light Test\n', ...
    '4) Reversal Learning\n', ...
    '5) Oddball\n', ...
    '6) Surprise\n', ...
    '7) Run All\n', ...
    'Q) Quit\n\n', ...
    'Choice:\t'));

%% initialize Tobii SDK
disp('Initializing tetio...');
tetio_init();
tetio_CONNECT;
TrackPupil;
%% ready PTB
warning('off','MATLAB:dispatcher:InexactMatch');
Screen('Preference', 'SkipSyncTests',2); %disables all testing -- use only if ms timing is not at all an issue
Screen('Preference','VisualDebugLevel', 0);
Screen('Preference', 'SuppressAllWarnings', 1);
PTBprelims;

%% start the menu loop
while 1
    display_instructions(win,'Relax. The task will begin shortly.',1);
    
    choice = input(menustr,'s');
    TrackPupil; %%this is here to make sure that the person doesn't move in between tests and then we lose their eyes and then the last 3 tests record no data at all, ya know, for example
    switch choice
        case '0'
            stub = 'calibrate';
            numpts = uint16(str2double(input('How many points?: ','s')));
            outfile = get_next_fname(subjdir,subjnum,stub);
            [errcode,calibdata] = calibrate(numpts,outfile);
            if errcode == 1
                tetio_stopCalib;
                tetio_disconnectTracker;
                clc
                fprintf('Calibration not successful! Try again, perhaps with more points.\n\n')
            else
                clc
                disp('Calibration successful!')
            end
            continue
            
        case '1'
            stub = 'darktest';
            outfile = get_next_fname(subjdir,subjnum,stub);
            lightdarktest(0,outfile)
            continue
        case '2'
            stub = 'pst';
            pstdur = 120;
            outfile = get_next_fname(subjdir,subjnum,stub);
            pst(pstdur,outfile)
            continue
        case '3'
            stub = 'lighttest';
            outfile = get_next_fname(subjdir,subjnum,stub);
            lightdarktest(1,outfile)
            continue
        case '4'
            stub = 'revlearn';
            neworold=input('Would you like to generate a new vector? Y/N ','s');
            lower(neworold);
            outfile = get_next_fname(subjdir,subjnum,stub);
            revlearn(outfile,(strcmp(neworold,'n')), 'RevVectors', 'six');
            %%%this needs to be fixed, right now generating a new vector
            %%%isn't working =)
            continue
        case '5'
            stub = 'oddball';
            neworold=input('Would you like to generate a new vector? Y/N ','s');
            lower(neworold);
            outfile = get_next_fname(subjdir,subjnum,stub);
            oddball(outfile,(strcmp(neworold,'n')),'OddballVectors', 'six')
        case 'Q'
            break
    end
    

    
end




%% Wrap up participant
tetio_disconnectTracker()
tetio_cleanUp()
cd(STARTDIR)
Screen('CloseAll')
clc
