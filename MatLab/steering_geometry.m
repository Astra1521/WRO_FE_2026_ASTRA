% =========================================================
% steering_geometry.m
% WRO Future Engineers — Ackermann Steering Geometry Analysis
%
% Calculates:
%   1. Turning radius vs steering angle
%   2. Inner / outer Ackermann wheel angles
%   3. Minimum turning radius (both directions)
%   4. Swept footprint at max lock
%   5. Servo duty-to-physical-angle linearisation
%
% Run robot_params.m first, or let this script call it.
% =========================================================

clear; clc; close all;
run('robot_params.m');

%% ── 1. Turning Radius vs Steering Angle ─────────────────
% Ackermann model: R = wheelbase / tan(delta)
% where delta is the ideal INNER front wheel angle.

delta_deg = linspace(1, MAX_STEER_LEFT, 300);   % sweep 1° → max left
delta_rad = deg2rad(delta_deg);

R_inner = WHEELBASE ./ tan(delta_rad);           % inner-wheel turning radius
R_centre = sqrt(R_inner.^2 + (WHEELBASE/2)^2);  % vehicle centre-of-mass radius

figure('Name','Turning Radius vs Steering Angle','NumberTitle','off', ...
       'Color','w','Position',[100 100 900 420]);

yyaxis left
plot(delta_deg, R_inner./1000, 'b-', 'LineWidth', 2);
ylabel('Inner-Wheel Turning Radius (m)','Color','b');

yyaxis right
plot(delta_deg, R_centre./1000, 'r--', 'LineWidth', 1.5);
ylabel('CoM Turning Radius (m)','Color','r');

xlabel('Steering Angle \delta (°)');
title('Turning Radius vs Steering Angle (Ackermann, Wheelbase = 150 mm)');
legend('Inner wheel radius','Vehicle CoM radius','Location','northeast');
grid on; xlim([0 MAX_STEER_LEFT]);

% Mark max-left and max-right operating points
[~,idx_L] = min(abs(delta_deg - MAX_STEER_LEFT));
[~,idx_R] = min(abs(delta_deg - MAX_STEER_RIGHT));

yyaxis left
hold on;
plot(MAX_STEER_LEFT,  R_inner(idx_L)./1000, 'bs', 'MarkerSize', 10, ...
     'MarkerFaceColor','b','DisplayName','Max Left Lock');
plot(MAX_STEER_RIGHT, R_inner(idx_R)./1000, 'b^', 'MarkerSize', 10, ...
     'MarkerFaceColor','c','DisplayName','Max Right Lock');
hold off;

fprintf('\n--- Minimum Turning Radii ---\n');
R_min_left  = WHEELBASE / tan(deg2rad(MAX_STEER_LEFT));
R_min_right = WHEELBASE / tan(deg2rad(MAX_STEER_RIGHT));
fprintf('  Max Left  (%2.0f°): inner-wheel R = %.1f mm  (%.3f m)\n', ...
        MAX_STEER_LEFT,  R_min_left,  R_min_left/1000);
fprintf('  Max Right (%2.0f°): inner-wheel R = %.1f mm  (%.3f m)\n', ...
        MAX_STEER_RIGHT, R_min_right, R_min_right/1000);

%% ── 2. Ackermann Inner / Outer Wheel Angles ─────────────
% True Ackermann: inner angle δ_i, outer angle δ_o
%   cot(δ_o) = cot(δ_i) + TRACK/WHEELBASE

delta_i = delta_deg;          % inner wheel angle (larger)
delta_o = rad2deg( atan( 1 ./ (cot(delta_rad) + FRONT_TRACK/WHEELBASE) ) );

figure('Name','Ackermann Inner vs Outer Wheel Angles','NumberTitle','off', ...
       'Color','w','Position',[120 120 750 400]);

plot(delta_i, delta_o, 'm-', 'LineWidth', 2); hold on;
plot(delta_i, delta_i, 'k:', 'LineWidth', 1, 'DisplayName','Equal (non-Ackermann)');
xline(MAX_STEER_LEFT,  '--b', 'Max Left',  'LabelVerticalAlignment','bottom');
xline(MAX_STEER_RIGHT, '--r', 'Max Right', 'LabelVerticalAlignment','bottom');
hold off;

xlabel('Inner Wheel Angle (°)');
ylabel('Outer Wheel Angle (°)');
title('True Ackermann Geometry — Inner vs Outer Front Wheel Angles');
legend('Ackermann outer angle','Ideal 1:1 (parallel steer)','Location','northwest');
grid on;

fprintf('\n--- Ackermann Wheel Angles at Max Lock ---\n');
idx = find(delta_i >= MAX_STEER_LEFT, 1);
fprintf('  Left lock  — Inner: %.1f°  |  Outer: %.1f°\n', ...
        delta_i(idx), delta_o(idx));
idx2 = find(delta_i >= MAX_STEER_RIGHT, 1);
fprintf('  Right lock — Inner: %.1f°  |  Outer: %.1f°\n', ...
        delta_i(idx2), delta_o(idx2));

%% ── 3. Swept Footprint at Max-Left Lock ─────────────────
% Trace the four corner paths of the chassis around a left turn.
% Origin = rear-axle centre. Vehicle turns counter-clockwise.

R_rear  = R_min_left;          % rear-axle turning radius
theta   = linspace(0, pi/2, 200);   % 90° sweep

% Four chassis corners in body frame (X=fwd, Y=left)
corners = [
    WHEELBASE,  FRONT_TRACK/2;   % front-left
    WHEELBASE, -FRONT_TRACK/2;   % front-right
    0,          REAR_TRACK/2;    % rear-left
    0,         -REAR_TRACK/2     % rear-right
];
labels = {'FL','FR','RL','RR'};
colours = {'b','r','g','k'};

figure('Name','Swept Footprint @ Max-Left Lock','NumberTitle','off', ...
       'Color','w','Position',[140 140 700 700]);
hold on; axis equal; grid on;

for c = 1:4
    cx = corners(c,1);
    cy = corners(c,2);
    % Distance from turn centre (which is at [0, -(R_rear+REAR_TRACK/2)])
    % Turn centre in body frame:
    Tx = 0;
    Ty = -(R_rear + REAR_TRACK/2);   % to the right of rear axle centre
    r_corner = sqrt((cx-Tx)^2 + (cy-Ty)^2);
    px = Tx + r_corner * sin(theta);
    py = Ty + r_corner * cos(theta);
    plot(px, py, '-', 'Color', colours{c}, 'LineWidth', 1.5, ...
         'DisplayName', labels{c});
end

% Draw robot outline at start
drawRobot(0, 0, 0, BODY_LENGTH, BODY_WIDTH);

xlabel('X — Forward (mm)'); ylabel('Y — Left (mm)');
title('Swept Corner Footprint — Max Left Lock (90° Turn)');
legend('Location','northeast'); hold off;

%% ── 4. Servo PWM → Steering Angle Linearisation ─────────
% Servo duty: 50 (full left) → 95 (centre) → 140 (full right)
% Physical angle: +MAX_STEER_LEFT … 0 … -MAX_STEER_RIGHT

duty_vals   = [SERVO_MIN_ANGLE,  SERVO_CENTER,   SERVO_MAX_ANGLE];
steer_vals  = [MAX_STEER_LEFT,   0,             -MAX_STEER_RIGHT];

% Fit linear mapping
p = polyfit(duty_vals, steer_vals, 1);
duty_range  = SERVO_MIN_ANGLE:SERVO_MAX_ANGLE;
steer_fit   = polyval(p, duty_range);

figure('Name','Servo Duty vs Steering Angle','NumberTitle','off', ...
       'Color','w','Position',[160 160 700 380]);

plot(duty_range, steer_fit, 'b-', 'LineWidth', 2); hold on;
scatter(duty_vals, steer_vals, 80, 'ro', 'filled', 'DisplayName','Calibration points');
xline(SERVO_CENTER, '--k', 'Centre (95)', 'LabelVerticalAlignment','bottom');
yline(0, '--k');
hold off;

xlabel('Servo Duty Value (SERVO\_MIN=50 … SERVO\_MAX=140)');
ylabel('Steering Angle (° left = +ve)');
title('Servo PWM → Physical Steering Angle (Linear Fit)');
legend('Linear fit','Calibration points','Location','northeast');
grid on;

fprintf('\n--- Servo Linear Mapping ---\n');
fprintf('  Slope : %.4f °/duty-unit\n', p(1));
fprintf('  Offset: %.2f °\n', p(2));
fprintf('  To convert duty D → angle: angle = %.4f*D + (%.2f)\n', p(1), p(2));

%% ── Helper: draw robot rectangle ─────────────────────────
function drawRobot(x, y, heading_deg, len, wid)
    % x,y = rear-axle centre; heading = yaw from X-axis (deg)
    h = deg2rad(heading_deg);
    corners_local = [0, wid/2; len, wid/2; len, -wid/2; 0, -wid/2];
    R = [cos(h), -sin(h); sin(h), cos(h)];
    c = (R * corners_local')';
    patch(x + c(:,1), y + c(:,2), [0.8 0.9 1.0], ...
          'EdgeColor','b','FaceAlpha',0.3,'DisplayName','Robot start');
end
