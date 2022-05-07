%% Load Filters
HRTF = load('hrir_final');
Fs = 44100;

%% Elevation and Azimuth Angles
elevations = -45 + 5.625*(0:49);
azimuth = [-80 -65 -55 -45:5:45 55 65 80];

%% Horizontal Plane Indice

el_front = 0;
el_behind = 180;
el_ind_front = find(elevations == el_front);
el_ind_behind = find(elevations == el_behind);

%% 8 directions
% Indice 1 is directly front
% Goes clock wise
% 8 equispaced points
% pairs
% (az,el)
% (0,0) 
% (45,0)
% (90,0) (Take average of (80,0) and (-80,180)
% (-45,180)
% (0,180)
% (45,180)
% (-90,0) (Take average of (-80,0) and (80,180)
% (-45,0)


az = [13,22,25,25,22,13,4,1,1,4];
el = [el_ind_front*ones(1,3),el_ind_behind*ones(1,4),el_ind_front,el_ind_behind,el_ind_front];

%% Get the filters

h_left_full = HRTF.hrir_l;
h_right_full = HRTF.hrir_r;

h_left = zeros(10,200);
h_right = zeros(10,200);
for i=1:10
    h_left(i,:) = h_left_full(az(i),el(i),:);
    h_right(i,:) = h_right_full(az(i),el(i),:);
end

h_l = h_left([1:3,5:8,10],:);
h_r = h_right([1:3,5:8,10],:);
% h_l(3,:) = 0.5*(h_left(3,:) + h_left(4,:));
% h_l(7,:) = 0.5*(h_left(8,:) + h_left(9,:));
% h_r(3,:) = 0.5*(h_right(3,:) + h_right(4,:));
% h_r(7,:) = 0.5*(h_right(8,:) + h_right(9,:));


%% Save to load at python

save left_filt.mat h_l
save right_filt.mat h_r
