FROM ubuntu

MAINTAINER David Wyde (david.wyde@gmail.com)

# Install extra software
RUN apt update
RUN apt install -y python3-pip nginx nginx-extras sudo
RUN pip3 install django==1.11.15 pyyaml psycopg2-binary uwsgi

# Add the user
RUN useradd --create-home scoreboard
RUN usermod -a -G scoreboard www-data

# Set our working directory
WORKDIR /home/scoreboard

# Copy the app in
COPY . /home/scoreboard/
RUN chown -R scoreboard challenges/migrations/

# Allow the scoreboard user to write logs
RUN touch debug.log
RUN chown scoreboard debug.log

# Deploy the nginx configuration
RUN ln -s /home/scoreboard/nginx.conf /etc/nginx/sites-enabled
RUN cp /home/scoreboard/sudoers /etc/sudoers

# Switch users
USER scoreboard

# Run the app as the 'scoreboard' user
CMD sudo /usr/sbin/service nginx start && ./run.sh

