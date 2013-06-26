%simple function to plot pupil points

function [x,y] = pupilplots(timeStampAll,rightEyeAll, leftEyeAll, StimOff, StimOnSet);
hold on
yL = [-1 4];
k=plot(timeStampAll,rightEyeAll(:,12));
set(k, 'Color', 'm')
q=plot(timeStampAll,leftEyeAll(:,12));
set(q, 'Color', 'b')
for i=1:length(StimOff)
line([StimOff(i) StimOff(i)], yL, 'Color', 'r');
line([StimOnSet(i) StimOnSet(i)], yL, 'Color', 'g');
end
end