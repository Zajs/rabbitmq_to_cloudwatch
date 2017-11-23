FROM python:2.7-alpine

ENV RABBITMQ_HOST=rabbitmq RABBITMQ_PORT=15672 RABBITMQ_USER=guest RABBITMQ_PASSWORD=guest CLOUDWATCH_NAMESPACE=rabbitmq_depth

ADD src/ /app/
ADD requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt && chmod +x /app/publish_queue_size.py

CMD /app/publish_queue_size.py