FROM node:22-alpine AS frontend
WORKDIR /build
COPY server/frontend/package*.json ./
RUN npm ci
COPY server/frontend/ ./
RUN npm run build
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY server/ ./server/
COPY --from=frontend /build/static/ ./server/frontend/static/
ENV PYTHONUNBUFFERED=1 PORT=8000
EXPOSE 8000
CMD ["sh","-c","python server/manage.py migrate --noinput && python server/manage.py seed_cars && python server/manage.py collectstatic --noinput && cd server && waitress-serve --listen=0.0.0.0:${PORT} dealership.wsgi:application"]
