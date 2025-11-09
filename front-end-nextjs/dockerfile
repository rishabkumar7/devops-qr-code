FROM node:18-alpine AS base

WORKDIR /app

COPY package.json .

RUN npm ci

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]