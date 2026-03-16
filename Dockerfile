# Stage 1: Build the frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
# Set production API URL (relative to the same host)
ENV VITE_API_URL=""
RUN npm run build

# Stage 2: Final image (Python 3.11)
FROM python:3.11-slim

# Install system dependencies for pandas/numpy/matplotlib
RUN apt-get update && apt-get install -y \
    build-essential \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up a new user named "user" with user id 1000
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy backend requirements and install
COPY --chown=user backend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy backend code
COPY --chown=user backend/app ./app
COPY --chown=user backend/samples ./samples

# Ensure work directories exist and have correct permissions
RUN mkdir -p uploads charts samples

# Copy built frontend from Stage 1
COPY --from=frontend-builder --chown=user /app/frontend/dist ./frontend/dist

# Environment variables
ENV PORT=7860
ENV PYTHONUNBUFFERED=1

# Expose the port HF Spaces uses
EXPOSE 7860

# Command to run the application using uvicorn
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
