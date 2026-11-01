FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY index.js seed.json ./
ENV BIND_HOST=0.0.0.0 PORT=3030
EXPOSE 3030
CMD ["node","index.js"]
