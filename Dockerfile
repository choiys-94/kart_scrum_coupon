FROM python:3.8-slim

RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

COPY ./ /kart
COPY requirements.txt ./
RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /kart
RUN ["chmod", "+x", "run.sh"]

CMD [ "./run.sh" ]