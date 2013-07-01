function fname = get_next_fname(datadir,sub,stub)
% files for pupiltest are named <sub>.<version>.<stub>.pupiltest.mat
% this function calculates version from files in current directory and
% returns string of filename

startdir = pwd;
cd(datadir)

% list contents of directory
flist = dir;
% extract all file names
allnames = {flist.name};

% define a regular expression that looks ahead for stub
pattern = sprintf('[1-9]+(?=.%s)',stub);

% regexp returns one cell for each filename, itself a cell array of matches
match = regexp(allnames, pattern, 'match', 'once');
% get the number of the latest version, convert to integer
lastver = max(str2double(match));

% increment
ver = uint16(lastver) + 1;

fpart = strcat(num2str(sub),'.',num2str(ver),'.',num2str(stub),'.pupiltest.mat');

fname = fullfile(datadir,fpart);

cd(startdir)