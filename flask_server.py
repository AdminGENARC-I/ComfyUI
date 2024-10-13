import os
import threading
import csv
from flask import Flask, request, make_response
import nest_asyncio

from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper

import main

class FlaskServer:
    LOCAL_SERVER_ADDRESS = "http://127.0.0.1:8188/"
    LOCAL_CONFIG_PATH = "workflows/default.json"
    
    def __init__(self, userCredentialsPath: str):
        self.userCredentials = []
        
        self.api = ComfyApiWrapper(FlaskServer.LOCAL_SERVER_ADDRESS)    
        self.app = Flask("Flask Server")
        self.setup_routes()
        self.parse_user_credentials(userCredentialsPath)
        
        self.app.run()
        
        print("Started running flask server...")
        
    def setup_routes(self):
        @self.app.route("/healthCheck", methods=['GET'])
        def healthCheck():
            return "Running!"

        @self.app.route("/generateImage", methods=['POST'])
        def generateImage():
            userName = request.args.get('username')
            userNumber = request.args.get('usernumber')
            sketchImage = request.files['sketch']
            sketchDescription = request.form['description']
            if self.validate_user(userName, userNumber):
                return self.generate_image(sketchImage, sketchDescription)
            
            return "No such user exists!"

    def parse_user_credentials(self, filePath: str):
        try:
            with open(filePath, newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.userCredentials.append((row[0], row[1]))
        except FileNotFoundError:
            print("File {0} not found!".format(filePath))
    
    def validate_user(self, userName: str, userNumber: str) -> bool:
        for userCredential in self.userCredentials:
            if userCredential[0] == userName and userCredential[1] == userNumber:
                return True
        
        return False
    
    def generate_image(self, sketchImage, sketchDescription):
        workflow = ComfyWorkflowWrapper(FlaskServer.LOCAL_CONFIG_PATH)
        workflow.set_node_param("positive", "text", sketchDescription)
        
        results = self.api.queue_and_wait_images(workflow, output_node_title="Save Image")
        for image_name, image_data in results.items():
            response = make_response(image_data)
            response.headers.set('Content-Type', 'image/jpeg')
            response.headers.set('Content-Disposition', 'attachment', filename='%s.jpg' % image_name)
            return response
        
        return "No generated image!"
    
if __name__ == "__main__":
    nest_asyncio.apply()
    
    comfyUiServer = threading.Thread(target=main.main, daemon=True)
    comfyUiServer.start()
    
    userCredentialsPath = "exampleUserCredentials.csv" # os.environ.get('USER_CREDENTIALS')
    app = FlaskServer(userCredentialsPath)