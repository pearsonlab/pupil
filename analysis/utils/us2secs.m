function out = us2secs(t, t0)
% convert microsecond tobii integer timestamps to seconds
% optionally, shift by reference time t0
% is assumed

if ~exist('t0', 'var')
    t0 = 0;
end

switch class(t0)
    case 'uint64'
        out = double(uint64(t) - t0)/1e6;
    case 'double'
        out = (double(t) - t0)/1e6;
end