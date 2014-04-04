function out = basenorm(dmat, taxis, Tint, type)
% for a data matrix dmat with multiple data series, each indexed by taxis,
% normalize by the mean value (within each series) between
% the time points given in the two-element interval [ Tint(1), Tint(2) ) 
% type = 0 (default) for subtractive normalization; = 1 for divisive

if ~(Tint(2) > Tint(1))
    warning('Normalizing epoch endpoint must be after start point.')
end

if ~exist('type', 'var')
    type = 0;
end

% first, find which axis of dmat taxis corresponds to
n = length(taxis);
[p, q] = size(dmat);

% fix it so that series are along columns
% if matrix is square, *assume* series are columns
if n == p
    D = dmat;
    isflipped = 0;
elseif n == q
    D = dmat';
    isflipped = 1;
else
    warning('Dimensions of data matrix do not match indexing axis.')
end

sel = (taxis >= Tint(1)) & (taxis < Tint(2));

B = D(sel, :);
baseline = nanmean(B);

switch type
    case 0
        Dnorm = bsxfun(@minus, D, baseline);
    case 1
        Dnorm = bsxfun(@rdivide, D, baseline);
end

if isflipped
    out = Dnorm';
else
    out = Dnorm;
end

