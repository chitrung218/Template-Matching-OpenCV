
import numpy as np
import cv2 as cv
import glob
from template_matching import TemplateMatching
from database_connection import DataConnection

dst_file = "images/2021-07-01_21h29_22.png"
src_file = 'images/2021-07-01_21h29_22.png'

src_img = cv.imread(src_file, cv.IMREAD_GRAYSCALE)

dst_img = cv.imread(dst_file, cv.IMREAD_GRAYSCALE)


## Convert to bytes
is_success, im_buf_arr = cv.imencode(".jpg", dst_img)

byte_im = im_buf_arr.tobytes()



template_matching_class = TemplateMatching()

#keyMatch, goodMatch = template_matching_class.compare_image(src_img, dst_img)

#print(keyMatch, goodMatch)

#found_id, plastic_type = template_matching_class.find_matching(src_img, max_index = 5)

#print(found_id, plastic_type)



list_record_files = glob.glob("record_image/*.png")

for index, file_ in enumerate(list_record_files):
    
    src_img_temp = cv.imread(file_, cv.IMREAD_GRAYSCALE)

    found_id, plastic_type = template_matching_class.find_matching(src_img_temp, max_index = 5)

    print(found_id, plastic_type)