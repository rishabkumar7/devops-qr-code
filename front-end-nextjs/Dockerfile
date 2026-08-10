FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
RUN npm run bui	ld --if-present

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

RUN addgroup -g 10001 appgroup && \
    adduser -u 10001 -G appgroup -s /bin/sh -D appuser

COPY --chown=10001:10001 package*.json ./
COPY --chown=10001:10001 --from=builder /app/.next ./.next
COPY --chown=10001:10001 --from=builder /app/public ./public
COPY --chown=10001:10001 --from=builder /app/node_modules ./node_modules

EXPOSE 3000
CMD ["npm", "run", "start"]
