# import mss
# import numpy as np
#
# with mss.mss() as screenshot:  # sets up the necessary requirements/system to take a screenshot?
#     area_to_capture = {"top": 660, "left": 218, "width": 42, "height": 40}  # mechanism is slightly diff,
#     # you just need the x1 and y1, then calc the diff with x2 y2 and enter the difference
#     image = screenshot.grab(area_to_capture)
#     img_as_array = np.array(image) # the array is height, width, 4 for 4 channels in 1 pixel
#     # print(img_as_array.shape)
#     print(img_as_array)
#     # so to get the first channel aka R value
#     print(img_as_array[:, :, 0])
#     if 48 in img_as_array[:, :, 0]:
#         print('yes')