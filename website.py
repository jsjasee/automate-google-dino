import time
import pyautogui
from selenium import webdriver
from pynput import keyboard
from PIL import ImageGrab, ImageDraw
import mss
import numpy as np

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()  # get hold of ChromeOptions
chrome_options.add_experimental_option("detach", True)  # setting the detach option to true, then pass it into
# webdriver, so it doesn't close automatically

JUMPING_DURATION = 0.6

class WebManager:
    def __init__(self):
        self.should_stop = False
        self.counter = 1 # this is for the naming of screenshots used when debugging
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://elgoog.im/dinosaur-game/")
        time.sleep(5)
        print(f"The screen size is Height: {pyautogui.size().height} by Width: {pyautogui.size().width}")
        self.focus_window()
        self.press_space()
        time.sleep(2)
        self.left_coor = 220
        self.mss_screenshot_obj = mss.mss()
        self.last_jump_time = time.time()

    def press_space(self):
        pyautogui.press('space')

    def focus_window(self):
        pyautogui.moveTo(600, 600)
        pyautogui.click()

    def get_mouse_position(self):

        def on_q_press(key): # key is a argument that is always passed in if using the listener thingy in the pynput module
            try:
                if key.char == 'q': # check if q is pressed before creating the bounding box
                    # self.create_bounding_box()
                    print(f"The mouse is at this position: {pyautogui.position()}")

            # if other keys are pressed will have an AttributeError, that's why need Try Except block
            except AttributeError:
                pass

        with keyboard.Listener(on_press=on_q_press) as listener:
            listener.join() # this is a 'pause' block for the code, basically code will stop here and keep running the listener,
            # until the events eg. on_press returns False, then the 'with .. as' block is exited, and other parts of the code can run

    def check_if_program_stop(self):

        def on_press(key):
            try:
                if key.char == 'p':
                    self.should_stop = True
                    return False
            except AttributeError:
                pass

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        # diff between listener.start() and listener.join():
        # with ... as listener: join()	-> Starts listener, then blocks program (like a pause block) until listener stops.
        # listener.start() ->	Starts listener in background thread, program keeps running.

    def create_bounding_box(self):
        now = time.time()
        # print(f"Another loop is running now at:{now}") # sometimes print consecutively if no cactus detected in that region
        # to check if the cropped screenshot is displaying correctly
        # self.counter += 1

        # screenshot = ImageGrab.grab(bbox=(218, 660, 255, 700)).convert('L') # crop and convert the image to grayscale directly
        # -> note when inputing the bbox aka area to screenshot, can based on the actual screen dimensions,
        # but if you want to crop the screenshot afterwards, either reduce the screenshot size by factor of 2 or
        # times 2 the coordinates (based on the screen dimensions) of the area you want to screenshot, reason below:

        # print(screenshot.size) # macOS scales the image, means the dimensions of the screenshot is TWICE as large as the actual screenshot
        # hence downsize the image before cropping so that the cropped area is accurate.
        # draw = ImageDraw.Draw(screenshot)
        # draw.rectangle((200 * 2, 659 * 2, 250 * 2, 715 * 2), outline="red", width=2)
        # screenshot.save(f"screenshot{self.counter}.png")

        # cropped = screenshot.crop((200 * 2, 659 * 2, 250 * 2, 715 * 2)) # (x1, y1, x2, y2)

        # cropped.save(f"bounding_box{self.counter}.png")
        # cropped.show()
        # print('cropped picture!')

        # if self.detect_obstacle(cropped_img=screenshot):
        #     print('jumped!')
        #     pyautogui.press('space')

        if self.faster_detect_obstacle(area_to_capture={"top": 657, "left": self.left_coor, "width": 45, "height": 40}):
            self.last_jump_time = time.time()
            pyautogui.press('space')
            print(f'FAR jumped! at {self.last_jump_time}')
            if self.left_coor < 700:
                self.left_coor *= 1.01
            print(self.left_coor)
            # self.queue_consecutive_jump(now)

        elif self.faster_detect_obstacle(area_to_capture={"top": 610, "left": self.left_coor -5, "width": 45, "height": 40}):
            pyautogui.keyDown('down')
            time.sleep(0.25)
            pyautogui.keyUp('down')
            print('FAR ducked!')

        # maybe add mid detection zone here?

        # close detection zone
        if self.faster_detect_obstacle(area_to_capture={"top": 657, "left": 235, "width": 40, "height": 40}):
            # this is a safety net
            pyautogui.press('space')
            print('CLOSE jumped! when its closest')
            if self.left_coor < 700:
                self.left_coor *= 1.01

        elif self.faster_detect_obstacle(area_to_capture={"top": 610, "left": 230, "width": 40, "height": 40}):
            print('CLOSE ducked! when its closest')
            pyautogui.keyDown('down')
            time.sleep(0.25)
            pyautogui.keyUp('down')

    def queue_consecutive_jump(self, time_now):
        if time_now - self.last_jump_time < JUMPING_DURATION:
            print('yes checking air borne status!')
            # check if there's a cactus nearby maybe in the middle region
            if self.faster_detect_obstacle(area_to_capture={"top": 657, "left": 300, "width": 40, "height": 40}):
                time.sleep(JUMPING_DURATION - (time_now - self.last_jump_time))
                pyautogui.press('space')
                print('consecutive cactus! JUMPED! again!')


    def detect_obstacle(self, cropped_img):
        # gray_scale = cropped_img.convert('L') # gray_scale changes the image to black and white, basically having 1 channel instead of 3 RGB channels
        pixels = cropped_img.getdata() # this is a PixelAccessObject which helps you to get the pixels based on the the x and y coordinates.
        # it is not a list where you can loop through the object and get each pixel like cannot do: 'for pixel in pixels'
        # you can only access the pixel in pixels with 'pixels[x, y] -> where x and y is the coordinate of the pixel
        # for x in range(cropped_img.width):
        #     for y in range(cropped_img.height):
        #         pixel_accessed = pixels[x, y]
        #         # print(pixel_accessed)
        #         if pixel_accessed == 83: # the grey colour have value 83 to be exact
        #             print('obstacle detected!')
        #             return True

        # to make the loop faster:
        if 83 in pixels:
            print('obstacle detected!')
            return True

    # Faster method
    def faster_detect_obstacle(self, area_to_capture):
        # with mss.mss() as screenshot: # sets up the necessary requirements/system to take a screenshot?
        #     # area_to_capture = {"top": 660, "left": 218, "width": 42, "height": 40} # mechanism is slightly diff,
        #     # # you just need the x1 and y1, then calc the diff with x2 y2 and enter the difference
        #     # top_area = {"top": 628, "left": 218, "width": 42, "height": 40} # this hopefully gets the image of the bird
        #
        #     image = screenshot.grab(area_to_capture)
        #     img_as_array = np.array(image)
        #     # print(img_as_array)
        #
        #     if any(num in img_as_array[:,:,0] for num in range(83, 172 + 1)):
        #         print('obstacle detected!')
        #         return True
        #
        #     # if any(num in img_as_array[:,:,0] for num in [83, 172]): # shorter and faster version of the condition below
        #     #     print('obstacle detected!')
        #     #     return True
        #
        #     # if 83 in img_as_array[:,:,0] or 172 in img_as_array[:,:,0]: # the 172 is for night mode
        #     #     print('obstacle detected!')
        #     #     return True

        # instead of creating the mss object every time the function is run, create it once and then use it
        image = self.mss_screenshot_obj.grab(area_to_capture)
        img_as_array = np.array(image)
        blue_channel_values = img_as_array[:,:,0]

        if np.any((blue_channel_values >= 83) & (blue_channel_values <= 172)):
            print('obstacle detected!')
            return True

        # np.any() checks if any element in a NumPy array is True.
        # any() is for normal Python iterables (like lists or tuples), but does not work properly with NumPy arrays of booleans—it can be ambiguous or error-prone.
        #
        # The & operator combines two boolean arrays element-wise. It returns a new array where each position is True only if both conditions were True at that position.
