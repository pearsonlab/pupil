% analyze_pst.m
% scratch code for analysis of pupillary sleep task

%% de-mean data
lpup = lpup - mean(lpup);
rpup = rpup - mean(rpup);

%% make power spectrum of each eye
Hs = spectrum.mtm(10); %multitaper spectrum object
lpsd=psd(Hs, lpup, 'Fs', sr);
rpsd=psd(Hs, rpup, 'Fs', sr);
lpwr = lpsd.data;
rpwr = rpsd.data;
ff=lpsd.frequencies;

figure(1)
hold all
plot(ff, 10*log10(lpwr))
plot(ff, 10*log10(rpwr))
title('Power spectral density of pupil fluctuations','fontsize', 20, 'fontweight', 'bold')
xlabel('Frequency (Hz)', 'fontsize', 16, 'fontweight', 'bold')
ylabel('Power (dB/Hz)', 'fontsize', 16, 'fontweight', 'bold')
legend({'Left eye', 'Right eye'})
hold off

%% now try time-frequency plots
freqs = 1:30; % transform takes longer, so use log-spaced frequencies

P = timefreq(lpup', freqs, sr);

% plot
figure(2)
pcolor(taxis, freqs, 10*log10(P)) %times is a vector of times
shading interp
set(gca,'ydir','normal')
xlabel('Time (s)')
ylabel('Frequency (Hz)')

%% instantaneous power
lpow = abs(hilbert(lpup)).^2;
rpow = abs(hilbert(rpup)).^2;

figure(3)
hold all
plot(taxis, 10*log10(lpow))
plot(taxis, 10*log10(rpow))
title('Instantaneous power of pupil fluctuations','fontsize', 20, 'fontweight', 'bold')
xlabel('Time (s)', 'fontsize', 16, 'fontweight', 'bold')
ylabel('Power (dB/Hz)', 'fontsize', 16, 'fontweight', 'bold')
legend({'Left eye', 'Right eye'})
hold off
