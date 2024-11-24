import os
import threading
import csv
from flask import Flask, request, make_response
from flask_cors import CORS
import time
import nest_asyncio
import gdown
import shutil

from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper

import main

class FlaskServer:
    LOCAL_SERVER_ADDRESS = "http://127.0.0.1:8188/"
    LOCAL_CONFIG_PATH = "workflows/adil_workflow_v1.0.0.json"
    USER_COOLDOWN = 300
    
    def __init__(self, userCredentialsPath: str):
        self.userCredentials = []
        self.userLastRequestTimes = {}
        
        self.api = ComfyApiWrapper(FlaskServer.LOCAL_SERVER_ADDRESS)    
        self.app = Flask("Flask Server")
        CORS(self.app, resources={r"/*": {"origins": "*"}})
        self.setup_routes()
        self.parse_user_credentials(userCredentialsPath)
        
        self.workflow = ComfyWorkflowWrapper(FlaskServer.LOCAL_CONFIG_PATH)
        
        self.app.run(host='0.0.0.0', port=80)
        
        print("Started running flask server...")
        
    def setup_routes(self):
        @self.app.route("/healthCheck", methods=['GET'])
        def healthCheck():
            return "Running!"

        @self.app.route("/generateImage", methods=['POST'])
        def generateImage():
            result = "Invalid username or password.", 403
            
            userName = request.authorization.get('username')
            password = request.authorization.get('password')
            
            print("Got request from {},{}".format(userName, password))
            if self.validate_user(userName, password):
                currentRequestTime = int(time.time())
                lastRequestTime = 0
                if self.userLastRequestTimes.get(userName) != None:
                    lastRequestTime = self.userLastRequestTimes[userName]
                
                passedTime = currentRequestTime - lastRequestTime 
                if passedTime > FlaskServer.USER_COOLDOWN:
                    print("Generating image!")
                    sketchImageFile = request.files['sketch']
                    sketchImageFile.save('temp.jpg')
                    sketchImageMetaData = self.api.upload_image('temp.jpg')
                    imagetype = request.form['imagetype'] 
                    buildingtype = request.form['buildingtype']
                    subregion = request.form['subregion']
                    architect = request.form['architect']
                    atmosphere = request.form['atmosphere']
                    ratio = request.form['ratio']
                    result = self.generate_image(sketchImageMetaData, imagetype, buildingtype, subregion, architect, atmosphere, ratio)
                    if os.path.exists('./temp.jpg'):
                        os.remove('./temp.jpg')
                        
                    self.userLastRequestTimes[userName] = currentRequestTime
                    print("Generated image!")
                else:
                    remainingTime = FlaskServer.USER_COOLDOWN - passedTime
                    minutes = int(remainingTime // 60)
                    seconds = int(remainingTime % 60)
                    result = "You have to wait before making any new requests! Current wait time is {} minutes and {} seconds".format(minutes, seconds), 429
            
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
    
    def generate_image(self, sketchImageMetaData, imagetype, buildingtype, subregion, architect, atmosphere, ratio):        
        self.workflow.set_node_param("Load Image", "image", "{0}/{1}".format(sketchImageMetaData['subfolder'], sketchImageMetaData['name']))
        self.workflow.set_node_param("Architectural Prompt Generator", "architect", architect)
        self.workflow.set_node_param("Architectural Prompt Generator", "region", subregion)
        self.workflow.set_node_param("Architectural Prompt Generator", "building_type", buildingtype)
        self.workflow.set_node_param("Architectural Prompt Generator", "interior_exterior", imagetype.lower())
        self.workflow.set_node_param("Architectural Prompt Generator", "atmosphere", atmosphere)
        self.workflow.set_node_param("Latent Image Resolution", "aspect_ratio", ratio)
        
        results = self.api.queue_and_wait_images(self.workflow, output_node_title="Save Image")
        for image_name, image_data in results.items():
            response = make_response(image_data)
            response.headers.set('Content-Type', 'image/jpeg')
            response.headers.set('Content-Disposition', 'attachment', filename='%s.jpg' % image_name)
            return response
        
        return "No generated image!", 500
    
if __name__ == "__main__":
    extras = [# ('https://drive.google.com/uc?id=1uA9lMI_Wk7Fgj2faHOWkliv-QjDzsP_n', 'realisticVisionV60B1_v51VAE.safetensors', 'models/checkpoints'), 
              ('https://drive.google.com/uc?id=1-sOYJNuCvRB966m30b604sgWvw-boLJU', 'control_v11p_sd15_lineart_fp16.safetensors', 'models/controlnet'),
              ('https://drive.google.com/uc?id=16S-lSU4dqkGfEc6bub0DpCyjkjkDXi4n', 'control_v11f1p_sd15_depth_fp16.safetensors', 'models/controlnet'),
              ('https://drive.google.com/uc?id=1sbEwhjJD_1jW5LP1IORH4WAi1ICYiZfZ', 'mk.safetensors', 'models/loras'),
              ('https://drive.google.com/uc?id=1S4ZEzxxWG4C1pcRK7RvVSr8bQM4ak7q4', 'vae-ft-mse-840000-ema-pruned.ckpt', 'models/vae')]
    for extra in extras:
        if not os.path.exists("{0}/{1}".format(extra[2], extra[1])):
            gdown.download(extra[0], extra[1], quiet=False)
            shutil.move("./{}".format(extra[1]), "./{0}/{1}".format(extra[2], extra[1]))
    
    nest_asyncio.apply()
    
    comfyUiServer = threading.Thread(target=main.main, daemon=True)
    comfyUiServer.start()
    
    userCredentialsPath = os.environ.get('USER_CREDENTIALS')
    app = FlaskServer(userCredentialsPath)