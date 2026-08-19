FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install CPU-only PyTorch
RUN pip install --no-cache-dir \
    --timeout 1000 \
    --retries 10 \
    torch \
    --index-url https://download.pytorch.org/whl/cpu

# Install remaining dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir \
    --timeout 1000 \
    --retries 10 \
    -r requirements.txt

# Copy application
COPY app ./app
COPY data ./data
COPY static ./static

EXPOSE 8000

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]