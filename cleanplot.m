%%%% Hello world! Little tiny plotting function. 
function cleanplot(filename)

datamat = repmat((NaN), length(eyedata.lefteye),3); % this creates a matrix with the size of the eyedata full of NaN


%tobii gives bad eye data back as a -1 or 4 in column 13 of the eye data matrix, so this ensures
%that all of the bad eye data is now considered a NaN
eyedata.lefteye(eyedata.lefteye(:,13)~=0,12) = NaN;
eyedata.righteye(eyedata.righteye(:,13)~=0,12) = NaN;

%get timestamp into a signed time so that it can be used
eyedata.timestamp=int64(eyedata.timestamp);
%eyedata.timestamp=(eyedata.timestamp-(datamat(1,3))/1000000

%create a matrix of 3 columns with left, right, and timestamp
datamat(:,1)=eyedata.lefteye(:,12);
datamat(:,2)=eyedata.righteye(:,12);
datamat(:,3)=eyedata.timestamp;

%switch type
    
%case oddball
    odd.sound=data(find(trialvec(1,:)==1));%find the trials where an oddball occurred
    plot((datamat(:,1)+(datamat(:,2)))/2); %plot the average of the left and right pupil
    hold on
%this will draw a vertical line marking when a sound occurred. 
    for ind=1:length(data);
        for i=1:length(datamat);
        tofindbins(i,ind)=data(ind).soundtime-datamat(i,3);
        
        [n timebin]=min(abs(tofindbins(:,ind))); % find the bin with the least difference between soundtime and bintime.
        line([timebin timebin],[(min(eyedata.lefteye(:,12))-0.5) max(eyedata.lefteye(:,12)+0.5)]);
             
      end
    end
    
    for i=1:length(datamat);
 % this will draw red vertical lines at oddball time points
 for ind=1:length(odd.sound);
        
        oddbins(i,ind)=odd.sound(ind).soundtime-datamat(i,3);
        
        [n oddbin(ind)]=min(abs(oddbins(:,ind)));
        y = line([oddbin(ind) oddbin(ind)],[(min(eyedata.lefteye(:,12))-0.5) max(eyedata.lefteye(:,12)+0.5)]);
        set(y, 'Color', 'r');     
      end
    end
    
  
case lightdark
    
     chopmat=[];
     
%%this spits out the bins that contain the position of each onset of the
%%stimulus
for ind = 1:length(data);
for i=1:length(datamat);
differenceontime(i)=data(ind).ontime-(datamat(i,3));
end
[n onbin(ind)]=min(abs(differenceontime));
chopmat(:,ind)=datamat((onbin(ind)-60):(onbin(ind)+120),1); %%since the tracker takes stamps at a rate of 60Hz this finds a second before the stimulus onset and 2 seconds after
chopmat(:,ind+3)=datamat((onbin(ind)-60):(onbin(ind)+120),2);
end

chopmat(:,7)=(chopmat(:,1)+chopmat(:,4)/2); %these are the average of left and right eye
chopmat(:,8)=(chopmat(:,2)+chopmat(:,5)/2);
chopmat(:,9)=(chopmat(:,3)+chopmat(:,6)/2);
plot(chopmat(:,7:9));




