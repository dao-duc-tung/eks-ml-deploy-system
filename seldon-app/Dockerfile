FROM python:3.6-slim

# Important
RUN mkdir -p /mnt/model/
RUN chmod -R a+rw /mnt/model/

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

# Port for GRPC
EXPOSE 5000
# Port for REST
EXPOSE 9000

# Define environment variable
ENV MODEL_NAME MLScore
ENV SERVICE_TYPE MODEL

RUN chown -R 8888 /app

CMD exec seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE
