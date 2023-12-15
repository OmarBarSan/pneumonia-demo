import numpy as np
import cv2

def pad_image(frame, goal):
  # Pad horizontal
  if frame.shape[1] < goal:
    pad = goal - frame.shape[1]
    pad1 = int(pad/2)
    pad2 = int(pad/2) + int(pad%2)
    frame =np.pad(frame, [[0,0],[pad1,pad2]], "constant", constant_values=[[0],[0]])
  # Pad vertical
  if frame.shape[0] < goal:
    pad = goal - frame.shape[0]
    pad1 = int(pad/2)
    pad2 = int(pad/2) + int(pad%2)
    frame =np.pad(frame, [[pad1,pad2],[0,0]], "constant", constant_values=[[0],[0]])
  return frame

def equalize(frame):
  clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8,8))
  equalized = clahe.apply(frame)
  return equalized

def normalize(frame):
  frame = frame.astype(np.float32)/255
  return frame

def preprocess_image(frame):
    frame = equalize(frame)
    max_shape = max(frame.shape)
    frame = pad_image(frame, max_shape)
    frame = pad_image(frame, 1024)
    frame = normalize(frame)
    frame = cv2.resize(frame, (1024,1024))

    return frame