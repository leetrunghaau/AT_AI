import faiss
import numpy as np
import json
import os
import atexit

class FaceDB:
    def __init__(self, dim=512, index_path="face.index", ids_path="face_ids.json"):
        self.dim = dim
        self.index_path = index_path
        self.ids_path = ids_path
        self.ids = []

        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
            print(f"[FaceDB] Loaded index from {index_path}")
        else:
            self.index = faiss.IndexFlatL2(dim)

        if os.path.exists(ids_path):
            with open(ids_path, "r", encoding="utf-8") as f:
                self.ids = json.load(f)
            print(f"[FaceDB] Loaded {len(self.ids)} IDs from {ids_path}")

        atexit.register(self.save)

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.ids_path, "w", encoding="utf-8") as f:
            json.dump(self.ids, f)
        print(f"[FaceDB] Saved index and IDs")

    # def add(self, vec, user_id):
    #     vec = np.asarray(vec).reshape(1, -1)
    #     self.index.add(vec)
    #     self.ids.append(user_id)
    def add(self, vec, user_id):
        vec = np.asarray(vec).reshape(1, -1)

        # === CHECK ID CÓ TỒN TẠI CHƯA ===
        if user_id in self.ids:
            i = self.ids.index(user_id)
            print(f"[FaceDB] ID {user_id} exists → updating vector at index {i}")

            # Thay thế vector trong FAISS
            try:
                faiss.replace_vectors(self.index, vec, np.array([i], dtype=np.int64))
            except AttributeError:
                # Fall-back nếu Faiss cũ: Rebuild index
                print("[FaceDB] replace_vectors not supported → rebuilding index")
                all_vecs = np.zeros((len(self.ids), self.dim), dtype=np.float32)
                for k in range(len(self.ids)):
                    all_vecs[k] = self.index.reconstruct(k)
                all_vecs[i] = vec  # thay vector index i

                self.index = faiss.IndexFlatL2(self.dim)
                self.index.add(all_vecs)

        else:
            # === ID MỚI → ADD BÌNH THƯỜNG ===
            self.index.add(vec)
            self.ids.append(user_id)
            print(f"[FaceDB] Added new ID {user_id}")


    def search(self, vec, threshold=0.6):
        if len(self.ids) == 0:
            return None, None 

        vec = np.asarray(vec).reshape(1, -1)
        D, I = self.index.search(vec, 1)
        idx = int(I[0][0])
        dist = float(D[0][0])

        if idx == -1 or idx >= len(self.ids) or dist > threshold:
            return None, None

        return self.ids[idx], dist