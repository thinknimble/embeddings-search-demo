FROM node:16-alpine

WORKDIR /app/client

COPY ./client/.npmrc /app/client/.npmrc
COPY ./client/package.json /app/client/package.json
RUN npm i

CMD ["npm", "run", "serve"]
