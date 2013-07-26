function DrawEyes(win, left_w_camera, left_h_camera, right_w_camera, right_h_camera, left_validity, right_validity )
%DrawEyes(win, w_camera, h_camera, left_validity, right_validity)
%
% w_camera: Left eye position seen by the camera.
%           0.0 is leftmost and 1.0 is rightmost.
% h_camera: Left eye position seen by the camera.
%           0.0 is topmost and 1.0 is bottommost.
% validity: How likely is it that the left eye was found? 
%           0 - Certainly (>99%),
%           1 - Probably (80%),
%           2 - (50%),
%           3 - Likely not (20%),
%           4 - Certainly not (0%) 


LCamW = left_w_camera;
RCamW = right_w_camera;
LCamH = left_h_camera;
RCamH = right_h_camera;

%estimate screen dimension
screenNumber=Screen('WindowScreenNumber', win);
res=Screen('Rect', screenNumber);
res = res(3:4);

%use one square display proportional to the screen resolution
width = 0.2*res(1);
height = width;%0.2*res(2);

%draw rectangles
rectWin(1) = res(1)/2-width/2;
rectWin(2) = res(2)/2-height/2;
rectWin(3) = res(1)/2+width/2;
rectWin(4) = res(2)/2+height/2;
color_frame = [0 0 0 ];


Screen( 'FillRect',win,color_frame,rectWin );

%draw eyes
%decide color
switch left_validity
    case 0,
        color_leftEye = [0 255 0];
    case 1, 
        color_leftEye = [64 192 0];
    case 2,
        color_leftEye = [128 128 0];
    case 3,
        color_leftEye = [192 64 0];
    otherwise,
        color_leftEye = [255 0 0];
end

switch right_validity
    case 0,
        color_rightEye = [0 255 0];
    case 1, 
        color_rightEye = [64 192 0];
    case 2,
        color_rightEye = [128 128 0];
    case 3,
        color_rightEye = [192 64 0];
    otherwise,
        color_rightEye = [255 0 0];
end

pupil_size = 0.1*width;
if( left_validity<4)
    LwC = rectWin(1) + width*LCamW;
    LhC = rectWin(2) + height*LCamH;
    rectOvalL(1) = LwC - pupil_size/2;
    rectOvalL(2) = LhC - pupil_size/2;
    rectOvalL(3) = LwC + pupil_size/2;
    rectOvalL(4) = LhC + pupil_size/2;
    Screen('FillOval',win, color_leftEye,rectOvalL);
end

if(right_validity<4)
    RwC = rectWin(1) + width*RCamW;
    RhC = rectWin(2) + height*RCamH;
    
    rectOvalR(1) = RwC - pupil_size/2;
    rectOvalR(2) = RhC - pupil_size/2;
    rectOvalR(3) = RwC + pupil_size/2;
    rectOvalR(4) = RhC + pupil_size/2;

    Screen('FillOval',win, color_rightEye,rectOvalR);
end


%flip
Screen('Flip', win );
