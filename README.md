# Face Recognition API

[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-performance, scalable, and production-ready face recognition API built with FastAPI, ONNX, and Faiss.

## Overview

This project provides a robust API for face recognition tasks. It allows you to register users with one or more images and then recognize them from new images. The system is designed for efficiency, using the lightweight **AuraFace-v1** model for feature extraction and **Faiss** for rapid similarity searches in the vector database.

## Key Technologies

- **Backend Framework**: FastAPI
- **Deep Learning Model**: AuraFace-v1 (via ONNX Runtime)
- **Vector Database**: Faiss (Facebook AI Similarity Search)
- **Async Server**: Uvicorn
- **Containerization**: Docker & Docker Compose

## Features

- **User Registration**: Register a `user_id` by averaging feature embeddings from multiple images.
- **Face Recognition**: Identify a user from a new image, returning their `user_id` and a similarity score.
- **Efficient Search**: Utilizes Faiss for near-instantaneous lookups even with millions of vectors.
- **Scalable**: Built with modern async Python and container-ready for easy scaling.

---

## Getting Started

### Prerequisites

- Git
- Python 3.10+
- Docker & Docker Compose (Recommended for deployment)

### 1. Clone the Repository

```bash
git clone https://github.com/leetrunghaau/AT_AI.git
cd AT_AI
```

### 2. Download the Model

The **AuraFace-v1** model is not included in this repository. You must download it manually from Hugging Face.

- **Source**: [AuraFace-v1 on Hugging Face](https://huggingface.co/fal/AuraFace-v1/tree/main)
- **Action**: Create a `models/AuraFace-v1/` directory and place all downloaded `.onnx` files inside.

### 3. Install Dependencies

It is highly recommended to use a Python virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

---

## Configuration

For a production environment, it is recommended to configure the application using environment variables.

| Variable               | Description                                       | Default                             |
| ---------------------- | ------------------------------------------------- | ----------------------------------- |
| `ARCFACE_MODEL_PATH`   | Path to the ONNX face embedding model.            | `models/AuraFace-v1/glintr100.onnx` |
| `FACE_DB_INDEX_PATH`   | Path to save the Faiss index file.                | `face.index`                        |
| `FACE_DB_IDS_PATH`     | Path to save the user IDs JSON file.              | `face_ids.json`                     |
| `FACE_DB_THRESHOLD`    | Maximum distance for a positive match.            | `0.6`                               |
| `MAX_UPLOAD_SIZE_MB`   | Maximum size for uploaded files (in MB).          | `50`                                |
| `HOST`                 | Host address to bind the server to.               | `0.0.0.0`                           |
| `PORT`                 | Port to run the server on.                        | `8000`                              |

---

## Usage

### Running Locally

To start the development server, use the following command:

```bash
uvicorn face_service:app --host $HOST --port $PORT
```

---

## Deployment

### Docker

Build and run the container using the provided `Dockerfile`.

```bash
# 1. Build the image
docker build -t face-recognition-api .

# 2. Run the container
docker run -d -p 8000:8000 --name face-api face-recognition-api
```

### Docker Compose (Recommended)

For a more robust setup, use the provided `docker-compose.yml` file. This simplifies management and configuration.

```bash
# Build and start the services in detached mode
docker-compose up --build -d

# Stop and remove the services
docker-compose down
```

### Template for a Master Docker Compose

To integrate this service into a larger microservices architecture, add the following to your main `docker-compose.yml` file.

```yaml
# --- In your master docker-compose.yml ---

services:
  # ... other services

  # --- Face Recognition API Service ---
  face-api:
    build:
      context: /path/to/your/face-recognition-project # <-- EDIT: Path to this project
    container_name: face-api
    restart: unless-stopped
    volumes:
      # Mount models directory from the host to avoid rebuilding
      - /path/to/your/face-recognition-project/models:/app/models # <-- EDIT: Path to models
    networks:
      - your_shared_network # <-- EDIT: Connect to your existing shared network
    environment:
      - FACE_DB_THRESHOLD=0.5
      - MAX_UPLOAD_SIZE_MB=100
    # If not using a reverse proxy, expose the port:
    # ports:
    #   - "8000:8000"

# --- Add this to your top-level networks definition ---
# networks:
#   your_shared_network:
#     external: true
```

---

## API Endpoints

### `POST /register`

Registers a user by associating a `user_id` with one or more face images.

**`curl` Example:**
```bash
curl -X POST "http://localhost:8000/register" \
-F "user_id=user_01" \
-F "files=@/path/to/image1.jpg" \
-F "files=@/path/to/image2.png" \
-F 'landmarks=[[[0.38, 0.51], ...], [[0.39, 0.52], ...]]' 
```

### `POST /recognize`

Recognizes a person from a single image against the database.

**`curl` Example:**
```bash
curl -X POST "http://localhost:8000/recognize" \
-F "file=@/path/to/unknown_person.jpg" \
-F 'landmarks=[[0.38, 0.51], ...]' 
```

- **Success Response**: `{"user_id": "user_01", "distance": 0.2345}`
- **Not Found Response**: `{"user_id": null, "distance": null}`

---

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss your ideas.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.