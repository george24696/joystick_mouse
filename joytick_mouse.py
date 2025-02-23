import pygame
import pyautogui

# Initialize pygame
pygame.init()
pygame.joystick.init()

# Check if a joystick is connected
if pygame.joystick.get_count() == 0:
    print("No joystick connected")
    exit()

# Initialize the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Calibration variables for sensitivity and smoothness
sensitivity = 8000     # High sensitivity as per your choice
scroll_sensitivity = 12000
smoothness = 180       # High FPS for smoother movement
dead_zone = 0.1        # Dead zone threshold

# Set up the clock for controlling the loop speed
clock = pygame.time.Clock()
fps = smoothness       # Frames per second

# Precompute movement factors (saves a few multiplications per frame)
move_factor = sensitivity / fps
scroll_factor = scroll_sensitivity / fps

# Initialize cumulative movement variables
cum_move_x = 0.0
cum_move_y = 0.0
cum_scroll = 0.0

# Cache number of buttons for performance
num_buttons = joystick.get_numbuttons()

# Initialize previous button states for debouncing
prev_button_states = [False] * num_buttons

def smooth_input(value, dead_zone):
    """
    Apply dead zone and cubic smoothing to joystick input for more natural movement.
    Cubing reduces sensitivity around the center while still allowing full range at the extremes.
    """
    if abs(value) < dead_zone:
        return 0.0
    return value ** 3

# Main loop
try:
    while True:
        # Process events (improves performance by handling events properly)
        for event in pygame.event.get():
            pass  # We can handle specific events here if needed

        # Handle button presses with debouncing
        for i in range(num_buttons):
            current_state = joystick.get_button(i)
            prev_state = prev_button_states[i]
            if not prev_state and current_state:
                print(f"Button {i} pressed")  # Log the pressed button
                if i == 5:
                    pyautogui.click(button='left')
                elif i == 7:
                    pyautogui.click(button='right')
                elif i == 0:
                    pyautogui.hotkey('ctrl', '+')  # Zoom in
                elif i == 2:
                    pyautogui.hotkey('ctrl', '-')  # Zoom out
                elif i == 3:
                    pyautogui.press('left')        # Left arrow key
                elif i == 1:
                    pyautogui.press('right')       # Right arrow key
                elif i == 4:
                    pyautogui.hotkey('win', 'tab') # Windows + Tab
                elif i == 6:
                    pyautogui.press('f11')         # Toggle Fullscreen
            prev_button_states[i] = current_state

        # Handle stick movements with smoothing
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)
        axis_scroll = joystick.get_axis(2)

        # Apply smoothing and dead zone to joystick axes
        smoothed_x = smooth_input(axis_x, dead_zone)
        smoothed_y = smooth_input(axis_y, dead_zone)
        smoothed_scroll = smooth_input(axis_scroll, dead_zone)

        # Calculate movement based on smoothed values
        move_x = smoothed_x * move_factor
        move_y = smoothed_y * move_factor
        scroll_amount = smoothed_scroll * scroll_factor

        # Accumulate movement
        cum_move_x += move_x
        cum_move_y += move_y
        cum_scroll += scroll_amount

        # Extract integer part for actual movement
        int_move_x = int(cum_move_x)
        int_move_y = int(cum_move_y)
        int_scroll = int(cum_scroll)

        # Update cumulative movement by removing the integer part
        cum_move_x -= int_move_x
        cum_move_y -= int_move_y
        cum_scroll -= int_scroll

        # Move the mouse if there is any movement
        if int_move_x != 0 or int_move_y != 0:
            pyautogui.moveRel(int_move_x, int_move_y)

        # Scroll the mouse if there is any scroll input
        if int_scroll != 0:
            pyautogui.scroll(-int_scroll)

        # Control the loop speed
        clock.tick(fps)

except KeyboardInterrupt:
    pass

# Quit pygame
pygame.quit()
