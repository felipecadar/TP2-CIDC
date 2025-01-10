FROM nginx:alpine
RUN mkdir -p /app/logs
COPY . /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]