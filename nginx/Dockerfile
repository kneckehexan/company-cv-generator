# Use Nginx image
FROM nginx

# Remove the default ngnix.conf
RUN rm /etc/nginx/conf.d/default.conf

# Replace with new ngnix.conf
COPY nginx.conf /etc/nginx/conf.d/
