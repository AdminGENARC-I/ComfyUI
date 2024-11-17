#!/bin/bash

source .venv/bin/activate
pip install -r requirements.txt

sudo apt-get install git-lfs
git lfs install
git lfs pull

if ! [ -d "./.venv" ]; then
    python3 -m venv .venv 
fi

if ! [ -d "./models/checkpoints/v1-5-pruned-emaonly.ckpt" ]; then
    wget -c https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt -P ./models/checkpoints/
fi

if ! [ -d "./models/checkpoints/v1-5-pruned.ckpt" ]; then
    wget -c https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5/blob/main/v1-5-pruned.ckpt -P ./models/checkpoints/
fi

if ! [ -d "./custom_nodes/ComfyUI-Manager" ]; then
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git ./custom_nodes/ComfyUI-Manager
fi

if ! [ -d "./custom_nodes/ComfyUI-Advanced-ControlNet" ]; then
    git clone git@github.com:Kosinkadink/ComfyUI-Advanced-ControlNet.git ./custom_nodes/ComfyUI-Advanced-ControlNet
fi

if ! [ -d "./custom_nodes/comfyui_controlnet_aux" ]; then
    git clone https://github.com/Fannovel16/comfyui_controlnet_aux.git ./custom_nodes/comfyui_controlnet_aux
fi

nohup python3 flask_server.py &
deactivate