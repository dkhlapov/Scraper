FROM python:3.7.2-alpine3.8
RUN apk update && apk upgrade
RUN apk add --no-cache mongodb && apk add --no-cache redis-server
COPY . .
RUN pip install -r requirements.txt
EXPOSE 6379
ENTRYPOINT ["python", "redis_to_mongo.py"]
