import urllib.request

import torch
import json
import numpy as np
import torchvision.transforms as transforms
import pandas as pd
from PIL import Image
from io import BytesIO
import urllib.request
import requests



## Class Mapping
class_to_index = {np.int64(k):v for k,v in json.loads(open("resnet50_50imgs_top3000.json","r").read()).items()}
index_to_class = {v:k for k,v in class_to_index.items()}

## load the train csv
image_repo = pd.read_csv("./train.csv")

## Load Model

model = torch.load("resnet50model.pt", map_location=torch.device('cpu'))

image_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


def predict_image(filename, model = model, transform=image_transform, class_map=index_to_class):

    ## Image transformation
    image = transform(filename)
    image = image[None, :, :, :]  ## Adding a single dimension to image
    image = image.to('cpu')

    model = model.eval()
    with torch.no_grad():
        output = model.forward(image)
        score, pred = torch.max(output, 1)
        pred_label = class_map[pred.item()]
        data = {'Prediction Landmark': pred_label, "Score": score.item()}
        urls = image_repo[image_repo['landmark_id'] == pred_label].sample(30, replace='True')['url'].to_list()

    return pred_label, urls




