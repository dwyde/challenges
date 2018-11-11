FROM ubuntu

MAINTAINER David Wyde (david.wyde@gmail.com)

# Install extra software
RUN apt-get update
RUN apt-get install nodejs npm -y
RUN npm install -g puppeteer

COPY apt-depends.txt /tmp
RUN cat /tmp/apt-depends.txt | xargs apt install -y
RUN rm /tmp/apt-depends.txt

# Add the user
RUN useradd --create-home challenge

# Set the working directory
WORKDIR /home/challenge

# Copy the app in
COPY server.js xss.js flag ./
RUN chown root:challenge server.js xss.js flag
RUN chmod 640 server.js xss.js flag

# Switch users
USER challenge

ENV NODE_PATH /usr/local/lib/node_modules

# Run the app
CMD nodejs server.js

