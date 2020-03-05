############################
# Build container
############################
FROM node:10-alpine AS dep

WORKDIR /starter
ENV NODE_ENV production

COPY package.json package-lock.json /starter/

RUN npm install --production

COPY . /starter

############################
# Final container
############################
FROM node:10-alpine

WORKDIR /starter

COPY --from=dep /starter .

CMD ["npm","start"]

EXPOSE 8080
