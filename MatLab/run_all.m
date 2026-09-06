% =========================================================
% run_all.m
% WRO Future Engineers — Run All MATLAB Analysis Scripts
%
% Executes every analysis script in logical order.
% Open this file in MATLAB and press Run, or type:
%   >> run('run_all.m')
% =========================================================

clc;
fprintf('==========================================\n');
fprintf(' WRO Future Engineers — MATLAB Analysis  \n');
fprintf('==========================================\n\n');

scripts = {
    'robot_params',
    'steering_geometry',
    'pd_wall_following_sim',
    'corner_detection_analysis',
    'speed_lap_analysis',
    'sensor_fov_layout'
};

for k = 1:length(scripts)
    fprintf('\n[%d/%d] Running %s.m ...\n', k, length(scripts), scripts{k});
    try
        run([scripts{k} '.m']);
        fprintf('      ✓ Done\n');
    catch ME
        fprintf('      ✗ Error: %s\n', ME.message);
    end
    pause(0.2);
end

fprintf('\n==========================================\n');
fprintf(' All scripts complete. Check figures.     \n');
fprintf('==========================================\n');
