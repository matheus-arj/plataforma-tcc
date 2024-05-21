FROM node:20

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

CMD ["node", "./src/scripts/run-migrations.js"]

