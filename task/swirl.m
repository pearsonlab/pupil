function StimulusOnsetTime=swirl(win, totTime, ifi, when0, position)
% StimulusOnsetTime=swirl(win,totTime,ifi,when0,position,flagTobii)
% This function draws a swirly pattern
% win is the window handle returned from psychtoolbox when it initializes
% the screen context that it draws in
% totTime is the time in seconds that the swirling pattern lasts
% ifi is the time returned by the Screen('GetFlipInterval') command
% when0 is the time to start displaying the swirly pattern
% position is the x, y screen coordinates of where to centre the swirly
% pattern
% flagTobii is used to decide whether to use on-line feedback about
% eyetracking data

rand('state',sum(100*clock));
pos = position;

rect=Screen('Rect',win);
cx = pos(1)*rect(3);
cy = pos(2)*rect(4);

global BACKCOLOR;
BACKCOLOR = [0 0 0];


dt = totTime/100;

decr = 1;
sides=floor(rand*3)+3;
color=round(rand(3,1)*255);
color(floor(rand*3)+1)=255;
dir=floor(rand*2)*2-1;
ainc=dir*2*pi*0.016;
angle=2*pi*rand;
size=100;

time01 = 0;
time02 = 0;

when = when0;
Screen('TextSize', win,20);
boundsText = Screen('TextBounds', win, '*');
for i=1:100
    RegPoly(win,sides,size,angle,color,cx,cy);
    Screen('DrawingFinished',win);
    size=round(size-decr);
    angle=angle+ainc;
    
    
    Screen('TextSize', win,20);
    Screen('DrawText', win, '*',cx-boundsText(3)/2,cy-boundsText(4)/2,[255 255 250]);
    
    [now StimulusOnsetTime FlipTimestamp Missed Beampos]= Screen('Flip',win, when);
    when = StimulusOnsetTime+dt-ifi;
end




%%
function RegPoly(win,sides,size,angle,color,cx,cy)

%cx=rect(3)/2;
%cy=rect(4)/2;
for i=1:sides
    vert(i,1)=cx+size*cos(angle+2*pi*(i-1)/sides);
    vert(i,2)=cy+size*sin(angle+2*pi*(i-1)/sides);
end
Screen('FillPoly', win, color, vert);
return
