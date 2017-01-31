FROM python:3.5

MAINTAINER David Wyde (david.wyde@gmail.com)

# Install extra software
RUN apt-get update
RUN apt-get install -y socat
RUN pip3 install pyyaml

# Add the user
RUN useradd --create-home challenge

# Copy the app in
COPY yam.py flag wrapper.sh /home/challenge/
RUN chown root:root /home/challenge/yam.py /home/challenge/flag /home/challenge/wrapper.sh
RUN chmod 644 /home/challenge/yam.py /home/challenge/flag
RUN chmod 755 /home/challenge/wrapper.sh

# Switch users
USER challenge

# Set our working directory
WORKDIR /home/challenge

# Run the app
EXPOSE 7777
CMD ["socat", "tcp-l:7777,reuseaddr,fork", "system:'./wrapper.sh',stderr,nofork"]

