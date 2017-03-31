FROM python:3.5

MAINTAINER David Wyde (david.wyde@gmail.com)

# Install extra software
RUN apt-get update
RUN apt-get install -y nginx net-tools
RUN pip3 install django==1.10.6 pyyaml psycopg2
RUN pip3 install uwsgi

# Add the user
RUN useradd --create-home scoreboard

# Set our working directory
WORKDIR /home/scoreboard

# Copy the app in
COPY . /home/scoreboard/
RUN chown -R scoreboard /home/scoreboard/challenges/migrations

# Deploy the nginx configuration
RUN ln -s /home/scoreboard/challenges_nginx.conf /etc/nginx/sites-enabled

# Switch users
#USER scoreboard

# Run the app as the 'scoreboard' user
CMD service nginx start && su - scoreboard ./run.sh
