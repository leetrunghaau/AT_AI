# service.py
from embeddings.arcface import ArcFaceEmbedding
from align.aligner import align_face
from database.faiss_db import FaceDB

class FaceService:
    def __init__(self):
        self.embedder = ArcFaceEmbedding()
        self.db = FaceDB()

    def register(self, images, landmarks_list, user_id):
        vectors = []
        for img, lm in zip(images, landmarks_list):
            aligned = align_face(img, lm)
            vec = self.embedder.embed(aligned)
            vectors.append(vec)

        mean_vec = sum(vectors) / len(vectors)
        self.db.add(mean_vec, user_id)
        return {"status": "ok"}

    def recognize(self, img, landmarks):
        aligned = align_face(img, landmarks)
        vec = self.embedder.embed(aligned)
        uid, dist = self.db.search(vec)
        return {"user_id": uid, "distance": dist}
