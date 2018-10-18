FROM python:3.5

MAINTAINER David Wyde (david.wyde@gmail.com)

# Add the user
RUN useradd -m challenge

# Copy in the app
COPY challenge.py server.py flag /home/challenge/
RUN chown root:root /home/challenge/*.py /home/challenge/flag
RUN chmod 644 /home/challenge/*.py /home/challenge/flag

# Switch users
USER challenge
WORKDIR /home/challenge

# Run the app
EXPOSE 8888
CMD ["python3", "server.py"]

