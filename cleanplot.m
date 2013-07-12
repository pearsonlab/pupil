%%%% Hello world! Little tiny plotting function. 
function cleanplot(filename)
load('filename')
 
hold on
datamat = repmat((NaN), length(eyedata.lefteye),3); % this creates a matrix with the size of the eyedata full of NaN


%tobii gives bad eye data back as a -1 or 4 or whatever, so this ensures
%that all of the bad eye data is now considered a NaN
eyedata.lefteye(eyedata.lefteye(:,13)~=0,12) = NaN;
eyedata.righteye(eyedata.righteye(:,13)~=0,12) = NaN;

%get timestamp into a signed time so that it can be used
eyedata.timestamp=int64(eyedata.timestamp);

%create a matrix with left, right, and timestamp
datamat(:,1)=eyedata.lefteye(:,12);
datamat(:,2)=eyedata.righteye(:,12);
datamat(:,3)=eyedata.timestamp;


% switch type
%     case oddball
data(find(trialvec(1,:)==1)) %find the trials where an oddball occured


plot(datamat(:,3),datamat(:,1));
set((plot(datamat(:,3),datamat(:,2))), 'Color', 'r');

