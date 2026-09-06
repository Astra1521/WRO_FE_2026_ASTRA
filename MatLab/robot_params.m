% =========================================================
% robot_params.m
% WRO Future Engineers — Shared Robot Physical Parameters
%
% Run this file (or call it from other scripts) to load
% every physical constant for the robot into the workspace.
% All units: mm, kg, degrees, seconds unless noted.
% =========================================================

%% ── Chassis Geometry ─────────────────────────────────────
WHEELBASE        = 150;   % mm  (front-to-rear axle distance)
FRONT_TRACK      =  85;   % mm  (front axle width, wheel-centre to wheel-centre)
REAR_TRACK       =  85;   % mm  (rear axle width)
BODY_LENGTH      = 195;   % mm
BODY_WIDTH       = 111;   % mm
BODY_HEIGHT      = 122;   % mm
WHEEL_RADIUS     =  30;   % mm
MASS             =   0.7; % kg
BATTERY_VOLTAGE  =  12;   % V  (Bonka LiPo)

%% ── Steering Limits (measured by eye, asymmetric) ────────
MAX_STEER_LEFT   =  60;   % degrees  (measured)
MAX_STEER_RIGHT  =  47;   % degrees  (estimated, "a little above 45")

% Servo PWM map: duty-cycle 0–180 → physical angle
SERVO_MIN_ANGLE  =  50;   % duty units (hard left lock)
SERVO_CENTER     =  95;   % duty units (straight ahead)
SERVO_MAX_ANGLE  = 140;   % duty units (hard right lock)

%% ── Drivetrain ───────────────────────────────────────────
% EV3 Medium Motor — rated free-run speed ≈ 240 rpm @ 9 V.
% At 12 V, conservatively assume ~300 rpm at no-load,
% ~220 rpm under typical load.
MOTOR_RPM_NOLOAD    = 300; % rpm
MOTOR_RPM_LOADED    = 220; % rpm
WHEEL_CIRCUMFERENCE = 2 * pi * WHEEL_RADIUS; % mm per revolution

% Estimated top linear speed (loaded, with differential)
% v = RPM/60 * circumference
V_MAX_NOLOAD = MOTOR_RPM_NOLOAD / 60 * WHEEL_CIRCUMFERENCE;  % mm/s
V_MAX_LOADED = MOTOR_RPM_LOADED / 60 * WHEEL_CIRCUMFERENCE;  % mm/s

fprintf('--- Robot Parameters Loaded ---\n');
fprintf('Wheelbase          : %g mm\n',   WHEELBASE);
fprintf('Track Width        : %g mm\n',   FRONT_TRACK);
fprintf('Wheel Radius       : %g mm\n',   WHEEL_RADIUS);
fprintf('Steer Left/Right   : %g° / %g°\n', MAX_STEER_LEFT, MAX_STEER_RIGHT);
fprintf('Est. Top Speed     : %.0f mm/s (no-load), %.0f mm/s (loaded)\n', ...
        V_MAX_NOLOAD, V_MAX_LOADED);
fprintf('Battery            : %g V\n',    BATTERY_VOLTAGE);

%% ── Sensor Positions (relative to rear-centre of chassis) ─
%
%  Coordinate system:
%    X → forward (towards front of robot)
%    Y → left     (driver's left)
%    Z → up
%
%  All sensor origins measured from the rear edge, centre of width.

% ToF — Left lateral sensor
SENSOR_LEFT.x  = 170;   % mm from rear edge
SENSOR_LEFT.y  =  (BODY_WIDTH/2);  % flush with left side
SENSOR_LEFT.z  =  70;   % mm from ground
SENSOR_LEFT.label = 'Left ToF';

% ToF — Front sensor (centre of front face)
SENSOR_FRONT.x = 190;   % mm from rear edge
SENSOR_FRONT.y =   0;   % centred
SENSOR_FRONT.z =  68;   % mm from ground
SENSOR_FRONT.label = 'Front ToF';

% ToF — Right lateral sensor
SENSOR_RIGHT.x = 170;   % mm from rear edge
SENSOR_RIGHT.y = -(BODY_WIDTH/2);  % flush with right side
SENSOR_RIGHT.z =  70;   % mm from ground
SENSOR_RIGHT.label = 'Right ToF';

% Rear sensor (added for completeness; not used in open code)
SENSOR_REAR.x  =   0;   % at rear edge
SENSOR_REAR.y  =   0;   % centred
SENSOR_REAR.z  =  65;   % 6.5 cm from ground
SENSOR_REAR.label = 'Rear ToF';
