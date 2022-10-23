FROM python:3.8-slim

RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

COPY ./ /kart
COPY requirements.txt ./
RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /kart

# RUN ["chmod", "777", "run.sh"]

# CMD [ "python", "run.py" ]
CMD [ "gunicorn", "run:app", "--workers=1", "--bind=0.0.0.0:5000", "--timeout=10", "--worker-class=gevent", "--log-level=debug"]
# gunicorn run:app -w 1 -b 0.0.0.0:5000 --timeout=10 -k gevent --log-level=debug