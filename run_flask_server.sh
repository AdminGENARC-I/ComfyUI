#!/bin/bash

echo "Make sure you set up your branch name in colab_runner.ipynb"

source .venv/bin/activate
pip install -r requirements.txt

if ! [ -d "./.venv" ]; then
    python3 -m venv .venv 
fi

if ! [ -d "./models/checkpoints/v1-5-pruned-emaonly.ckpt"]; then
    wget -c https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt -P ./models/checkpoints/
fi

if ! [ -d "./custom_nodes/ComfyUI-Manager"]; then
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git ./custom_nodes/ComfyUI-Manager
fi

if ! [ -d "./custom_nodes/ComfyUI-Advanced-ControlNet"]; then
    git clone git@github.com:Kosinkadink/ComfyUI-Advanced-ControlNet.git ./custom_nodes/ComfyUI-Advanced-ControlNet
fi

python3 flask_server.py
deactivate