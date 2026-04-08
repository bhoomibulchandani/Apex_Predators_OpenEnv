# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables for Gradio
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    GRADIO_SERVER_NAME="0.0.0.0" \
    GRADIO_SERVER_PORT=7860

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first
COPY requirements.txt .

# CRITICAL FIX: Install UI dependencies AND your Backend dependencies!
RUN pip install --no-cache-dir gradio pandas numpy scikit-learn pydantic openai

# CRITICAL FIX: Copy the ENTIRE repository (so Meta can see inference.py)
COPY . .

# Expose the port Gradio will run on
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the UI application
CMD ["python", "server/ui.py"]
