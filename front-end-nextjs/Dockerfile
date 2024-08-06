FROM node:18-alpine as base

WORKDIR /app

COPY package.json yarn.lock* package-lock.json* pnpm-lock.json* ./
RUN \
    if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
    elif [ -f package-lock.json ]; then npm ci; \
    elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
    else echo "Lockfile not found." && exit 1; \
    fi
COPY . .

RUN npm run build 

EXPOSE 3000 

USER root
CMD ["npm", "start"]