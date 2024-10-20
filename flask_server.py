import os
import threading
import csv
from flask import Flask, request, make_response
from flask_cors import CORS
import nest_asyncio
import gdown
import shutil

from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper

import main

class FlaskServer:
    LOCAL_SERVER_ADDRESS = "http://127.0.0.1:8188/"
    LOCAL_CONFIG_PATH = "workflows/adilWorkflow_v0.0.1.json"
    
    def __init__(self, userCredentialsPath: str):
        self.userCredentials = []
        
        self.api = ComfyApiWrapper(FlaskServer.LOCAL_SERVER_ADDRESS)    
        self.app = Flask("Flask Server")
        CORS(self.app)
        self.setup_routes()
        self.parse_user_credentials(userCredentialsPath)
        
        self.workflow = ComfyWorkflowWrapper(FlaskServer.LOCAL_CONFIG_PATH)
        
        self.app.run()
        
        print("Started running flask server...")
        
    def setup_routes(self):
        @self.app.route("/healthCheck", methods=['GET'])
        def healthCheck():
            return "Running!"

        @self.app.route("/generateImage", methods=['POST'])
        def generateImage():
            result = "No such user exists!"
            
            userName = request.authorization.get('username')
            password = request.authorization.get('password')
            if self.validate_user(userName, password):
                sketchImageFile = request.files['sketch']
                sketchImageFile.save('temp.jpg')
                sketchImageMetaData = self.api.upload_image('temp.jpg')
                subregion = request.form['subregion']
                architect = request.form['architect'] 
                result = self.generate_image(sketchImageMetaData, subregion, architect)
            
            if os.path.exists('./temp.jpg'):
                os.remove('./temp.jpg')
            
            return result

    def parse_user_credentials(self, filePath: str):
        try:
            with open(filePath, newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.userCredentials.append((row[0], row[1]))
        except FileNotFoundError:
            print("File {0} not found!".format(filePath))
    
    def validate_user(self, userName: str, password: str) -> bool:
        for userCredential in self.userCredentials:
            if userCredential[0] == userName and userCredential[1] == password:
                return True
        
        return False
    
    def generate_image(self, sketchImageMetaData, subregion, architect):
        self.workflow.set_node_param("Load Image", "image", "{0}/{1}".format(sketchImageMetaData['subfolder'], sketchImageMetaData['name']))
        self.workflow.set_node_param("First Text Prompt", "text", "{0}, {1}".format(subregion, architect))
        
        results = self.api.queue_and_wait_images(self.workflow, output_node_title="Save Image")
        for image_name, image_data in results.items():
            response = make_response(image_data)
            response.headers.set('Content-Type', 'image/jpeg')
            response.headers.set('Content-Disposition', 'attachment', filename='%s.jpg' % image_name)
            return response
        
        return "No generated image!"
    
if __name__ == "__main__":
    extras = [('https://drive.google.com/uc?id=1LKq_8HblgJYC3iButkOItDM-NsZLETlv', 'realisticVisionV60B1_v51VAE.safetensors', 'models/checkpoints'), 
              ('https://drive.google.com/uc?id=1-sOYJNuCvRB966m30b604sgWvw-boLJU', 'control_v11p_sd15_lineart_fp16.safetensors', 'models/controlnet')]
    for extra in extras:
        if not os.path.exists("{0}/{1}".format(extra[2], extra[1])):
            gdown.download(extra[0], extra[1], quiet=False)
            shutil.move("./{}".format(extra[1]), "./{0}/{1}".format(extra[2], extra[1]))
    
    nest_asyncio.apply()
    
    comfyUiServer = threading.Thread(target=main.main, daemon=True)
    comfyUiServer.start()
    
    userCredentialsPath = "exampleUserCredentials.csv" # os.environ.get('USER_CREDENTIALS')
    app = FlaskServer(userCredentialsPath)