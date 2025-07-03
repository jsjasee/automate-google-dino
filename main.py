from website import WebManager

website_manager = WebManager()

# This code is to get the coordinates of the mouse to determine the bounding box
# website_manager.get_mouse_position()

# this is a background listener -> so that both while loop and listener can run at the same time
website_manager.check_if_program_stop()

while not website_manager.should_stop:
    website_manager.create_bounding_box()

# todo: use PIL to get screenshots of an image in a while loop
# todo: crop the screenshot to the bounding box
# todo: detect when there is a black pixel in the bounding box
# todo: if yes, then jump
# todo: define a top bounding box as well to know when to duck instead of jump
# todo: use pixels to determine when to get the dino to jump

# improving the screenshot system from PIL to mss so the dino can jump in time
# with.. as.. is a context manager that cleans up automatically once done with the operation

