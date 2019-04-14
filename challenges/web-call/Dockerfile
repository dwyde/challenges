FROM node

MAINTAINER David Wyde (david.wyde@gmail.com)

# Install extra software
RUN apt-get update
RUN apt-get install -y socat

# Add the user
RUN useradd --create-home challenge

# Set our working directory
WORKDIR /home/challenge

# Copy the app in
COPY call.js server.js flag wrapper.sh /home/challenge/
RUN chown root:challenge call.js flag wrapper.sh
RUN chmod 640 call.js flag
RUN chmod 750 wrapper.sh

# Switch users
USER challenge

# Run the app
EXPOSE 8888
CMD ["nodejs", "server.js"]

