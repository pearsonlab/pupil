function [RGBconv] = convertlums(RGBval)
lumens_max = 118.877; % Max luminance measure value based on Spyder
RGBval = RGBval;
RGB_max = 255; % Max RBG value

lumens_real = RGBval/RGB_max;% Find normalized lumen value corresponding to % max luminance we want
% RBGtolum(x) = 1.1197508*(x^2) - (0.1538355*x) + 0.0113504
lumtoRGB = (2251799813685248*((5042909285627815*lumens_real)/1125899906842624 - 35272722328531464996282178689579/1298074214633706907132624082305024)^(1/2))/5042909285627815 + 5542508003810831/80686548570045040; % inverse - convert lumens to RBG
if lumtoRGB > 1
    lumtoRGB = 1
end
RGBconv = 255*[lumtoRGB lumtoRGB lumtoRGB];

end

