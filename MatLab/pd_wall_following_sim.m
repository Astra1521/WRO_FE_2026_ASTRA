% =========================================================
% pd_wall_following_sim.m
% WRO Future Engineers — PD Wall-Following Controller Simulation
%
% Mirrors the EXACT PD logic from main_open.py:
%
%   if error > 0:   KP = KP_NEAR   (too close → strong correction)
%   else:           KP = KP_FAR    (too far   → gentle correction)
%   steering = KP*error + KD*derivative
%   angle    = SERVO_CENTER ± steering   (sign flips for right wall)
%
% Use this to:
%   • Compare KP_NEAR / KP_FAR / KD without touching the robot
%   • Show judges the thought process behind your chosen gains
%   • Spot oscillation or sluggish response before competition
%
% Run robot_params.m first (loaded automatically below).
% =========================================================

clear; clc; close all;
run('robot_params.m');

%% ── Tunable Parameters (copy from main_open.py) ──────────
TARGET_DISTANCE  = 180;    % mm  — desired wall distance
KP_NEAR          = 0.65;   % gain when robot is TOO CLOSE (error > 0)
KP_FAR           = 0.30;   % gain when robot is TOO FAR   (error < 0)
KD               = 0.02;   % derivative gain

SERVO_MIN  =  50;
SERVO_CEN  =  95;
SERVO_MAX  = 140;

%% ── Simulation Setup ─────────────────────────────────────
dt        = 0.015;                  % control loop period (seconds)
T_total   = 8.0;                    % simulate 8 s (one WRO mat lap)
t         = 0 : dt : T_total;
N         = length(t);

% Disturbance profile: robot starts 250 mm away, hits corners,
% then wall disappears briefly (corner) and comes back.
%   Segment 1 (0–2 s)   : far from wall, approaches
%   Segment 2 (2–3.5 s) : on target
%   Segment 3 (3.5–4 s) : corner — sensor reads 800 mm (open space)
%   Segment 4 (4–5.5 s) : back on target
%   Segment 5 (5.5–6 s) : corner
%   Segment 6 (6–8 s)   : final straightaway

wall_true = zeros(1, N);
for i = 1:N
    ti = t(i);
    if     ti < 2.0,                wall_true(i) = 250 - 35*ti;
    elseif ti < 3.5,                wall_true(i) = TARGET_DISTANCE + 5*sin(4*pi*ti);
    elseif ti < 4.0,                wall_true(i) = 700;          % corner
    elseif ti < 5.5,                wall_true(i) = TARGET_DISTANCE + 3*sin(3*pi*ti);
    elseif ti < 6.0,                wall_true(i) = 700;          % corner
    else,                           wall_true(i) = TARGET_DISTANCE + 2*sin(2*pi*ti);
    end
end

% Add realistic ToF sensor noise (±5 mm std-dev)
rng(42);
sensor_noise = 5 * randn(1, N);
wall_measured = wall_true + sensor_noise;

%% ── PD Controller Loop ───────────────────────────────────
servo_angle  = zeros(1, N);
error_log    = zeros(1, N);
kp_used      = zeros(1, N);
prev_error   = 0;

for i = 1:N
    d = wall_measured(i);

    % Skip corner readings (sensor out of range)
    if d > 600
        servo_angle(i) = SERVO_CEN;
        error_log(i)   = 0;
        kp_used(i)     = 0;
        prev_error     = 0;
        continue;
    end

    err = TARGET_DISTANCE - d;

    if err > 0
        KP = KP_NEAR;          % too close
    else
        KP = KP_FAR;           % too far
    end

    derivative = (err - prev_error) / dt;  % scaled by dt (proper units)
    % Note: original code uses (err - prev_error) without /dt,
    % so KD absorbs the dt factor. We keep physical units here.
    steering = KP * err + KD * (err - prev_error);   % matches Python

    % LEFT wall following (matches sign convention in main_open.py)
    angle = SERVO_CEN + steering;
    angle = max(SERVO_MIN, min(SERVO_MAX, angle));

    servo_angle(i) = angle;
    error_log(i)   = err;
    kp_used(i)     = KP;
    prev_error     = err;
end

%% ── Convert servo units → physical steering angle ────────
% Using linear mapping from steering_geometry.m:
%   angle_deg = slope * duty + offset
slope  = (MAX_STEER_LEFT - (-MAX_STEER_RIGHT)) / (SERVO_MIN_ANGLE - SERVO_MAX_ANGLE);
offset = MAX_STEER_LEFT - slope * SERVO_MIN_ANGLE;
steer_deg = slope * servo_angle + offset;

%% ── Plots ────────────────────────────────────────────────
fig = figure('Name','PD Wall-Following Simulation','NumberTitle','off', ...
             'Color','w','Position',[80 60 1100 800]);

% -- Subplot 1: Sensor distance vs target
subplot(3,1,1);
plot(t, wall_measured, 'Color',[0.7 0.7 0.7], 'LineWidth', 1, 'DisplayName','Sensor (noisy)');
hold on;
plot(t, wall_true, 'b-', 'LineWidth', 1.5, 'DisplayName','True wall distance');
yline(TARGET_DISTANCE, 'r--', 'LineWidth', 1.5, 'DisplayName','Target 180 mm');
yline(600, 'k:', 'Corner threshold', 'LabelVerticalAlignment','bottom');
ylabel('Wall Distance (mm)');
title('Sensor Reading vs Target Distance');
legend('Location','northeast'); grid on;
ylim([0 800]);

% -- Subplot 2: Error and which KP was active
subplot(3,1,2);
yyaxis left
area(t, (kp_used == KP_NEAR) * max(abs(error_log)), ...
     'FaceColor',[1 0.9 0.9], 'EdgeColor','none', 'DisplayName','KP\_NEAR active');
hold on;
plot(t, error_log, 'b-', 'LineWidth', 1.5, 'DisplayName','Error (mm)');
yline(0, 'k--');
ylabel('Error (mm)'); ylim([-200 300]);

yyaxis right
plot(t, kp_used, 'm-', 'LineWidth', 1, 'DisplayName','KP used');
ylabel('Active KP'); ylim([0 1]);

title(['PD Error & Gain Switching   |   KP\_NEAR=' num2str(KP_NEAR) ...
       '   KP\_FAR=' num2str(KP_FAR) '   KD=' num2str(KD)]);
legend('Location','northeast'); grid on;

% -- Subplot 3: Servo output
subplot(3,1,3);
yyaxis left
plot(t, servo_angle, 'k-', 'LineWidth', 1.5, 'DisplayName','Servo duty');
yline(SERVO_CEN, 'k--', 'Centre (95)');
yline(SERVO_MIN, ':r'); yline(SERVO_MAX, ':r');
ylabel('Servo Duty Value');
ylim([SERVO_MIN-10, SERVO_MAX+10]);

yyaxis right
plot(t, steer_deg, 'r-', 'LineWidth', 1, 'DisplayName','Steer angle (°)');
yline(0, 'r--');
ylabel('Physical Steering Angle (°)');

xlabel('Time (s)');
title('Servo Command — Duty Value & Physical Steering Angle');
legend('Location','northeast'); grid on;

sgtitle('WRO Future Engineers — PD Wall Following Simulation', ...
        'FontSize', 14, 'FontWeight', 'bold');

%% ── Gain Sensitivity Study ───────────────────────────────
% How do different KP_NEAR values affect overshoot?

fprintf('\n--- PD Performance Summary ---\n');
valid = abs(error_log) < 300 & error_log ~= 0;
fprintf('  Mean error  (on-wall): %+.1f mm\n', mean(error_log(valid)));
fprintf('  Std  error  (on-wall): %.1f mm (±1σ)\n', std(error_log(valid)));
fprintf('  Max  error            : %.1f mm\n', max(abs(error_log(valid))));
fprintf('  Servo saturation      : %.1f %% of time\n', ...
    100 * mean(servo_angle == SERVO_MIN | servo_angle == SERVO_MAX));

% Sweep KP_NEAR
kp_sweep    = 0.1 : 0.05 : 1.2;
overshoot   = zeros(size(kp_sweep));
settle_time = zeros(size(kp_sweep));

for k = 1:length(kp_sweep)
    pe  = 0;
    sa  = zeros(1,N);
    el  = zeros(1,N);
    for i = 1:N
        d = wall_measured(i);
        if d > 600; pe=0; continue; end
        err = TARGET_DISTANCE - d;
        KP_k = kp_sweep(k);
        steering_k = KP_k * err + KD * (err - pe);
        a = max(SERVO_MIN, min(SERVO_MAX, SERVO_CEN + steering_k));
        sa(i) = a; el(i) = err; pe = err;
    end
    in_range = abs(el) < 300 & el ~= 0;
    overshoot(k) = max(abs(el(in_range)));
end

figure('Name','KP Sensitivity','NumberTitle','off','Color','w','Position',[200 200 700 350]);
plot(kp_sweep, overshoot, 'b-o', 'LineWidth', 2, 'MarkerSize', 5);
xline(KP_NEAR, '--r', ['Current KP\_NEAR=' num2str(KP_NEAR)], ...
      'LabelVerticalAlignment','bottom');
xlabel('KP\_NEAR Value'); ylabel('Peak Error Magnitude (mm)');
title('Gain Sensitivity — KP\_NEAR vs Peak Wall-Distance Error');
grid on;

fprintf('\nDone. Review figures for PD tuning insights.\n');
