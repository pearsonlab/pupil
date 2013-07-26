%process_lighttest.m
%process tobii data from lighttest.m, which performs a test of the
%pupillary light reflex

%% go to data directory
cd('/data/pupil')
addpath('/matlab/pupil/code/TESTER')
ls('/data/pupil')
%% 
DataDir = input('\n What Directory would you like to open for analysis?:   \n \n','s');
display('   ')
display('   ')

ls(DataDir)
cd(DataDir)

%% get data
DataFile = input('\n \n Full file name with extension of the Data file to be analyzed?:   \n \n ','s');
EventFile = input('\n \n Full file name with extension of the Event file to be analyzed?:   \n \n ','s');

ltodt = input('\n \n lighttest or darktest? (lt/dt):   ', 's');

eyedat=dlmread(DataFile,'');

formatstr ='%[^123456789.] %f %f'; %read all characters until the first number, then two numbers
fid=fopen(EventFile);
evtdat=textscan(fid,formatstr);
fclose(fid);

%strip extra spaces from events
evtdat{1}=cellfun(@strtrim,evtdat{1},'UniformOutput',0);

%% take care of clock differential
%because local (talk2tobii) and tobii (TET) clocks are synchronized, we
%only need to subtract an absolute value from each
eyetime_abs=eyedat(:,1)+1e-6*eyedat(:,2); %first col is seconds, second microseconds
eyetime=eyetime_abs-eyetime_abs(1); %tobii time relative to recording start
local_offset=evtdat{2}(1); %corresponds to #START command from talk2tobii
evttime=evtdat{2}-local_offset; %event times relative to task start

%% get relevant event times
stim_on = evttime(strcmp('stim on',evtdat{1}));
stim_off= evttime(strcmp('stim off',evtdat{1}));
tgrab=5; %number of seconds of data to grab

lpup=eyedat(:,13); %left pupil diameter
rpup=eyedat(:,14); %right pupil diameter

%loop over stims, grab data for pupil size each eye
pseries=cell(length(stim_on),2); %time series for pupil measures
bseries=cell(length(stim_on),2); %time series for pre-reflex baseline
for ind=1:length(stim_on)
    %response time series
    sel=(eyetime > stim_on(ind)) & (eyetime <= (stim_on(ind)+tgrab));
    pseries{ind,1}=lpup(sel);
    pseries{ind,2}=rpup(sel);
    
    %baseline time series
    sel=(eyetime > stim_on(ind)) & (eyetime <= stim_off(ind));
    bseries{ind,1}=lpup(sel);
    bseries{ind,2}=rpup(sel); 
end

%clean up
pbseries=cell(size(pseries));
for ind=1:numel(pseries)
    pseries{ind}(pseries{ind}==-1)=NaN; %replace 0 pupil measurements with nans
    
    pbseries{ind}=pseries{ind}-nanmean(bseries{ind}); %pupil series corrected for baseline
end
%% try some plotting
%raw plots
clf
hold all
for ind=1:numel(pseries)
    plot(pseries{ind},'linewidth',2)
end

%% adjusting for baseline
clf
hold all
for ind=1:numel(pseries)
    plot(pbseries{ind},'linewidth',2)
end


%% averaging across eyes
clf
hold all
for ind=1:size(pseries,1)
    peff{ind}=nanmean([pseries{ind,1} pseries{ind,2}],2);
    plot(peff{ind},'linewidth',2)
end

%% averaging across eyes, baseline adjusted
dt=1/60; %eyetracker runs at 60Hz
clf
hold all
for ind=1:size(pseries,1)
    peff{ind}=nanmean([pbseries{ind,1} pbseries{ind,2}],2);
    taxis=dt:dt:(length(peff{ind})*dt);
    taxis = taxis';
    plot(taxis,peff{ind},'linewidth',2)
end
if strcmp(ltodt, 'lt') ==1 || strcmp(ltodt, 'LT')
    legend('0.25','0.5','0.75','1', 0)
    legd = [0.25, 0.50, 0.75, 1];
end
xlabel('Time (s)')
ylabel('Pupil Diameter Change (mm)')

%% Nonlinear Fitting
disp( 'scaling * t ^ (tpeak/Beta) * exp(- t / Beta) + Verticle translation')
% initA = input('\n Based on the above graphs give your best guess \n to the scaling of the pupillary response: ');
% initB = input('\n Based on the above graphs give your best guess \n to the Verticle translation of the pupillary response: ');
% inittpeak = input('\n Based on the above graphs give your best guess \n to the tpeak value of the fitted Gamma distribution: ');
% initbeta = input('\n Based on the above graphs give your best guess \n to the beta value of the fitted Gamma Distribution: ');

GammaHandle =@ (GAMA, x) (GAMA(1).*x.^(GAMA(2)./GAMA(3)).*exp(-x./GAMA(3))+GAMA(4));
for ind=1:size(peff, 2)
    Ia = []; Ib = []; v = []; bchg = [];
    taxis=dt:dt:(length(peff{ind})*dt);
    taxis = taxis';
    [v, Ia] = min(peff{ind}(find(taxis==0.75):find(taxis==dt.*67)));
    Ia = Ia + find(taxis == 0.75);
    inittpeak = taxis(Ia);
    initB = nanmean(peff{ind});
    bchg = v  - ((v - nanmean(peff{ind}))*0.7);
    Ib = find(diff(find(peff{ind} < bchg))> 16);
    Ib = Ib(Ib > Ia);
    if isempty(Ib) == 1
        Ib = find(peff{ind} < bchg); Ib = Ib(end);
        initbeta = taxis(Ib(1)) - inittpeak;
    else
        initbeta = taxis(Ib(1)) - inittpeak;
    end
    initA = -1.*range(peff{ind}).*10;
[GAMMA(ind,:), R, J, CovG(:, :, ind), MSE(ind, :)] = nlinfit(taxis, peff{ind}, GammaHandle, [initA, inittpeak, initbeta, initB]);
end

A = GAMMA(:,1);
tpeak = GAMMA(:,2);
beta = GAMMA(:,3);
B = GAMMA(:,4);

dt=1/60; %eyetracker runs at 60Hz
figure(2); hold all
for ind=1:size(pseries,1)
    peff{ind}=nanmean([pbseries{ind,1} pbseries{ind,2}],2);
    taxis=dt:dt:(length(peff{ind})*dt);
    taxis = taxis';
    subplot(4, 1, ind)
    plot(taxis,peff{ind},'linewidth',2); hold on
    legd = [0.25, 0.50, 0.75, 1];
    plot(taxis, GammaHandle([A(ind), tpeak(ind), beta(ind), B(ind)], taxis), 'k-', 'linewidth', 1.5)
    xlabel('Time (s)'); ylabel('Pupil Diameter Change (mm)')
   title(sprintf('Pupillary response model for brightness %1.2f', legd(ind)))
end


%% Revert to start directory
cd('/matlab/pupil/code/TESTER')