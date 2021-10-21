
import cv2 as cv
import numpy as np

from database_connection import DataConnection

#constant parameters
minHessian = 400


class TemplateMatching():

    def __init__(self):
        
        self.detector = cv.SIFT_create()
    
    
        self.DbConnection = DataConnection("localhost", 27017, 'plastic_reidentification')

    def compare_image(self, src_img, dst_img):

        FLANN_INDEX_KDTREE = 0
        
        #Detect the keypoints using SIFT
        kp1, des1 = self.detector.detectAndCompute(src_img, None)

        kp2, des2 = self.detector.detectAndCompute(dst_img, None)
        

        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=10)
        
        search_params = dict(checks=50)

        flann = cv.FlannBasedMatcher(index_params, search_params)

        if(len(kp1) > 2 and len(kp2) >= 2):
            matches = flann.knnMatch(des1, des2, k=2)


        # Filter matches using the Lowe's ratio test    
        ratio_thresh = 0.7
        ratio_thresh_good = 0.6
        keyMatch = 0
        goodMatch = 0

        for i, (m,n) in enumerate(matches):
            if m.distance < ratio_thresh * n.distance:
                keyMatch = keyMatch + 1
            if m.distance < ratio_thresh_good * n.distance:
                goodMatch = goodMatch + 1

        return keyMatch, goodMatch


    def find_matching(self, src_img, max_index = 5):

        #index = max_index

        max_keymatch = 0

        plastic_type = "unknown"

        found_id = 0

        #delete_key = 0


        # search the 5 latest uploaded imgs in the database

        files = self.DbConnection.retrieve_img_from_db(limitation=5)

        #print(files)

        for img in list(files):

            if(img.checked == False):

                print(img.filename)

                nparr = np.frombuffer(img.read(), np.uint8)

                img_np = cv.imdecode(nparr, cv.IMREAD_GRAYSCALE) # convert to GRAY

                #print(img_np)

                #Apply template matching

                keymatch, goodmatch = self.compare_image(src_img, img_np)

                print(keymatch, goodmatch)

                if keymatch > max_keymatch and goodmatch > 3:

                    max_keymatch = keymatch

                    plastic_type = img.plasticType

                    found_id = img._id
        
        if (found_id != 0):

            self.DbConnection.update_field(found_id, "checked", True)


        return found_id, plastic_type