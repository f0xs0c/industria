FROM nginx:1.27-alpine

# Copie des assets
COPY index.html /usr/share/nginx/html/index.html
COPY dashboard.js /usr/share/nginx/html/dashboard.js

# Conf Nginx avec reverse proxy /api -> api_service
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Sécurité (nginx user par défaut)
EXPOSE 80
HEALTHCHECK CMD wget -qO- http://localhost/ || exit 1
