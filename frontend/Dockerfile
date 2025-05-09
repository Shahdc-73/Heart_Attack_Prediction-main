FROM nginx:alpine

# Install curl for healthcheck
RUN apk add --no-cache curl

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Set working directory to the default nginx public folder
WORKDIR /usr/share/nginx/html

# Clean default nginx content (optional but good practice)
RUN rm -rf ./*

# Copy all static files from the local static/ directory into nginx
COPY static/ .

# Expose the default port
EXPOSE 80
