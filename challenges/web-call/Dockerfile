FROM node:10

MAINTAINER David Wyde (david.wyde@gmail.com)

# Install extra software
RUN apt-get update
RUN apt-get install -y socat

# Add the user
RUN useradd --create-home challenge

# Copy the app in
COPY call.js server.js flag wrapper.sh /home/challenge/
RUN chown root:root /home/challenge/call.js /home/challenge/flag /home/challenge/wrapper.sh
RUN chmod 644 /home/challenge/call.js /home/challenge/flag
RUN chmod 755 /home/challenge/wrapper.sh

# Switch users
USER challenge

# Set our working directory
WORKDIR /home/challenge

# Run the app
EXPOSE 8888
CMD ["nodejs", "server.js"]

