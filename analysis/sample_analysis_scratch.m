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
normtype = 0;  % 0 for subtractive, 1 for divisive
overplot = 0;  % 0 produces a new plot, 1 plots into existing axes
plottype = 1;  % 0 for no sem, 1 for error shading, 2 for dotted lines

%% run task-specific analysis
if ~overplot
    figure
end

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