
from collections import deque
import time
import queue
import numpy as np
import cv2
import threading
import os
import sys
import traceback
from datetime import datetime
from gpiozero import Button, LED

import bno055
import camera
import distance
import motor
import servo
import config

ORANGE_COOLDOWN_FRAMES = 50
ORANGE_DETECTION_HISTORY_LENGTH = 4

FRAME_WIDTH = 640
FRAME_HEIGHT = 360
FRAME_MIDPOINT_X = FRAME_WIDTH // 2

HSV_RANGES = {
    'LOWER_RED_1': np.array([0, 100, 55]), 'UPPER_RED_1': np.array([5, 255, 255]),
    'LOWER_RED_2': np.array([174, 100, 55]), 'UPPER_RED_2': np.array([180, 255, 255]),
    'LOWER_GREEN': np.array([40, 108, 40]), 'UPPER_GREEN': np.array([80, 255, 180]),
    'LOWER_BLACK': np.array([0, 0, 0]), 'UPPER_BLACK': np.array([180, 95, 70]),
    'LOWER_ORANGE': np.array([6, 70, 20]), 'UPPER_ORANGE': np.array([26, 255, 255]),
    'LOWER_MAGENTA': np.array([158, 73, 64]), 'UPPER_MAGENTA': np.array([172, 255, 223]),
    'LOWER_BLUE': np.array([94, 45, 58]), 'UPPER_BLUE': np.array([140, 226, 185])
}

COLOR_RANGES = HSV_RANGES

LOWER_RED_1 = COLOR_RANGES['LOWER_RED_1']
UPPER_RED_1 = COLOR_RANGES['UPPER_RED_1']
LOWER_RED_2 = COLOR_RANGES['LOWER_RED_2']
UPPER_RED_2 = COLOR_RANGES['UPPER_RED_2']
LOWER_GREEN = COLOR_RANGES['LOWER_GREEN']
UPPER_GREEN = COLOR_RANGES['UPPER_GREEN']
LOWER_BLACK = COLOR_RANGES['LOWER_BLACK']
UPPER_BLACK = COLOR_RANGES['UPPER_BLACK']
LOWER_ORANGE = COLOR_RANGES['LOWER_ORANGE']
UPPER_ORANGE = COLOR_RANGES['UPPER_ORANGE']
LOWER_MAGENTA = COLOR_RANGES['LOWER_MAGENTA']
UPPER_MAGENTA = COLOR_RANGES['UPPER_MAGENTA']
LOWER_BLUE = COLOR_RANGES['LOWER_BLUE']
UPPER_BLUE = COLOR_RANGES['LOWER_BLUE']

detection_params = {'min_area': 300, 'return_rule': 'biggest_in_job', 'return_mask': True}
WALL_MIN_AREA = detection_params['min_area']
BLOCK_MIN_AREA = 500
MAGENTA_MIN_AREA = 500
CLOSE_BLOCK_MIN_AREA = 15

left_roi_x, left_roi_y, left_roi_w, left_roi_h = 0, 140, 135, 150
right_roi_x, right_roi_y, right_roi_w, right_roi_h = 505, 140, 135, 150
inner_left_roi_x, inner_left_roi_y, inner_left_roi_w, inner_left_roi_h = 140, 165, 100, 100
inner_right_roi_x, inner_right_roi_y, inner_right_roi_w, inner_right_roi_h = 400, 165 , 100, 100
line_roi_x, line_roi_y, line_roi_w, line_roi_h = 280, 200, 80, 40
close_x,close_y,close_w,close_h = 140,120,360,10
full_frame_roi = (0, 100, 640, 165)
close_block_roi = (250, 230, 140, 10)

left_side_job = {'roi': (left_roi_x, left_roi_y, left_roi_w, left_roi_h), 'type': 'wall_left'}
right_side_job = {'roi': (right_roi_x, right_roi_y, right_roi_w, right_roi_h), 'type': 'wall_right'}
inner_left_side_job = {'roi': (inner_left_roi_x, inner_left_roi_y, inner_left_roi_w, inner_left_roi_h), 'type': 'wall_inner_left'}
inner_right_side_job = {'roi': (inner_right_roi_x, inner_right_roi_y, inner_right_roi_w, inner_right_roi_h), 'type': 'wall_inner_right'}

roi_mask_walls = np.zeros((FRAME_HEIGHT, FRAME_WIDTH), dtype="uint8")
for job in [left_side_job, right_side_job, inner_left_side_job, inner_right_side_job]:
    x, y, w, h = job['roi']
    cv2.rectangle(roi_mask_walls, (x, y), (x + w, y + h), 255, -1)

roi_mask_main_blocks = np.zeros((FRAME_HEIGHT, FRAME_WIDTH), dtype="uint8")
x, y, w, h = full_frame_roi
cv2.rectangle(roi_mask_main_blocks, (x, y), (x + w, y + h), 255, -1)

roi_mask_close_blocks = np.zeros((FRAME_HEIGHT, FRAME_WIDTH), dtype="uint8")
x, y, w, h = close_block_roi
cv2.rectangle(roi_mask_close_blocks, (x, y), (x + w, y + h), 255, -1)

roi_mask_line = np.zeros((FRAME_HEIGHT, FRAME_WIDTH), dtype="uint8")
cv2.rectangle(roi_mask_line, (line_roi_x, line_roi_y), (line_roi_x + line_roi_w, line_roi_h + line_roi_y), 255, -1)

roi_mask_magenta = np.zeros((FRAME_HEIGHT, FRAME_WIDTH), dtype="uint8")
x, y, w, h = full_frame_roi
cv2.rectangle(roi_mask_magenta, (x, y), (x + w, y + h), 255, -1)

roi_mask_close_black = np.zeros((FRAME_HEIGHT, FRAME_WIDTH), dtype="uint8")
cv2.rectangle(roi_mask_close_black, (close_x, close_y), (close_x + close_w, close_y + close_h), 255, -1)

class CameraThread(threading.Thread):
    def __init__(self, camera_instance):
        super().__init__()
        self.camera = camera_instance
        self.latest_frame = None
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.daemon = True
        self.frame_counter = 0

    def run(self):
        while not self.stop_event.is_set():
            frame = self.camera.capture_frame()
            with self.lock:
                self.frame_counter += 1
                self.latest_frame = frame

    def get_frame(self):
        with self.lock:
            if self.latest_frame is not None:
                return self.latest_frame.copy(), self.frame_counter
            return None

    def stop(self):
        self.stop_event.set()

class VideoWriterThread(threading.Thread):
    def __init__(self, path, fourcc, fps, frame_size):
        super().__init__()
        self.out = cv2.VideoWriter(path, fourcc, fps, frame_size)
        self.queue = queue.Queue()
        self.stop_event = threading.Event()
        self.daemon = True

    def run(self):
        while not self.stop_event.is_set() or not self.queue.empty():
            try:
                frame = self.queue.get(timeout=0.1)
                self.out.write(frame)
                self.queue.task_done()
            except queue.Empty:
                continue
            except:
                print(f"VideoWriterThread: ERROR writing frame")
                traceback.print_exc()
                continue
        self.out.release()

    def write(self, frame):
        if not self.stop_event.is_set():
            self.queue.put(frame)

    def stop(self):
        self.stop_event.set()

def process_video_frame(frame):
    processed_data = {
        'detected_blocks': [],
        'detected_walls': [],
        'detected_orange': [],
        'detected_blue' : [],
        'detected_magenta': [],
        'detected_close_black': []
    }
    
    GLOBAL_Y_OFFSET = 100
    GLOBAL_Y_END = 290
    SLICE_HEIGHT = GLOBAL_Y_END - GLOBAL_Y_OFFSET

    frame_slice = frame[GLOBAL_Y_OFFSET:GLOBAL_Y_END, :]
    frame_slice = cv2.GaussianBlur(frame_slice, (1, 7), 0)
    
    hsv_slice = cv2.cvtColor(frame_slice, cv2.COLOR_BGR2HSV)

    mx, my, mw, mh = full_frame_roi
    my_slice = max(0, my - GLOBAL_Y_OFFSET)
    main_crop = hsv_slice[my_slice:my_slice+mh, mx:mx+mw]
    
    mask_red1_main = cv2.inRange(main_crop, LOWER_RED_1, UPPER_RED_1)
    mask_red2_main = cv2.inRange(main_crop, LOWER_RED_2, UPPER_RED_2)
    mask_red_main = cv2.bitwise_or(mask_red1_main, mask_red2_main)
    mask_green_main = cv2.inRange(main_crop, LOWER_GREEN, UPPER_GREEN)
    mask_magenta_main = cv2.inRange(main_crop, LOWER_MAGENTA, UPPER_MAGENTA)

    lx, ly, lw, lh = line_roi_x, line_roi_y, line_roi_w, line_roi_h
    ly_slice = ly - GLOBAL_Y_OFFSET
    line_crop = hsv_slice[ly_slice:ly_slice+lh, lx:lx+lw]
    
    mask_orange_line = cv2.inRange(line_crop, LOWER_ORANGE, UPPER_ORANGE)
    mask_blue_line = cv2.inRange(line_crop, LOWER_BLUE, UPPER_BLUE)

    cx, cy, cw, ch = close_block_roi
    cy_slice = cy - GLOBAL_Y_OFFSET
    close_crop = hsv_slice[cy_slice:cy_slice+ch, cx:cx+cw]
    
    mask_red1_close = cv2.inRange(close_crop, LOWER_RED_1, UPPER_RED_1)
    mask_red2_close = cv2.inRange(close_crop, LOWER_RED_2, UPPER_RED_2)
    mask_red_close = cv2.bitwise_or(mask_red1_close, mask_red2_close)

    mask_green_close = cv2.inRange(close_crop, LOWER_GREEN, UPPER_GREEN)
    mask_magenta_close = cv2.inRange(close_crop, LOWER_MAGENTA, UPPER_MAGENTA)

    cbx, cby, cbw, cbh = close_x, close_y, close_w, close_h
    cby_slice = cby - GLOBAL_Y_OFFSET
    
    global_red_mask = np.zeros((SLICE_HEIGHT, FRAME_WIDTH), dtype="uint8")
    global_green_mask = np.zeros((SLICE_HEIGHT, FRAME_WIDTH), dtype="uint8")
    global_blue_mask = np.zeros((SLICE_HEIGHT, FRAME_WIDTH), dtype="uint8")
    global_magenta_mask = np.zeros((SLICE_HEIGHT, FRAME_WIDTH), dtype="uint8")

    global_red_mask[my_slice:my_slice+mh, mx:mx+mw] = cv2.bitwise_or(global_red_mask[my_slice:my_slice+mh, mx:mx+mw], mask_red_main)
    global_green_mask[my_slice:my_slice+mh, mx:mx+mw] = cv2.bitwise_or(global_green_mask[my_slice:my_slice+mh, mx:mx+mw], mask_green_main)
    global_magenta_mask[my_slice:my_slice+mh, mx:mx+mw] = cv2.bitwise_or(global_magenta_mask[my_slice:my_slice+mh, mx:mx+mw], mask_magenta_main)

    global_red_mask[cy_slice:cy_slice+ch, cx:cx+cw] = cv2.bitwise_or(global_red_mask[cy_slice:cy_slice+ch, cx:cx+cw], mask_red_close)
    global_green_mask[cy_slice:cy_slice+ch, cx:cx+cw] = cv2.bitwise_or(global_green_mask[cy_slice:cy_slice+ch, cx:cx+cw], mask_green_close)
    global_magenta_mask[cy_slice:cy_slice+ch, cx:cx+cw] = cv2.bitwise_or(global_magenta_mask[cy_slice:cy_slice+ch, cx:cx+cw], mask_magenta_close)

    global_blue_mask[ly_slice:ly_slice+lh, lx:lx+lw] = cv2.bitwise_or(global_blue_mask[ly_slice:ly_slice+lh, lx:lx+lw], mask_blue_line)

    mask_black = cv2.inRange(hsv_slice, LOWER_BLACK, UPPER_BLACK)
    mask_red_or_green = cv2.bitwise_or(global_red_mask, global_green_mask)
    mask_red_or_green_or_blue = cv2.bitwise_or(mask_red_or_green, global_blue_mask)
    
    pure_black_mask = cv2.bitwise_and(mask_black, cv2.bitwise_not(mask_red_or_green_or_blue))
    black_or_magenta_mask = cv2.bitwise_or(pure_black_mask, global_magenta_mask)

    roi_mask_walls_slice = roi_mask_walls[GLOBAL_Y_OFFSET:GLOBAL_Y_END, :]
    roi_mask_close_black_slice = roi_mask_close_black[GLOBAL_Y_OFFSET:GLOBAL_Y_END, :]

    final_mask_walls = cv2.bitwise_and(pure_black_mask, roi_mask_walls_slice)
    final_mask_close_black = cv2.bitwise_and(black_or_magenta_mask, roi_mask_close_black_slice)
    
    if cv2.countNonZero(mask_magenta_main) > 0:
        contours, _ = cv2.findContours(mask_magenta_main, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            biggest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(biggest_contour)

            if area > MAGENTA_MIN_AREA:
                M = cv2.moments(biggest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"]) + mx
                    cy = int(M["m01"] / M["m00"]) + my
                    biggest_contour_global = biggest_contour + [mx, my]
                    leftmost_x = biggest_contour_global[:, 0, 0].min()
                    rightmost_x = biggest_contour_global[:, 0, 0].max()

                    dist_to_center_left = abs(leftmost_x - FRAME_MIDPOINT_X)
                    dist_to_center_right = abs(rightmost_x - FRAME_MIDPOINT_X)

                    if dist_to_center_left <= dist_to_center_right:
                        target_x = leftmost_x
                    else:
                        target_x = rightmost_x
                    
                    processed_data['detected_magenta'].append({
                        'type': 'magenta_block',
                        'area': area,
                        'centroid': (cx, cy),
                        'contour': biggest_contour_global,
                        'target_x': target_x,
                        'target_y': cy
                    })

    def process_block_contours(mask, offset_x, offset_y, b_type, b_color, min_area):
        if cv2.countNonZero(mask) > 0:
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                biggest_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(biggest_contour)
                if area > min_area:
                    M = cv2.moments(biggest_contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"]) + offset_x
                        cy = int(M["m01"] / M["m00"]) + offset_y
                        biggest_contour_global = biggest_contour + [offset_x, offset_y]
                        return {'type': b_type, 'color': b_color, 'area': area, 'centroid': (cx, cy), 'contour': biggest_contour_global}
        return None

    all_detected_blocks = []
    
    res = process_block_contours(mask_red_main, mx, my, 'block', 'red', BLOCK_MIN_AREA)
    if res: all_detected_blocks.append(res)
    
    res = process_block_contours(mask_green_main, mx, my, 'block', 'green', BLOCK_MIN_AREA)
    if res: all_detected_blocks.append(res)

    res = process_block_contours(mask_red_close, cx, cy, 'close_block', 'red', CLOSE_BLOCK_MIN_AREA)
    if res: all_detected_blocks.append(res)

    res = process_block_contours(mask_green_close, cx, cy, 'close_block', 'green', CLOSE_BLOCK_MIN_AREA)
    if res: all_detected_blocks.append(res)

    res = process_block_contours(mask_magenta_close, cx, cy, 'close_block', 'magenta', CLOSE_BLOCK_MIN_AREA)
    if res: all_detected_blocks.append(res)

    main_blocks = [b for b in all_detected_blocks if b['type'] == 'block']
    other_blocks = [b for b in all_detected_blocks if b['type'] != 'block']
    if len(main_blocks) > 1:
        lowest_main_block = max(main_blocks, key=lambda b: b['centroid'][1])
        main_blocks = [lowest_main_block]
    processed_data['detected_blocks'] = main_blocks + other_blocks
    
    if cv2.countNonZero(mask_orange_line) > 0:
        contours, _ = cv2.findContours(mask_orange_line, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            biggest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(biggest_contour)
            if area > 20:
                M = cv2.moments(biggest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"]) + lx
                    cy = int(M["m01"] / M["m00"]) + ly
                    biggest_contour_global = biggest_contour + [lx, ly]
                    processed_data['detected_orange'].append({'type': 'orange_block', 'color': 'orange', 'area': area, 'centroid': (cx, cy), 'contour': biggest_contour_global})

    if cv2.countNonZero(mask_blue_line) > 0:
        contours, _ = cv2.findContours(mask_blue_line, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            biggest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(biggest_contour)
            if area > 20:
                M = cv2.moments(biggest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"]) + lx
                    cy = int(M["m01"] / M["m00"]) + ly
                    biggest_contour_global = biggest_contour + [lx, ly]
                    processed_data['detected_blue'].append({'type': 'blue_block', 'color': 'blue', 'area': area, 'centroid': (cx, cy), 'contour': biggest_contour_global})

    if cv2.countNonZero(final_mask_close_black) > 0:
        contours, _ = cv2.findContours(final_mask_close_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > WALL_MIN_AREA:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"]) + GLOBAL_Y_OFFSET
                    contour_global = contour + [0, GLOBAL_Y_OFFSET]
                    processed_data['detected_close_black'].append({
                        'type': 'close_black',
                        'color': 'black',
                        'area': area,
                        'centroid': (cx, cy),
                        'contour': contour_global
                    })

    wall_contours_by_roi = {job['type']: [] for job in [left_side_job, right_side_job, inner_left_side_job, inner_right_side_job]}
    if cv2.countNonZero(final_mask_walls) > 0:
        contours, _ = cv2.findContours(final_mask_walls, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            if cv2.contourArea(c) > WALL_MIN_AREA:
                M = cv2.moments(c)
                if M["m00"] == 0: continue
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"]) + GLOBAL_Y_OFFSET

                job_type = 'unknown'
                if left_side_job['roi'][0] <= cx < left_side_job['roi'][0] + left_side_job['roi'][2]: job_type = left_side_job['type']
                elif right_side_job['roi'][0] <= cx < right_side_job['roi'][0] + right_side_job['roi'][2]: job_type = right_side_job['type']
                elif inner_left_side_job['roi'][0] <= cx < inner_left_side_job['roi'][0] + inner_left_side_job['roi'][2]: job_type = inner_left_side_job['type']
                elif inner_right_side_job['roi'][0] <= cx < inner_right_side_job['roi'][0] + inner_right_side_job['roi'][2]: job_type = inner_right_side_job['type']

                if job_type != 'unknown':
                    wall_contours_by_roi[job_type].append(c)

    for job_type, contour_list in wall_contours_by_roi.items():
        if contour_list:
            biggest_contour = max(contour_list, key=cv2.contourArea)
            area = cv2.contourArea(biggest_contour)
            M = cv2.moments(biggest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"]) + GLOBAL_Y_OFFSET
                biggest_contour_global = biggest_contour + [0, GLOBAL_Y_OFFSET]
                processed_data['detected_walls'].append({'type': job_type, 'color': 'black', 'area': area, 'centroid': (cx, cy), 'contour': biggest_contour_global})
    
    return processed_data

def annotate_video_frame(frame, detections, driving_direction, debug_info="", visual_target_x=None):
    annotated_frame = frame.copy()
    light_blue = (255, 255, 0)
    target_line_color = (255, 0, 255)

    all_rois = [
        (left_roi_x, left_roi_y, left_roi_w, left_roi_h),
        (right_roi_x, right_roi_y, right_roi_w, right_roi_h),
        (inner_left_roi_x, inner_left_roi_y, inner_left_roi_w, inner_left_roi_h),
        (inner_right_roi_x, inner_right_roi_y, inner_right_roi_w, inner_right_roi_h),
        (line_roi_x, line_roi_y, line_roi_w, line_roi_h),
        (close_x, close_y, close_w, close_h),
        full_frame_roi,
        close_block_roi
    ]
    for x, y, w, h in all_rois:
        cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), light_blue, 2)

    for wall in detections['detected_walls']:
        cv2.drawContours(annotated_frame, [wall['contour']], -1, (0, 0, 0), 2)

    for block in detections['detected_blocks']:
        draw_color = (255, 255, 255)
        if block['color'] == 'red':
            draw_color = (0, 0, 255)
        elif block['color'] == 'green':
            draw_color = (0, 255, 0)
        elif block['color'] == 'magenta':
            draw_color = (255, 0, 255)
        cv2.drawContours(annotated_frame, [block['contour']], -1, draw_color, 2)

    for orange_obj in detections['detected_orange']:
        cv2.drawContours(annotated_frame, [orange_obj['contour']], -1, (0, 165, 255), 2)

    for blue_obj in detections['detected_blue']:
        cv2.drawContours(annotated_frame, [blue_obj['contour']], -1, (255, 0, 0), 2)

    for black_obj in detections.get('detected_close_black', []):
        cv2.drawContours(annotated_frame, [black_obj['contour']], -1, (0, 0, 0), 2)

    for magenta_obj in detections['detected_magenta']:
        cv2.drawContours(annotated_frame, [magenta_obj['contour']], -1, (255, 0, 255), 2)
        target_x = magenta_obj['target_x']
        cy = magenta_obj['centroid'][1]
        cv2.circle(annotated_frame, (target_x, cy), 7, (255, 255, 255), -1)

    if visual_target_x is not None:
        cv2.line(annotated_frame, (visual_target_x, 0), (visual_target_x, FRAME_HEIGHT), target_line_color, 2)

    cv2.putText(annotated_frame, str(debug_info), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    
    return annotated_frame

if __name__ == "__main__":
    
    run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_folder = "obstacle"
    run_folder = os.path.join(base_folder, run_timestamp)
    os.makedirs(run_folder, exist_ok=True)
    video_path = os.path.join(run_folder, 'obstacle.mp4')
    log_path = os.path.join(run_folder, 'obstacle_output.txt')
    log_file = open(log_path, 'w')
    sys.stdout = log_file
    sys.stderr = log_file
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    video_writer_thread = VideoWriterThread(video_path, fourcc, 30, (640, 360))
    video_writer_thread.start()
    
    camera.initialize()
    motor.initialize()
    servo.initialize()
    
    button = Button(16)
    led = LED(5)
    
    print("Main: Initializing IMU...")
    bno055.initialize()
    print("Main: IMU is ready.")

    print("Main: Initializing distance sensors...")
    distance.initialise()
    print("Main: Distance sensors are ready.")

    orange_detection_history = deque([False] * ORANGE_DETECTION_HISTORY_LENGTH, maxlen=ORANGE_DETECTION_HISTORY_LENGTH)
    cooldown_frames = 0
    orange_detection_history.append(False)
    turn_counter = 0
    angle = 0
    prevangle = 0
    
    camera_thread = CameraThread(camera)
    camera_thread.start()
    
    time.sleep(1)
    led.on()
    print("MainThread: Waiting for physical button press to start...")
    button.wait_for_press()
    led.off()
    time.sleep(0.5)

    driving_direction = "clockwise"
    print(f"MainThread: Hardcoding driving direction to {driving_direction} for testing.")
       
    INITIAL_HEADING = bno055.get_heading()
    while INITIAL_HEADING is None:
        print("MainThread: Waiting for first valid heading reading...")
        INITIAL_HEADING = bno055.get_heading()
        time.sleep(0.05)
    print(f"MainThread: Initial heading locked: {INITIAL_HEADING}")

    try:
        run_start_time = time.monotonic()
        past_frame_counter = 0
        frame_counter = 0
        
        motor.forward(config.OBS_BASE_SPEED)
        frame_start_time = time.perf_counter()
        
        while True:
            angle = 0
            debug = []
            visual_target_x = None
            
            frame, frame_counter = camera_thread.get_frame()
            if frame_counter == past_frame_counter:
                continue
            past_frame_counter = frame_counter
            if frame is None:
                continue

            distance_left = distance.get_distance(config.LEFT_CHANNEL)
            distance_center = distance.get_distance(config.FRONT_CHANNEL)
            distance_right = distance.get_distance(config.RIGHT_CHANNEL)
            current_heading = bno055.get_heading()

            detections = process_video_frame(frame)
            detected_blocks = detections['detected_blocks']
            detected_walls = detections['detected_walls']
            detected_orange_object = detections['detected_orange']
            detected_blue_object = detections['detected_blue']

            blue_detected_this_frame = bool(detected_blue_object)
            orange_detected_this_frame = bool(detected_orange_object)
            orange_detection_history.append(orange_detected_this_frame)

            if cooldown_frames > 0:
                cooldown_frames -= 1
            elif not orange_detection_history[-ORANGE_DETECTION_HISTORY_LENGTH] and all(list(orange_detection_history)[1:]):
                turn_counter += 1
                cooldown_frames = ORANGE_COOLDOWN_FRAMES
                print("turn_counter ---------------->", turn_counter)

            if detected_blocks:
                is_close_block = False
                for block in detected_blocks:
                    if block['type'] == 'close_block':
                        is_close_block = True
                        if block['color'] == 'magenta' and (time.monotonic()-run_start_time) > 5:
                            if driving_direction == 'clockwise':
                                angle = -25
                            else:
                                angle = 30
                        elif block['color'] == 'red':
                            angle = -25
                        elif block['color'] == 'green':
                            angle = 30
                        else:
                            is_close_block = False
                            break
                        servo.set_angle(angle)
                        motor.reverse(60)
                        time.sleep(0.5)
                        motor.forward(60)
                        servo.set_angle(-angle)
                        time.sleep(0.3)
                        motor.forward(config.OBS_BASE_SPEED)
                        break
                
                if not is_close_block:
                    motor.forward(config.OBS_BASE_SPEED)
                    block = detected_blocks[0]
                    block_color = block['color']
                    block_x, block_y = block['centroid']
                    debug.append((block_x, block_y))
                    
                    if block_color == 'red':
                        wall_inner_right_size = sum(obj['area'] for obj in detected_walls if obj['type'] == 'wall_inner_right')
                        target = 300 if block_y > 170 and 200 < block_x < 440 else 150
                        debug.append(target)
                        if detections['detected_magenta'] and driving_direction == 'counter-clockwise' and abs(detections['detected_magenta'][0]['target_y']-block_y) < 70 and abs(detections['detected_magenta'][0]['centroid'][0]-block_x) > 70:
                            target_x = detections['detected_magenta'][0]['target_x']
                            midpoint_x = (block_x + target_x) // 2
                            visual_target_x = midpoint_x
                            angle = ((midpoint_x - FRAME_MIDPOINT_X) * 0.15) + 1
                        else:
                            visual_target_x = 320 - target
                            angle = ((block_x - (320 - target)) * 0.09) + 1
                        if wall_inner_right_size > 3000: angle = np.clip(angle, -45, -10)
                        else: angle = np.clip(angle, -45, 35)
                    
                    elif block_color == 'green':
                        wall_inner_left_size = sum(obj['area'] for obj in detected_walls if obj['type'] == 'wall_inner_left')
                        target = 300 if block_y > 160 and 240 < block_x < 400 else 150
                        if detections['detected_magenta'] and driving_direction == 'clockwise' and abs(detections['detected_magenta'][0]['target_y']-block_y) < 70:
                            target_x = detections['detected_magenta'][0]['target_x']
                            midpoint_x = (block_x + target_x) // 2
                            visual_target_x = midpoint_x
                            angle = ((midpoint_x - FRAME_MIDPOINT_X) * 0.30) + 1
                        else:
                            visual_target_x = 320 + target
                            angle = ((block_x - (320 + target)) * 0.1) + 1
                        if wall_inner_left_size > 3000: angle = np.clip(angle, 15, 45)
                        else: angle = np.clip(angle, -45, 45)
            elif detections['detected_magenta']:
                if driving_direction == 'clockwise':
                    target = 320 - 200
                else:
                    target = 320 + 220
                angle = ((detections['detected_magenta'][0]['centroid'][0] - target) * 0.15) + 1
        
            else:
                left_pixel_size, right_pixel_size, wall_inner_left_size, wall_inner_right_size, target = 0, 0, 0, 0, 0
                left_pixel_size = sum(obj['area'] for obj in detected_walls if obj['type'] == 'wall_left')
                right_pixel_size = sum(obj['area'] for obj in detected_walls if obj['type'] == 'wall_right')
                wall_inner_left_size = sum(obj['area'] for obj in detected_walls if obj['type'] == 'wall_inner_left')
                wall_inner_right_size = sum(obj['area'] for obj in detected_walls if obj['type'] == 'wall_inner_right')
                if left_pixel_size < 100 and (right_pixel_size + wall_inner_right_size) > 100:
                    right_pixel_size *= 2
                    right_pixel_size += 25000
                elif right_pixel_size < 100 and (left_pixel_size + wall_inner_left_size) > 100:
                    left_pixel_size *= 2
                    left_pixel_size += 25000
                
                debug.extend([left_pixel_size, right_pixel_size])
                angle = (((left_pixel_size + wall_inner_left_size) - (right_pixel_size + wall_inner_right_size)) * 0.0005) + 1
                close_black_area = sum(obj['area'] for obj in detections.get('detected_close_black', []))
                if close_black_area > 3000:
                    if driving_direction == 'clockwise':
                        angle += 35
                    else:
                        angle += -35
                if left_pixel_size == 0 and right_pixel_size == 0 and (detected_orange_object or detected_blue_object):
                    if driving_direction == 'clockwise':
                        angle += 35
                    else:
                        angle += -35
            
            debug.append(round(angle))
            debug.append(turn_counter)

            elapsed = time.perf_counter() - frame_start_time
            if elapsed < 1/40:
                time.sleep(1/40 - elapsed)
            frame_end_time = time.perf_counter()
            fps = 1 / (frame_end_time - frame_start_time)
            frame_start_time = time.perf_counter()
            
            debug.append(round(fps))
            debug.append(frame_counter)
            
            annotated_frame = annotate_video_frame(frame, detections, driving_direction, debug_info=str(debug), visual_target_x=visual_target_x)
            
            try:
                video_writer_thread.write(annotated_frame)
            except Exception as e:
                print(e)
                
            angle = np.clip(angle, prevangle - 10, prevangle + 10)
            angle = np.clip(angle, -40, 40)
            if angle != prevangle:
                servo.set_angle(angle)
            prevangle = angle
            angle = 0
            
            if button.is_pressed:
                print("Main: Button pressed, stopping robot.")
                motor.brake()
                break
                
            if turn_counter >= 13:
                print("Main: 13 turns completed! Stopping robot safely.")
                run_end_time = time.monotonic()
                run_time = run_end_time - run_start_time
                print(f"Total Run Time: {run_time:.2f} seconds")
                motor.brake()
                break

    except Exception as e:
        print(f"Main: ERROR during execution: {e}")
        traceback.print_exc()

    finally:
        motor.brake()
        servo.set_angle(0)
        time.sleep(0.5)
        
        try:
            print("Final Left:", distance.get_distance(config.LEFT_CHANNEL))
            print("Final Center:", distance.get_distance(config.FRONT_CHANNEL))
            print("Final Right:", distance.get_distance(config.RIGHT_CHANNEL))
        except:
            pass

        motor.brake()
        print("Main: Signaling threads to stop...")
        camera_thread.stop()
        video_writer_thread.stop()

        print("Main: Waiting for threads to complete...")
        camera_thread.join()
        video_writer_thread.join()
        print("Main: All threads have completed.")
                
        motor.brake()
        camera.cleanup()
        servo.set_angle(0)
        servo.cleanup()
        motor.cleanup()
        bno055.cleanup()
        distance.cleanup()
        cv2.destroyAllWindows()
        
        if 'log_file' in locals() and not log_file.closed:
            print(f"Log file saved to {log_path}")
            log_file.close()
