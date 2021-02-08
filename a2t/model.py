import numpy as np
import tempfile
from torch import nn
from torchvision import datasets, transforms
from torchvision.transforms import functional as F
import torch
from torch.utils import data
from PIL import Image

class DialogueCrop(object):
    """Crop to where the dialogue will appear.

    Args:
        output_size (tuple or int): Desired output size. If int, square crop
            is made.
    """

    def __init__(self, size):
        self.size = size

    def __call__(self, img):
        return F.resize(F.crop(img, 610, 325, 400, 1275), self.size)
    
transform = transforms.Compose([
    DialogueCrop((224, 224)),
    transforms.ToTensor(),
])


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # convolutional layer
        self.conv1 = nn.Conv2d(3, 16, 5)
        # max pooling layer
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 32, 5)
        self.dropout = nn.Dropout(0.2)
        self.fc1 = nn.Linear(32*53*53, 256)
        self.fc2 = nn.Linear(256, 84)
        self.fc3 = nn.Linear(84, 2)
        self.softmax = nn.LogSoftmax(dim=1)
        
    def forward(self, x):
        # add sequence of convolutional and max pooling layers
        x = self.pool(nn.functional.relu(self.conv1(x)))
        x = self.pool(nn.functional.relu(self.conv2(x)))
        x = self.dropout(x)
        x = x.view(-1, 32 * 53 * 53)
        x = nn.functional.relu(self.fc1(x))
        x = self.dropout(nn.functional.relu(self.fc2(x)))
        x = self.softmax(self.fc3(x))
        return x

model = Net()
model.load_state_dict(torch.load('./model_cifar.pt'))