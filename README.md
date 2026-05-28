# AI Spam Detector API

A REST API that detects spam messages using Hugging Face transformers (BERT-tiny model fine-tuned for SMS spam detection).

## Features

- 🔍 Detect spam messages with confidence scores
- 💾 Store all requests in PostgreSQL database
- 📜 View request history
- 🐳 Docker containerization
- ✅ Health check endpoint

## Tech Stack

- FastAPI
- PostgreSQL
- Hugging Face Transformers
- Docker & Docker Compose
- SQLAlchemy

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
git clone <your-repo-url>
cd <project-directory>
2. Copy environment variables:
cp .env.example .env

3. Build and run with Docker Compose:
docker compose up --build

4. API will be available at: http://localhost:8000
