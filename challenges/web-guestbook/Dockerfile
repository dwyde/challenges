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

# Copy the app in
COPY xss.js /home/challenge/
RUN chown root:root /home/challenge/xss.js
RUN chmod 644 /home/challenge/xss.js

# Switch users
USER challenge

# Set our working directory
WORKDIR /home/challenge

ENV NODE_PATH /usr/local/lib/node_modules

# Run the app
CMD while true; do sleep 5; done

