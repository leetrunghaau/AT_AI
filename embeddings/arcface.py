# embeddings/arcface.py
import onnxruntime as ort
import numpy as np
import cv2

class ArcFaceEmbedding:
    def __init__(self, model_path="models/AuraFace-v1/glintr100.onnx"):
        self.session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])

    def preprocess(self, img):
        img = cv2.resize(img, (112, 112))
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR -> RGB + CHW
        img = img.astype(np.float32)
        img = (img - 127.5) / 128.0
        img = np.expand_dims(img, axis=0)
        return img

    def embed(self, img):
        blob = self.preprocess(img)
        vec = self.session.run(None, {"data": blob})[0]
        vec = vec / np.linalg.norm(vec)
        return vec.reshape(-1)
