# build environment
FROM node:12.4.0-alpine AS build

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json /app/package.json
RUN npm i --silent
RUN npm i react-scripts@3.0.1 -g --silent
COPY . /app
RUN npm run build

# prod env
FROM ngnix:1.16.0-alpine
COPY --from=build /app/build /ush/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
