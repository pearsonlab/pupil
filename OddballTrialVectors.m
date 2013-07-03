%%%%function to create an order for Oddball
function [oddtrialvec]=OddballTrialVectors(mode, ntrials)
cond_check=1;
clear vectors;
clear ntrials;
clear numhigh;
ntrials = input('input number of trials:  ');
numhigh = floor(ntrials/5);

switch mode
    case 0 %%generates a new vector
while cond_check==1;
   %%%% Randomization %%%%
oddtrialvec = zeros(length(ntrials),1);
oddtrialvec(randperm(ntrials,numhigh),1)=1;

% Run Length Code %
checkgood=[([oddtrialvec(diff(oddtrialvec) ~= 0)' oddtrialvec(end)]') (diff([0 find(diff(oddtrialvec) ~= 0)' length(oddtrialvec)])')];

%%checks to see if the vector is nice
b=checkgood(:,1)==0 & checkgood(:,2)< 2; 
c=checkgood(:,1)==1 & checkgood(:,2) >= 2 ;
if sum(b) || sum(c) > 0
    cond_check=1;
else
    cond_check=0;
end
      
end
    case 1 %%loads a previously created vector THAT I am going to make right now
       'HERE IS A PRETTY VECTOR'
        
end

