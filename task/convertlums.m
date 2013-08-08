function [RBGconv,lumtoRBG] = convertlums(RBGval)
lumens_max = 118.877; % Max luminance measure value based on Spyder
RBG_max = 255; % Max RBG value

lumens_real = (lumens_max*RBGval)/RBG_max; % Find lumen value corresponding to % max luminance we want
% RBGtolum(x) = 0.002*(x^2)-(0.01717*x)+1.3493;
lumtoRBG = 250*(lumens_real/125 - 104995911/10000000000)^(1/2) + 1717/400; % inverse - convert lumens to RBG
RBGconv = [lumtoRBG lumtoRBG lumtoRBG];
end

