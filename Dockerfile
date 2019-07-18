# front build
FROM node:12.4.0-alpine AS front-build

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY front/package.json /app/package.json
RUN npm i --silent
COPY /front /app
RUN npm run build

# prod env
FROM nginx:1.17.1-alpine
COPY --from=front-build /app/build/ /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
