%%%% Hello world! Little tiny plotting function. 
function cleanplot(filename)
 
% Create a NaN matrix the size of eyedata
datamat = repmat((NaN), length(eyedata.lefteye),3); 
 
%tobii gives bad eye data back as a -1 or 4 in column 13 of the eye data matrix, so this ensures
%that all of the bad eye data is now considered a NaN
eyedata.lefteye(eyedata.lefteye(:,13)~=0,12) = NaN;
eyedata.righteye(eyedata.righteye(:,13)~=0,12) = NaN;
 
%get timestamp into a signed time so that it can be used
eyedata.timestamp=int64(eyedata.timestamp);
%eyedata.timestamp=(eyedata.timestamp-(datamat(1,3))/1000000
 
%Replace NaN matrix with 3 columns of the same length to be plotted: left, right, and
%timestamp
datamat(:,1)=eyedata.lefteye(:,12);
datamat(:,2)=eyedata.righteye(:,12);
datamat(:,3)=eyedata.timestamp;
 
%plot the average of the left and right pupil
plot((datamat(:,1)+(datamat(:,2)))/2);
hold on
 
%switch type
    %case oddball
        %find the trials where an oddball occurred
        odd.sound=data(find(trialvec(1,:)==1));
        
        %draw a vertical line where a sound occurred
        for ind=1:length(data);
            for i=1:length(datamat);
                tofindbins(i,ind)=data(ind).soundtime-datamat(i,3); 
                
                % find the bin with the least difference between soundtime and bintime.
                [n timebin(ind)]=min(abs(tofindbins(:,ind)));
                % find 1 second before, 2 seconds after normal sounds
                chopmat_norm(:,ind+3)=datamat((timebin(ind)-60):(timebin(ind)+120),2);
                % plot vertical lines
                %line([timebin(ind) timebin(ind)],[(min(eyedata.lefteye(:,12))-0.5) max(eyedata.lefteye(:,12)+0.5)]);
            end
        end
        
        for i=1:length(datamat);
            % this will draw red vertical lines at oddball time points
            for ind=1:length(odd.sound);
        
            oddbins(i,ind)=odd.sound(ind).soundtime-datamat(i,3);
        
            [n oddbin(ind)]=min(abs(oddbins(:,ind)));
            % find 1 second before, 2 seconds after oddball sounds
            chopmat_odd(:,ind+3)=datamat((oddbin(ind)-60):(oddbin(ind)+120),2);
            % plot vertical lines
            %y = line([oddbin(ind) oddbin(ind)],[(min(eyedata.lefteye(:,12))-0.5) max(eyedata.lefteye(:,12)+0.5)]);
            %set(y, 'Color', 'r');     
            end
        end
        
        % plot averaged normal trials and averaged oddball trials - take 1
        % second before and 2 seconds after
        
        
        figure;
        
       
        %case revlearn

        for i=1:length(data);
            ctrials(i)=data(i).correct==1;
            mtrials(i)=data(i).correct==0;
      end

mispos=find(mtrials==1);
corpos=zeros(1,length(data));
corpos(mispos)=1;

for q=1:length(mispos);
for z=1:length(datamat);
ze(z,q)=data(mispos(q)).soundtime-datamat(z,3);
end
[num pos(q)]=min(abs(ze(:,q)));
%revlearnmat(:,q)=datamat((onbin(ind)-60):(onbin(ind)+120),2);
end

revlearnmat=datamat((pos(q)-60):(pos(q)+120),1); %%since the tracker takes stamps at a rate of 60Hz this finds a second before the stimulus onset and 2 seconds after

for w=1:length(corpos);
    for t=1:length(datamat);
    if corpos(w)==0
        qw(w,t)=data(w).soundtime-datamat(t,3);
    else
        qw(w,t)=NaN;
    end
    end
end

   % case lightdark
    
        chopmat=[];
     
        %%this spits out the bins that contain the position of each onset of the
        %%stimulus
        for ind = 1:length(data);
            for i=1:length(datamat);
            differenceontime(i)=data(ind).ontime-(datamat(i,3));
            end
        [n onbin(ind)]=min(abs(differenceontime));
         %%since the tracker takes stamps at a rate of 60Hz this finds a second before the stimulus onset and 2 seconds after

