import os
import threading
import csv
from flask import Flask, request
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
            if self.validate_user(userName, userNumber):
                self.generate_image(sketchImage)

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
    
    def generate_image(self, sketchImage):
        workflow = ComfyWorkflowWrapper(FlaskServer.LOCAL_CONFIG_PATH)
        workflow.set_node_param("positive", "text", "a beautiful townhouse")
        
        results = self.api.queue_and_wait_images(workflow, output_node_title="Save Image")
        for file_name, image_data in results.items():
            with open("{}".format(file_name), "wb+") as file:
                file.write(image_data)
    
if __name__ == "__main__":
    nest_asyncio.apply()
    
    comfyUiServer = threading.Thread(target=main.main, daemon=True)
    comfyUiServer.start()
    
    userCredentialsPath = "exampleUserCredentials.csv" # os.environ.get('USER_CREDENTIALS')
    app = FlaskServer(userCredentialsPath)