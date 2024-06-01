# Use an appropriate base image, e.g., python:3.10-slim
FROM python:3.10-slim

# Set environment variables (e.g., set Python to run in unbuffered mode)
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "data_app.py"]
