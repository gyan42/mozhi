# https://vuejs.org/v2/cookbook/dockerize-vuejs-app.html
# https://cli.vuejs.org/guide/deployment.html#docker-nginx
# build stage
FROM node:lts-alpine as build-stage
#FROM node:latest as build-stage
WORKDIR /app
COPY ui/package.json /app/
ENV PATH /app/node_modules/.bin:$PATH
RUN npm install
COPY ui/.env* /app/
COPY ui/src /app/src
ENV NODE_ENV "demo"
RUN npm run build -- --mode $NODE_ENV

# production stage
FROM nginx:stable-alpine as production-stage
#FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY ui/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]