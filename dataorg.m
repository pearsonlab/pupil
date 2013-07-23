%%%%% This function organizes data.

% function dataorg(filename)

if ~exist('task')
    testdata=data;
else
    testdata=eyedata;
end

[findevents;

makemat;

makesec;

plotraw;

evtsplit;

chopmaker;

% end