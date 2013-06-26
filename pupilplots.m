%simple function to plot pupil points
%for dark

yL = [-1 4];
fig = figure('Name','Pupil During Dark Test'); 
k=plot(timeStampAll_dark,rightEyeAll_dark(:,12));
set(k, 'Color', 'm')
hold on
q=plot(timeStampAll_dark,leftEyeAll_dark(:,12));
set(q, 'Color', 'b')
for i=1:length(StimOff)
line([StimOff_dark(i) StimOff_dark(i)], yL, 'Color', 'r');
line([StimOnSet_dark(i) StimOnSet_dark(i)], yL, 'Color', 'g');
end
% for light
yL = [-1 4];
fig = figure('Name','Pupil During Light Test'); 
k=plot(timeStampAll_light,rightEyeAll_light(:,12));
set(k, 'Color', 'm')
hold on
q=plot(timeStampAll_light,leftEyeAll_light(:,12));
set(q, 'Color', 'b')
for i=1:length(StimOff)
line([StimOff_light(i) StimOff_light(i)], yL, 'Color', 'r');
line([StimOnSet_light(i) StimOnSet_light(i)], yL, 'Color', 'g');
end

%for reversal learning


