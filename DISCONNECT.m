function [] = disconnect()
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here

hostName = '169.254.225.234';

talk2tobii('STOP_TRACKING');
WaitSecs(0.5);
talk2tobii('DISCONNECT');
WaitSecs(0.5);
tstatus


end

