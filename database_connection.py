from bson.objectid import ObjectId
from pymongo import MongoClient
import gridfs
import numpy as np
import cv2
import glob
class DataConnection():

    def __init__(self, hostName, portNumber, databaseName):

        self.hostName = hostName
        
        self.portNumber = portNumber
        
        self.databaseName = databaseName

        # Connect to the server with the hostName and portNumber.
        connection = MongoClient(hostName, portNumber)

        # Connect to the Database where the images will be stored.
        self.database = connection[databaseName]

        self.fs = gridfs.GridFS(self.database)
    
    def save_to_db(self, image_data, file_name, plastic_type="unknown"):
        ''' Purpose: to save image in the database
        Args:
            - image_data (bytes): binary image data
            - file_name (str): name of the file saved in the database
            - plastic_type (str): type of the plastic
        '''

        if(type(image_data) is not bytes):

            print("image_data should be byte array")
        
        else:

            self.fs.put(image_data, filename=file_name, checked = False, plasticType = plastic_type)

    def retrieve_img_from_db(self, limitation=3) :
        '''Purpose: Retrieve list of images based on uploadData with limitation to 3
        Args: 
            - limitation (default=3): limited number of images

        Return:
            list of files 
        '''

        files = self.fs.find({"checked": False}).sort("uploadDate", 1).limit(limitation)

        '''
        for img in list(files):

            if(img.checked == False):
                print("not checked")
        '''

        '''
        nparr = np.frombuffer(list(files)[2].read(), np.uint8)

        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR) 

        cv2.imwrite('color_img.jpg', img_np)
        cv2.imshow("image", img_np)
        cv2.waitKey()
        cv2.destroyAllWindows()
        '''

        return files
    
    def retrive_img_by_id(self, found_id):

        file = self.fs.find_one({"_id": found_id})

        return file
    
    def update_field(self, id, field, value):

        if(field == "checked"):

            col = self.database["fs.files"]

            doc = col.find_one_and_update(
            {"_id" : ObjectId(id)},
            {"$set":
                {"checked": value}
            },upsert=True
        )
if __name__ == "__main__":
    

    db_connection = DataConnection("localhost", 27017, 'plastic_reidentification')

    #db_connection.retrive_img_from_db();

    #db_connection.update_field('616fdd2cbe33d91e80065039',"checked", value=True)
        
    list_record_files = glob.glob("record_image/*.png")

    print(list_record_files)

    for index, file_ in enumerate(list_record_files):
        
        with open(file_, 'rb') as f:
            contents = f.read()
            db_connection.save_to_db(contents, "file_"+str(index))