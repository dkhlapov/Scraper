FROM python:3.7.2-alpine3.8
RUN apk update && apk upgrade && apk add redis && apk add mongo
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "scraper_to_redis.py"]
