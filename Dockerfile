# Stage 1: Build the frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
# Set production API URL (relative to the same host)
ENV VITE_API_URL=""
RUN npm run build

# Stage 2: Final image
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies for pandas/numpy/matplotlib
RUN apt-get update && apt-get install -y \
    build-essential \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/app ./app
COPY backend/samples ./samples
# Ensure work directories exist
RUN mkdir -p uploads charts samples

# Copy built frontend from Stage 1
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Environment variables
ENV PORT=7860
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

# Expose the port HF Spaces uses
EXPOSE 7860

# Command to run the application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
