FROM python:3.6

MAINTAINER David Wyde (david.wyde@gmail.com)

# Install dependencies
RUN pip3 install tornado

# Add the user
RUN useradd -m challenge

# Change directories
WORKDIR /home/challenge

# Copy in the app
COPY challenge.py server.py flag /home/challenge/

# Update permissions
RUN chown root:challenge challenge.py server.py flag
RUN chmod 640 challenge.py server.py flag

# Switch users
USER challenge

# Run the app
EXPOSE 8888
CMD ["python3", "server.py"]

