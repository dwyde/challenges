FROM python:3.5

MAINTAINER David Wyde (david.wyde@gmail.com)

# Install extra software
RUN apt-get update
RUN apt-get install -y nginx net-tools sudo
RUN pip3 install django==1.11.15 pyyaml psycopg2-binary
RUN pip3 install uwsgi

# Add the user
RUN useradd --create-home scoreboard
RUN usermod -a -G scoreboard www-data

# Set our working directory
WORKDIR /home/scoreboard

# Copy the app in
COPY . /home/scoreboard/
RUN chown -R scoreboard /home/scoreboard/challenges/migrations

# Deploy the nginx configuration
RUN ln -s /home/scoreboard/challenges_nginx.conf /etc/nginx/sites-enabled
RUN cp /home/scoreboard/sudoers /etc/sudoers

# Switch users
USER scoreboard

# Run the app as the 'scoreboard' user
CMD sudo /usr/sbin/service nginx start && ./run.sh

