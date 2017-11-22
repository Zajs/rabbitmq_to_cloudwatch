FROM python:2.7-alpine
ADD src/ /app/
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt && chmod +x /app/publish_queue_size.py
CMD /app/publish_queue_size.py