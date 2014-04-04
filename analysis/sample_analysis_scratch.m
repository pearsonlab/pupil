% scratchpad for working out some sample plots of behavior

%% setup paths
addpath('~/code/pupil/analysis')
addpath('~/code/pupil/analysis/utils')
addpath('~/code/electrophysiology')
ddir = '~/data/pupil/';

%% load data
[dfile, newdir, was_success] = uigetfile([ddir '*.mat']);

%% prepare data
if was_success
    prepdata
else
    warning('You must select a valid file!');
end

%% set options
normtype = 1;

%% run task-specific analysis
switch task
    case 'darktest'
        analyze_darktest
    case 'lighttest'
        analyze_lighttest
    case 'revlearn'
        analyze_revlearn
    case 'oddball'
        analyze_oddball
    case 'pst'
        analyze_pst
end