%setup_geometry
%get screen resolution and define useful locations (origin, text locations,
%etc.) with respect to it

%get screen resolution
res_info=Screen('Resolution',which_screen);
horz=res_info.width;
vert=res_info.height;

%set various convenient screen locations (0,0) is upper-left monitor corner
% basic rectangles
origin = [horz/2 vert/2];
text_origin = origin - [45 25];
origin2=[origin origin];
baserect=minrad*[-1 -1 1 1]; %rectangle of cue
opt_loc_L=origin+[-250 200];
opt_loc_R=origin+[250 200];

cue_color=[[255 200 0];...
    [255 102 0]; ...
    [255  0 0]; ...
    [150 150 150]];

state.txtpos=text_origin;
state.Lpos=opt_loc_L;
state.Rpos=opt_loc_R;

%progress bar
pbar_hoffset=100;
pbar_voffset=100;
pbar_thick=50;
pbar_UL=[0 vert]+[pbar_hoffset -pbar_voffset-pbar_thick]; %lower left corner of pbar
pbar_LR=[horz vert]+[-pbar_hoffset -pbar_voffset];
state.pbar=[pbar_UL pbar_LR];

min_vpos=origin(2)-100;
max_vpos=0+30;