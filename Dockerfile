FROM python:3.9-slim
WORKDIR /app
RUN apt-get update \
    && apt-get install -y gcc g++ \
    && apt-get install ffmpeg libsm6 libxext6 -y \
    && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
EXPOSE 8000


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]