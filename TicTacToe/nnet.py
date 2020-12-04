import torch
import torch.nn as nn
import torch.nn.functional as F


torch.set_printoptions(profile="full")


class ConvBlock(nn.Module):

    def __init__(self, nb_in_planes, nb_kernels):
        super().__init__()
        # Bias is disabled because it's already managed by batch normalization.
        self.conv = nn.Conv2d(nb_in_planes, nb_kernels, kernel_size=1, stride=1, bias=False)
        self.bn = nn.BatchNorm2d(nb_kernels)
    
    def forward(self, t):
        t = F.relu(self.bn(self.conv(t)))
        return t


class ResBlock(nn.Module):

    def __init__(self, nb_kernels):
        super().__init__()
        self.conv1 = nn.Conv2d(nb_kernels, nb_kernels, kernel_size=1, stride=1, bias=False)
        self.bn1 = nn.BatchNorm2d(nb_kernels)
        self.conv2 = nn.Conv2d(nb_kernels, nb_kernels, kernel_size=1, stride=1, bias=False)
        self.bn2 = nn.BatchNorm2d(nb_kernels)
    
    def forward(self, t):
        residual = t
        t = F.relu(self.bn1(self.conv1(t)))
        t = self.bn2(self.conv2(t))
        t = t + residual
        t = F.relu(t)
        return t


class OutBlock(nn.Module):

    def __init__(self, nb_kernels):
        super().__init__()
        self.conv3 = nn.Conv2d(nb_kernels, nb_kernels//2, kernel_size=1, stride=1, bias=False)
        self.bn2 = nn.BatchNorm2d(nb_kernels//2)
        self.fc1 = nn.Linear(nb_kernels//2*3*3, 128)
        self.fc2 = nn.Linear(128, 3*3)
    
    def forward(self, t):
        v = F.relu(self.bn2(self.conv3(t)))
        v = v.flatten(start_dim=1)
        v = F.relu(self.fc1(v))
        v = torch.tanh(self.fc2(v))
        v = v.reshape(-1, 3, 3)
        return v


class NNet(nn.Module):

    def __init__(self, nb_kernels, nb_res_blocks):
        super().__init__()
        self.nb_res_blocks = nb_res_blocks
        self.convBlock = ConvBlock(3, nb_kernels)
        for i in range(nb_res_blocks):
            setattr(self, f"resBlock{i}", ResBlock(nb_kernels))
        self.outBlock = OutBlock(nb_kernels)
    
    def forward(self, t):
        t = self.convBlock(t)
        for i in range(self.nb_res_blocks):
            t = getattr(self, f"resBlock{i}")(t)
        t = self.outBlock(t)
        return t