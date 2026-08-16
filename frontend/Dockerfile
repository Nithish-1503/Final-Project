# Frontend: static files served by nginx (also proxies /api to backend)
FROM nginx:1.27-alpine

# Remove default config and add ours
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static site
COPY index.html style.css app.js /usr/share/nginx/html/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

