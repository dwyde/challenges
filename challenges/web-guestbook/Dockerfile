# Use the Python 2 image
FROM ubuntu:latest

MAINTAINER David Wyde (david.wyde@gmail.com)

# Install extra software
RUN apt-get update
RUN apt-get install -y phantomjs

# Add the user
RUN useradd --create-home challenge

# Copy the app in
COPY xss.js /home/challenge/
RUN chown root:root /home/challenge/xss.js
RUN chmod 644 /home/challenge/xss.js

# Switch users
USER challenge

# Set our working directory
WORKDIR /home/challenge

ENV QT_QPA_PLATFORM offscreen

# Run the app
CMD ["phantomjs", "xss.js"]
