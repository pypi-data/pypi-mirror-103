import os, pdb
import numpy as np
import torch
import torchvision
from PIL import Image
import urllib.request
import requests
import shutil
import torch.nn.functional as F

class ResizeDataset(torch.utils.data.Dataset):
    """
    A placeholder Dataset that enables parallelizing the resize operation 
    using multiple CPU cores

    files: list of all files in the folder
    fn_resize: function that takes an np_array as input [0,255]
    """
    def __init__(self, files, size=(299,299), fn_resize=None):
        self.files = files
        self.transforms = torchvision.transforms.ToTensor()
        self.size=size
        self.fn_resize = fn_resize


    def __len__(self):
        return len(self.files)

    def __getitem__(self, i):
        path = str(self.files[i])
        if ".npy" in path:
            img_np = np.load(path)
        else:
            img_pil = Image.open(path).convert('RGB')
            img_np = np.asarray(img_pil)
        
        # fn_resize expects a np array and returns a np array
        img_resized = self.fn_resize(img_np)

        # ToTensor() converts to [0,1] only if input in uint8
        if img_resized.dtype == "uint8":
            img_t = self.transforms(img_resized)
        elif img_resized.dtype == "float32":
            img_t = self.transforms(img_resized)/255.0

        return img_t


class TensorResizeDataset(torch.utils.data.Dataset):
    """
    A placeholder Dataset that splits a batch and resizes each
    image individually

    batch: batch of images to be resized in range[0,1]
    fn_resize: function that takes an np_array as input [0,255]
    """
    def __init__(self, batch, fn_resize=None):
        # permute to match npy channel order
        #self.batch = (batch.permute(0, 2, 3, 1) * 255).numpy()
        self.batch = batch.cpu()
        self.transforms = torchvision.transforms.ToTensor()
        self.fn_resize = fn_resize
    def __len__(self):
        return self.batch.shape[0]
    def __getitem__(self, i):
        # curr img
        #img_pil = torchvision.transforms.ToPILImage()()
        #img_np = np.asarray(img_pil)
        img_np = self.batch[i].numpy().transpose((1,2,0))

        img_resized = self.fn_resize(img_np)
        # convert back to torch tensors -> [0,1]
        return self.transforms(img_resized)


# def np_pil_bicubic(x, size):
#     x = Image.fromarray(x)
#     x = x.resize(size, resample=Image.BICUBIC)
#     x = np.array(x)
#     return x

# input range is [0,255]
# output range is [0,255]
# def np_tf_bilinear(x, size):
#     x = tf.constant(x)[tf.newaxis, ...]
#     x = tf.image.resize(x, size, method="bilinear", antialias=False)
#     x = x[0,...].numpy().clip(0,255)
#     return x

"""
x is np array in range[0,255]
"""
# def pil_bicubic_resize(x):
#     #x = x.clip(0,255).astype(np.uint8)
#     x = Image.fromarray(x)
#     x = x.resize((299,299), resample=Image.BICUBIC)
#     return x

# def pil_float_bicubic_resize(x_np):
#     def resize_1ch(img_np):
#         img = Image.fromarray(img_np.astype(np.float32), mode='F')
#         img = img.resize((299,299), resample=Image.BICUBIC)
#         return np.asarray(img).reshape(299,299,1)
#     img_out = [resize_1ch(x_np[:,:,idx]) for idx in range(3)]
#     out = np.concatenate(img_out, axis=2).astype(np.float32)/255.0
#     return out

"""
img_np is in range[0,255]
resized output is in range[0,1]
"""
# def pytorch_bilinear_resize(img_np):
#     img_tens = torch.Tensor(img_np.transpose((2,0,1)))[None,...]
#     interp_tens = F.interpolate(img_tens,
#                             size=(299, 299),
#                             mode="bilinear")
#     interp_np = interp_tens[0,...].cpu().data.numpy().transpose((1,2,0)).clip(0,255)
#     return interp_np/255.0

"""
img_np is in range[0,255]
resized output is in range[0,1]
"""
# def tf_bilinear_resize(img_np):
#     x = tf.constant(img_np)[tf.newaxis, ...]
#     x = tf.image.resize(x, (299,299), method="bilinear", antialias=False)
#     x = x[0,...].numpy().clip(0,255)/255.0
#     # pdb.set_trace()
#     return x

EXTENSIONS = {'bmp', 'jpg', 'jpeg', 'pgm', 'png', 'ppm',
                    'tif', 'tiff', 'webp', 'npy'}





