% =========================================================
% sensor_fov_layout.m
% WRO Future Engineers — Sensor Positions & Field-of-View Map
%
% Draws a top-down and side-view of the robot with all three
% ToF sensors at their exact measured positions, plus their
% detection cones and blind spots.
%
% VL53L0X / TOF_Sense typical specs:
%   FoV (half-angle)  : ±12.5° (25° full cone)
%   Range             : 20 – 2000 mm
%   Best accuracy     : < 1200 mm
% =========================================================

clear; clc; close all;
run('robot_params.m');

%% ── Sensor Specs ─────────────────────────────────────────
TOF_FOV_HALF  =  12.5;    % degrees half-angle
TOF_RANGE_MIN =   20;     % mm
TOF_RANGE_MAX = 1200;     % mm (reliable range)

%% ── Sensor Positions (in top-down XY plane) ──────────────
%  X = forward from rear edge, Y = left from centre-line

sensors(1) = struct('label','Left ToF',  'x',SENSOR_LEFT.x,  'y', SENSOR_LEFT.y,  'az',90);
sensors(2) = struct('label','Front ToF', 'x',SENSOR_FRONT.x, 'y', SENSOR_FRONT.y, 'az',0);
sensors(3) = struct('label','Right ToF', 'x',SENSOR_RIGHT.x, 'y',SENSOR_RIGHT.y,  'az',-90);
% az = sensor pointing azimuth: 0=forward, 90=left, -90=right

colours = {'b','g','r'};

%% ── Figure 1: Top-Down Layout ────────────────────────────
figure('Name','Top-Down Sensor FoV','NumberTitle','off', ...
       'Color','w','Position',[80 60 900 800]);
hold on; axis equal; grid on;

% Robot body rectangle (rear edge at X=0)
rect_x = [0, BODY_LENGTH, BODY_LENGTH, 0, 0];
rect_y = [BODY_WIDTH/2, BODY_WIDTH/2, -BODY_WIDTH/2, -BODY_WIDTH/2, BODY_WIDTH/2];
fill(rect_x, rect_y, [0.85 0.92 1.0], 'EdgeColor','k','LineWidth',2,'DisplayName','Robot body');

% Axle lines
plot([0 0],           [-REAR_TRACK/2  REAR_TRACK/2],  'k-',  'LineWidth',3);
plot([WHEELBASE WHEELBASE], [-FRONT_TRACK/2 FRONT_TRACK/2], 'k-',  'LineWidth',3);

% Wheels (4 rectangles)
wheel_w = 20; wheel_h = WHEEL_RADIUS*0.7;
wheel_pos = [WHEELBASE, FRONT_TRACK/2; WHEELBASE, -FRONT_TRACK/2; ...
             0, REAR_TRACK/2;          0,         -REAR_TRACK/2];
for w = 1:4
    wx = wheel_pos(w,1); wy = wheel_pos(w,2);
    rect2 = [-wheel_h/2+wx, wy-wheel_w/2; wx+wheel_h/2, wy-wheel_w/2; ...
              wx+wheel_h/2, wy+wheel_w/2; -wheel_h/2+wx, wy+wheel_w/2];
    fill(rect2(:,1), rect2(:,2), [0.3 0.3 0.3], 'EdgeColor','k', ...
         'HandleVisibility','off');
end

% Sensor FoV cones
for s = 1:3
    sx = sensors(s).x;
    sy = sensors(s).y;
    az = sensors(s).az;

    ang1 = az - TOF_FOV_HALF;
    ang2 = az + TOF_FOV_HALF;
    theta = linspace(deg2rad(ang1), deg2rad(ang2), 50);

    cone_x = [sx, sx + TOF_RANGE_MAX * cos(theta), sx];
    cone_y = [sy, sy + TOF_RANGE_MAX * sin(theta), sy];

    fill(cone_x, cone_y, colours{s}, ...
         'FaceAlpha', 0.12, 'EdgeColor', colours{s}, ...
         'LineStyle','--','DisplayName', [sensors(s).label ' FoV']);

    % Sensor dot
    scatter(sx, sy, 80, colours{s}, 'filled', ...
            'HandleVisibility','off');

    % Label
    lbl_offset = [15*cosd(az+90), 15*sind(az+90)];
    text(sx+lbl_offset(1), sy+lbl_offset(2), sensors(s).label, ...
         'Color', colours{s}, 'FontWeight','bold','FontSize',9, ...
         'HorizontalAlignment','center');
end

% Track wall at TARGET_DISTANCE from left sensor
wall_y = SENSOR_LEFT.y + 180;
xline_at = [0, BODY_LENGTH+200];
plot(xline_at, [wall_y wall_y], 'b--', 'LineWidth', 1.5, ...
     'DisplayName','Left wall @ 180 mm target');

% Dimensions
annotation_dim(0, -BODY_WIDTH/2-40, BODY_LENGTH, -BODY_WIDTH/2-40, ...
               sprintf('L = %g mm', BODY_LENGTH));
annotation_dim(-30, -REAR_TRACK/2, -30, REAR_TRACK/2, ...
               sprintf('W = %g mm', REAR_TRACK));

xlabel('X — Forward from Rear Edge (mm)');
ylabel('Y — Left from Centre-Line (mm)');
title('Top-Down View — Robot & ToF Sensor FoV (25° cone, 1200 mm range)');
legend('Location','northeastoutside');
xlim([-100, BODY_LENGTH+500]);
ylim([-600, 800]);
set(gca,'YDir','normal');

%% ── Figure 2: Side-View (sensor heights) ────────────────
figure('Name','Side-View Sensor Heights','NumberTitle','off', ...
       'Color','w','Position',[120 120 800 450]);
hold on; axis equal; grid on;

% Robot profile
fill([0 BODY_LENGTH BODY_LENGTH 0], [0 0 BODY_HEIGHT BODY_HEIGHT], ...
     [0.85 0.92 1.0], 'EdgeColor','k','LineWidth',2,'DisplayName','Robot body');

% Ground
plot([-30 BODY_LENGTH+30], [0 0], 'k-', 'LineWidth', 2);

% Sensor positions + FoV arcs (vertical plane, sensors pointing sideways)
side_sensors = [SENSOR_LEFT; SENSOR_FRONT; SENSOR_RIGHT; SENSOR_REAR];
side_labels  = {'Left ToF','Front ToF','Right ToF','Rear ToF'};
side_colors  = {'b','g','r','m'};
side_heights = [SENSOR_LEFT.z, SENSOR_FRONT.z, SENSOR_RIGHT.z, SENSOR_REAR.z];
side_xpos    = [SENSOR_LEFT.x, SENSOR_FRONT.x, SENSOR_RIGHT.x, 0];

for s = 1:4
    sz = side_heights(s);
    sx = side_xpos(s);
    scatter(sx, sz, 80, side_colors{s}, 'filled', 'DisplayName', side_labels{s});

    % Downward tilt line to ground
    plot([sx sx], [0 sz], '--', 'Color', [0.6 0.6 0.6], ...
         'HandleVisibility','off');

    text(sx+10, sz+5, sprintf('z=%.0f mm', sz), ...
         'Color', side_colors{s}, 'FontSize', 9);
end

xlabel('X — Forward from Rear Edge (mm)');
ylabel('Z — Height from Ground (mm)');
title('Side View — Sensor Height Positions');
legend('Location','northeast'); ylim([-20 150]);

fprintf('\n--- Sensor Blind-Spot Analysis ---\n');
fprintf('  Left ToF  : %g mm from rear, %g mm from left edge, %g mm high\n', ...
        SENSOR_LEFT.x, BODY_WIDTH/2 - SENSOR_LEFT.y, SENSOR_LEFT.z);
fprintf('  Front ToF : %g mm from rear, centred, %g mm high\n', ...
        SENSOR_FRONT.x, SENSOR_FRONT.z);
fprintf('  Right ToF : %g mm from rear, %g mm from right edge, %g mm high\n', ...
        SENSOR_RIGHT.x, abs(SENSOR_RIGHT.y) - BODY_WIDTH/2, SENSOR_RIGHT.z);

% Nose blind spot (in front of front sensor)
fprintf('\n  Front sensor is %.0f mm from front edge → %.0f mm forward blind region\n', ...
        BODY_LENGTH - SENSOR_FRONT.x, BODY_LENGTH - SENSOR_FRONT.x);
fprintf('  Emergency stop at 50 mm (from code) covers this blind region: %s\n', ...
        ternary(BODY_LENGTH - SENSOR_FRONT.x < 50, 'YES ✓', 'NO — adjust threshold'));

%% ── Helpers ──────────────────────────────────────────────
function annotation_dim(x1, y1, x2, y2, lbl)
    plot([x1 x2],[y1 y2],'k-','LineWidth',0.8,'HandleVisibility','off');
    mx = (x1+x2)/2; my = (y1+y2)/2;
    text(mx, my, lbl, 'HorizontalAlignment','center', ...
         'FontSize',8,'BackgroundColor','w','HandleVisibility','off');
end

function s = ternary(cond, a, b)
    if cond; s = a; else; s = b; end
end
