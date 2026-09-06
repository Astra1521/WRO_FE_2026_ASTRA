% =========================================================
% speed_lap_analysis.m
% WRO Future Engineers — Speed & Lap Time Analysis
%
% Calculates:
%   1. Estimated linear speed from EV3 medium motor specs
%   2. Back-calculates actual speed from measured 8.7 s lap time
%   3. Track perimeter geometry (WRO 2025 mat: 3m × 3m)
%   4. Energy budget from 12 V Bonka battery
%   5. Lap time vs motor speed sensitivity
% =========================================================

clear; clc; close all;
run('robot_params.m');

%% ── 1. EV3 Medium Motor Speed Estimates ─────────────────
% EV3 Medium Motor datasheet:
%   Free-run:  ~240–260 rpm @ 9 V
%   At 12 V (scaled):  ~320 rpm free-run
%   Stall torque:  8 N·cm
%   Running torque (≈50% load): ~4 N·cm

RPM_12V_FREE  = 320;    % rpm  @ 12 V, no load
RPM_12V_LOAD  = 220;    % rpm  @ 12 V, with differential + friction loss

V_free = RPM_12V_FREE  / 60 * WHEEL_CIRCUMFERENCE;   % mm/s
V_load = RPM_12V_LOAD  / 60 * WHEEL_CIRCUMFERENCE;   % mm/s

fprintf('=== Speed Estimates ===\n');
fprintf('  Wheel circumference   : %.1f mm\n', WHEEL_CIRCUMFERENCE);
fprintf('  Free-run speed @12V   : %.0f mm/s  (%.2f m/s)\n', V_free, V_free/1000);
fprintf('  Loaded speed @12V     : %.0f mm/s  (%.2f m/s)\n', V_load, V_load/1000);

%% ── 2. WRO Mat Geometry ──────────────────────────────────
% Official WRO 2025 Future Engineers mat: 3000 × 3000 mm
% Inner track boundary — car must stay within the track.
% Track consists of 4 straights + 4 corners.
% Typical inner-wall clearance for wall-following at 180 mm:
%   Track is 1000 mm wide (approx), wall at 180 mm → robot centre 180 mm from wall

MAT_SIZE      = 3000;   % mm
WALL_OFFSET   = 180;    % mm from inner wall (TARGET_DISTANCE)

% Robot path perimeter (approximate rectangle, wall-following at 180 mm)
% Path = along the outer wall, 180 mm offset
% Inner edge of track ≈ 1000 mm border → robot path ≈ 1000 + 180 = 1180 from centre
inner_path_L   = MAT_SIZE - 2 * 1000;  % inner free space ≈ 1000 mm
outer_path_dim = inner_path_L + 2 * WALL_OFFSET;  % robot centre path size

% Perimeter (4 straight sides + 4 corner arcs at ~R_corner)
R_corner   = 330;   % mm  WRO standard corner radius
straight_L = outer_path_dim - 2 * R_corner;
perimeter  = 4 * straight_L + 2 * pi * R_corner;  % one lap

fprintf('\n=== Track Geometry ===\n');
fprintf('  Mat size               : %g × %g mm\n', MAT_SIZE, MAT_SIZE);
fprintf('  Robot path dimension   : ~%.0f mm square\n', outer_path_dim);
fprintf('  Estimated 1-lap length : %.0f mm  (%.2f m)\n', perimeter, perimeter/1000);

%% ── 3. Back-Calculate Speed from 8.7 s Lap Time ─────────
LAP_TIME_S = 8.7;   % seconds — measured value
LAPS       = 3;

speed_measured = perimeter / LAP_TIME_S;   % mm/s for 1 lap

fprintf('\n=== Speed from Measured Lap Time ===\n');
fprintf('  Measured lap time      : %.1f s\n', LAP_TIME_S);
fprintf('  Estimated track length : %.0f mm\n', perimeter);
fprintf('  Derived avg speed      : %.0f mm/s  (%.2f m/s)\n', ...
        speed_measured, speed_measured/1000);

% Compare to motor estimate
fprintf('\n  Motor free-run speed   : %.0f mm/s\n', V_free);
fprintf('  Motor loaded speed     : %.0f mm/s\n', V_load);
fprintf('  Speed utilisation      : %.0f %% of free-run\n', ...
        100 * speed_measured / V_free);

%% ── 4. Lap Time vs Speed Sensitivity ────────────────────
speeds = 400 : 50 : 1200;  % mm/s
lap_times = perimeter ./ speeds;

figure('Name','Lap Time vs Speed','NumberTitle','off','Color','w','Position',[100 100 800 400]);

plot(speeds, lap_times, 'b-', 'LineWidth', 2); hold on;
xline(speed_measured, '--g', sprintf('Measured avg (%.0f mm/s)', speed_measured), ...
      'LabelVerticalAlignment','bottom');
xline(V_load, '--r', sprintf('Est. loaded motor (%.0f mm/s)', V_load), ...
      'LabelVerticalAlignment','bottom');
yline(LAP_TIME_S, ':k', sprintf('%.1f s target', LAP_TIME_S));

scatter(speed_measured, LAP_TIME_S, 100, 'g^', 'filled');

xlabel('Average Robot Speed (mm/s)');
ylabel('Lap Time (s)');
title('Lap Time Sensitivity — Speed vs Time @ WRO Track');
grid on;
legend('Lap time curve','Location','northeast');

%% ── 5. Energy Budget ─────────────────────────────────────
% EV3 Medium Motor: rated ~2.2 W mechanical output
% Electrical input ≈ motor_power / efficiency
MOTOR_EFF   = 0.65;      % ~65% efficiency for small DC motor
P_mech      = 2.2;       % W
P_elec      = P_mech / MOTOR_EFF;   % W
P_servo     = 0.5;       % W (typical small servo)
P_sensors   = 3 * 0.05;  % W (3 × VL53L0X ≈ 50 mW each)
P_pi        = 3.0;       % W (Raspberry Pi Zero 2W typical)
P_pca       = 0.1;       % W (PCA9685 PWM driver)

P_total = P_elec + P_servo + P_sensors + P_pi + P_pca;

% Bonka 12 V LiPo — typical 1000–1300 mAh for FE-class packs
BATT_CAPACITY_MAH = 1300;   % mAh (conservative estimate)
I_draw    = P_total / BATTERY_VOLTAGE;   % A
runtime_h = BATT_CAPACITY_MAH / 1000 / I_draw;
runtime_m = runtime_h * 60;
total_laps = runtime_m * 60 / LAP_TIME_S;

fprintf('\n=== Energy Budget ===\n');
fprintf('  Motor electrical power : %.1f W\n', P_elec);
fprintf('  Servo power            : %.1f W\n', P_servo);
fprintf('  Sensors × 3            : %.2f W\n', P_sensors);
fprintf('  Raspberry Pi           : %.1f W\n', P_pi);
fprintf('  PCA9685 driver         : %.1f W\n', P_pca);
fprintf('  TOTAL draw             : %.2f W\n', P_total);
fprintf('  Current draw           : %.0f mA @ 12 V\n', I_draw*1000);
fprintf('  Est. runtime           : %.0f min  (%.0f laps of 8.7 s)\n', ...
        runtime_m, total_laps);

% Power breakdown pie chart
figure('Name','Power Budget','NumberTitle','off','Color','w','Position',[200 200 550 440]);
labels = {'Motor','Servo','Sensors','Raspberry Pi','PCA9685'};
vals   = [P_elec, P_servo, P_sensors, P_pi, P_pca];
explode = [1 0 0 0 0];
pie(vals, explode, labels);
title(sprintf('Power Budget — %.1f W Total @ %g V', P_total, BATTERY_VOLTAGE));
colormap(lines(5));

fprintf('\nDone. See figures for speed and energy analysis.\n');
