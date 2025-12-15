# align/aligner.py
import numpy as np
import cv2

ARC_FACE_TEMPLATE = np.float32([
    [38.2946, 51.6963],
    [73.5318, 51.5014],
    [56.0252, 71.7366],
    [41.5493, 92.3655],
    [70.7299, 92.2041]
])

def align_face(img, lm10):

    h, w = img.shape[:2]
    pts_src = np.array(lm10, dtype=np.float32).reshape(5, 2)
    pts_src[:, 0] *= w
    pts_src[:, 1] *= h
    
    M = cv2.estimateAffinePartial2D(pts_src, ARC_FACE_TEMPLATE)[0]

    aligned = cv2.warpAffine(img, M, (112, 112))
    return aligned

def align_face487(img, lm487):
    # Lấy 5 điểm từ 487 landmarks
    pts_src = np.float32([
        lm487[33],
        lm487[263],
        lm487[1],
        lm487[61],
        lm487[291]
    ])

    M = cv2.estimateAffinePartial2D(pts_src, ARC_FACE_TEMPLATE)[0]
    aligned = cv2.warpAffine(img, M, (112, 112))
    return aligned
