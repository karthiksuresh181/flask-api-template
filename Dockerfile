FROM python:3.10

EXPOSE 5000

COPY . /src
WORKDIR /src

RUN pip3 install -r requirements.txt

COPY . .

RUN printf '#!/bin/sh\n exit 0' > /usr/sbin/policy-rc.d
RUN apt update && apt install -y cron
RUN crontab -l | { echo "* */1 * * * cd /src/api && /usr/local/bin/flask clear-cache"; } | crontab -

CMD ["/bin/bash", "-c", "service cron start;python api/wsgi.py"]
