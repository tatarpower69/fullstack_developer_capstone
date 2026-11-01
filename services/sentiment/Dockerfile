FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir Flask==3.1.3 waitress==3.0.2
COPY app.py ./
EXPOSE 5050
CMD ["waitress-serve","--listen=0.0.0.0:5050","app:app"]
