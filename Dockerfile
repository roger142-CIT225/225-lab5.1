FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY style.css /app/static/style.css
EXPOSE 80
CMD ["python", "app.py"]
