#
# Dockerfile for SecCon CTF challenges
#
FROM nginx:1

MAINTAINER David Wyde (david.wyde@gmail.com)

# Install packages, then clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy in the app
COPY challenge/* /usr/share/nginx/html/

# Run the app
EXPOSE 80

