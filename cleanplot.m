%%%% Hello world! Little tiny plotting function. 
function cleanplot(filename)
addpath ('C:\Users\Anna\Desktop\Work\Duke Summer\data\part.7data')  %%this is specifically for Anna Leigh's computer, take this out!!!
load('filename')
 
hold on
datamat = repmat((NaN), length(eyedata.lefteye),3); % this creates a matrix with the size of the eyedata full of NaN


%tobii gives bad eye data back as a -1 or 4 or whatever, so this ensures
%that all of the bad eye data is now considered a NaN
eyedata.lefteye(eyedata.lefteye(:,13)~=0,12) = NaN;
eyedata.righteye(eyedata.righteye(:,13)~=0,12) = NaN;

%get timestamp into a signed time so that it can be used
eyedata.timestamp=int64(eyedata.timestamp);
%eyedata.timestamp=(eyedata.timestamp-(datamat(1,3))/1000000

%create a matrix with left, right, and timestamp
datamat(:,1)=eyedata.lefteye(:,12);
datamat(:,2)=eyedata.righteye(:,12);
datamat(:,3)=eyedata.timestamp;

chopmat=[];
%%this spits out the bins that contain the position of each onset of the
%%stimulus
for ind = 1:length(data)
for i=1:length(datamat)
d(i)=data(ind).ontime-(datamat(i,3));
end
[n onbin(ind)]=min(abs(d));
chopmat(:,ind)=datamat((onbin(ind)-60):(onbin(ind)+120),1)
end



% switch type
%     case oddball
%data(find(trialvec(1,:)==1)) %find the trials where an oddball occured


plot(datamat(:,3),datamat(:,1));
set((plot(datamat(:,3),datamat(:,2))), 'Color', 'r');

