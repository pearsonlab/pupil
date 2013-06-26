%simple function to plot pupil points

function r=pupilplots (timeStampAll,rightEyeAll, leftEyeAll, StimOff, StimOnSet);
yL = get(gca,'YLim');
r=plot(timeStampAll,rightEyeAll(:,12));
set(r, 'Color', 'c')
r=plot(timeStampAll,leftEyeAll(:,12));
set(r, 'Color', 'b')
for i=1:length(StimOff)
line([StimOff(i) StimOff(i)], yL, 'Color', 'r');
line([StimOnSet(i) StimOnSet(i)], yL, 'Color', 'g');
end
end