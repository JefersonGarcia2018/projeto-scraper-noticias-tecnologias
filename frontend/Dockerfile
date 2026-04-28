FROM node:22-alpine

WORKDIR /app

COPY . .

RUN npm install

COPY . .

EXPOSE 9000

CMD ["npx", "quasar", "dev"]
