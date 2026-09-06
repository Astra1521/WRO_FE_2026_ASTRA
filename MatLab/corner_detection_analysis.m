% =========================================================
% corner_detection_analysis.m
% WRO Future Engineers — Corner Detection State Machine Analysis
%
% Replicates the EXACT 3-state corner FSM from main_open.py:
%
%   State 0  → wait for wall to disappear (reading > CORNER_HIGH)
%   State 1  → wait for wall to reappear  (reading < CORNER_END)
%              → increment corner_count
%   State 2  → wait until following resumes (|dist - TARGET| < 30)
%              → back to State 0
%
% Inputs:
%   Either (a) your real CSV log from the robot, OR
%          (b) the built-in synthetic 3-lap profile (default).
%
% How to use with real data:
%   1. Add this to your Python code:
%        with open("sensor_log.csv","a") as f:
%            f.write(f"{time.time()},{left},{front},{right}\n")
%   2. Set USE_REAL_DATA = true and update CSV_FILE below.
% =========================================================

clear; clc; close all;
run('robot_params.m');

%% ── Configuration ────────────────────────────────────────
USE_REAL_DATA = false;          % ← set true when you have a CSV
CSV_FILE      = 'sensor_log.csv';  % columns: time, left, front, right

% FSM thresholds (must match main_open.py exactly)
TARGET_DISTANCE  = 180;    % mm
CORNER_THRESHOLD = 500;    % wall "disappeared"  (legacy, not used in FSM)
CORNER_HIGH      = 550;    % State 0 → 1 trigger
CORNER_END       = 300;    % State 1 → 2 trigger (corner counted)
SETTLE_BAND      = 30;     % State 2 → 0 trigger
TOTAL_CORNERS    = 11;

WALL_DIR = "LEFT";   % change to "RIGHT" if needed

%% ── Load / Generate Sensor Data ─────────────────────────
if USE_REAL_DATA
    raw  = readmatrix(CSV_FILE);
    t    = raw(:,1) - raw(1,1);      % zero-start time
    left = raw(:,2);
    fwd  = raw(:,3);
    rght = raw(:,4);

    if WALL_DIR == "LEFT"
        wall = left;
    else
        wall = rght;
    end
    fprintf('Loaded %d samples from %s\n', length(t), CSV_FILE);

else
    % ── Synthetic 3-lap profile ───────────────────────────
    dt = 0.015;
    T  = 3 * 8.7;          % 3 laps × 8.7 s
    t  = (0:dt:T)';
    N  = length(t);

    % Straight sections: wall ≈ TARGET ± small noise
    % Corner: wall spikes to 700 mm for ~0.5 s, then drops back
    rng(7);
    wall = TARGET_DISTANCE + 8*randn(N,1);

    corner_times = [2.0, 4.5, 7.0, 9.5, 12.0, 14.5, ...
                    17.0, 19.5, 22.0, 24.5, 26.5];  % 11 corners
    for k = 1:length(corner_times)
        tc  = corner_times(k);
        idx = t >= tc & t <= tc + 0.50;
        wall(idx) = 700;                    % wall disappears
        idx2 = t > tc+0.50 & t <= tc+0.80;
        wall(idx2) = linspace(700,TARGET_DISTANCE,sum(idx2))';
    end

    fwd  = 350 + 20*randn(N,1);    % front sensor (not used by FSM)
    left = wall;
    rght = 800 * ones(N,1);        % right side open
end

%% ── Replay FSM ───────────────────────────────────────────
N = length(t);
state        = zeros(N,1);
corner_count = zeros(N,1);

cs = 0;   % current state
cc = 0;   % corner count

for i = 1:N
    d = wall(i);

    switch cs
        case 0
            if ~isnan(d) && d > CORNER_HIGH
                cs = 1;
            end
        case 1
            if ~isnan(d) && d < CORNER_END
                cc = cc + 1;
                cs = 2;
            end
        case 2
            if ~isnan(d) && abs(d - TARGET_DISTANCE) < SETTLE_BAND
                cs = 0;
            end
    end

    state(i)        = cs;
    corner_count(i) = cc;
end

fprintf('\n--- Corner Detection Results ---\n');
fprintf('  Total corners counted : %d  (expected %d)\n', cc, TOTAL_CORNERS);
if cc == TOTAL_CORNERS
    fprintf('  ✓ Correct count — robot would stop after settling.\n');
else
    fprintf('  ✗ Mismatch — check CORNER_HIGH / CORNER_END thresholds.\n');
end

%% ── Plots ────────────────────────────────────────────────
fig = figure('Name','Corner Detection Analysis','NumberTitle','off', ...
             'Color','w','Position',[80 60 1100 750]);

%  Panel 1: sensor trace + state regions
subplot(3,1,1);
% Shade state regions
for s = 1:2
    mask = state == s;
    c = [0.9 0.95 1.0; 1.0 0.9 0.85];
    shade_region(t, mask, c(s,:));
end
hold on;
plot(t, wall, 'b-', 'LineWidth', 1.2, 'DisplayName','Wall sensor (mm)');
yline(TARGET_DISTANCE, 'g--', 'LineWidth', 1.5, 'DisplayName','Target 180 mm');
yline(CORNER_HIGH,     'r:',  'LineWidth', 1.5, 'DisplayName','CORNER\_HIGH 550');
yline(CORNER_END,      'm:',  'LineWidth', 1.5, 'DisplayName','CORNER\_END 300');

% Mark each counted corner
events = find(diff(corner_count) > 0);
scatter(t(events), wall(events), 80, 'r^', 'filled', 'DisplayName','Corner counted');

ylabel('Wall Distance (mm)');
title('Sensor Trace — Corner Events & FSM State Regions');
legend('Location','northeast'); grid on;
ylim([0 800]);

% Panel 2: FSM state
subplot(3,1,2);
stairs(t, state, 'k-', 'LineWidth', 1.5);
yticks([0 1 2]);
yticklabels({'0: Follow','1: Corner open','2: Settle'});
ylabel('FSM State');
title('Corner Detection State Machine');
grid on; ylim([-0.5 2.8]);

% Panel 3: running corner count
subplot(3,1,3);
stairs(t, corner_count, 'b-', 'LineWidth', 2);
yline(TOTAL_CORNERS, 'r--', ['Stop at ' num2str(TOTAL_CORNERS)], ...
      'LabelVerticalAlignment','bottom');
xlabel('Time (s)');
ylabel('Corner Count');
title('Cumulative Corner Count — Finish Condition');
grid on; ylim([-0.5 TOTAL_CORNERS+1]);

sgtitle('WRO Future Engineers — Corner Detection Analysis', ...
        'FontSize', 14, 'FontWeight', 'bold');

%% ── Timing Report ────────────────────────────────────────
if length(events) == TOTAL_CORNERS
    inter_corner = diff(t(events));
    fprintf('\n--- Corner Timing (seconds between corners) ---\n');
    for k = 1:length(inter_corner)
        fprintf('  Corner %2d → %2d : %.2f s\n', k, k+1, inter_corner(k));
    end
    fprintf('  Total lap time : %.2f s\n', t(events(end)) - t(events(1)));

    figure('Name','Inter-Corner Timing','NumberTitle','off', ...
           'Color','w','Position',[200 200 600 320]);
    bar(2:TOTAL_CORNERS, inter_corner, 'FaceColor',[0.3 0.6 0.9]);
    xlabel('Corner Number'); ylabel('Time Since Previous Corner (s)');
    title('Inter-Corner Interval — Consistency Check');
    grid on;
end

%% ── Helper ───────────────────────────────────────────────
function shade_region(t, mask, col)
    % Shade time intervals where mask is true
    starts = find(diff([0; mask]) == 1);
    ends   = find(diff([mask; 0]) == -1);
    for k = 1:length(starts)
        x1 = t(starts(k)); x2 = t(ends(k));
        patch([x1 x2 x2 x1], [0 0 900 900], col, ...
              'EdgeColor','none','FaceAlpha',0.25,'HandleVisibility','off');
    end
end
