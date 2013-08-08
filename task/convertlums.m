function [RGBconv] = convertlums(RGBval)
% Takes input of the RGB value we want and spits out the value of the RGB
% we actually need to use to get the luminance we originally wanted. (Due
% to computer's luminance issues).

lumens_max = 118.877; % Max luminance measure value based on Spyder
RGBval = RGBval;
RGB_max = 255; % Max RBG value

lumens_real = RGBval/RGB_max;% Find normalized lumen value corresponding to % max luminance we want
% RBGtolum(x) = 1.1347695*(x^2) - (0.1645912*x) + 0.0123075
lumtoRGB = (562949953421312*((1277636874337851*lumens_real)/281474976710656 - 9337839445892667871051724163069/324518553658426726783156020576256)^(1/2))/1277636874337851 + 988337155984617/13628126659603744; % inverse - convert lumens to RBG
if lumtoRBG > 1
    lumtoRBG = 1
end

RGBconv = 255*[lumtoRGB lumtoRGB lumtoRGB];

end

