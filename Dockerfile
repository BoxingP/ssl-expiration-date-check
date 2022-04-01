FROM python:3.8-slim
RUN apt-get update && apt-get install -y --no-install-recommends cron tzdata lsb-release build-essential
RUN apt-get update && apt-get install -y --no-install-recommends python3-dev python3-virtualenv
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev
WORKDIR /usr/src/ssl_expiry_check
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m pip install virtualenv
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./*.py ./
COPY ./*.json ./
COPY ./crontab ./crontab
RUN mv ./crontab /etc/cron.d/cron-jobs && sed -i -e 's/\r/\n/g' /etc/cron.d/cron-jobs && chmod 0644 /etc/cron.d/cron-jobs
COPY ./cron.sh cron.sh
RUN chmod +x cron.sh
RUN mkdir -p /var/log/cron && touch /var/log/cron/cron.log
ENV TZ="Asia/Shanghai"
ENTRYPOINT ["/bin/sh", "/usr/src/ssl_expiry_check/cron.sh"]