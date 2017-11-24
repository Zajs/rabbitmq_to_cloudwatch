#!/usr/bin/env python
from __future__ import with_statement, print_function

from pyrabbit.api import Client
from boto.ec2.cloudwatch import CloudWatchConnection
import os
from time import sleep


def get_queue_depths(host, username, password, vhost):
    cl = Client(host, username, password)
    if not cl.is_alive():
        raise Exception("Failed to connect to rabbitmq")
    depths = {}
    queues = [q['name'] for q in cl.get_queues(vhost=vhost)]
    for queue in queues:
        if queue == "aliveness-test":
            continue
        depths[queue] = cl.get_queue_depth(vhost, queue)
    return depths


def publish_queue_depth_to_cloudwatch(cwc, queue_name, depth, namespace):
    cwc.put_metric_data(namespace=namespace,
                        name=queue_name,
                        unit="Count",
                        value=depth)


def publish_depths_to_cloudwatch(depths, namespace):
    cwc = CloudWatchConnection()
    for queue in depths:
        publish_queue_depth_to_cloudwatch(cwc, queue, depths[queue], namespace)


def get_queue_depths_and_publish_to_cloudwatch(host, username, password, vhost, namespace):
    depths = get_queue_depths(host, username, password, vhost)
    publish_depths_to_cloudwatch(depths, namespace)


if __name__ == "__main__":
    host = os.environ.get("RABBITMQ_HOST")
    port = os.environ.get("RABBITMQ_PORT")
    user = os.environ.get("RABBITMQ_USER")
    password = os.environ.get("RABBITMQ_PASSWORD")
    namespace = os.environ.get("CLOUDWATCH_NAMESPACE")
    print("Starting host=%s:%s user=%s namespace=%s" % (host, port, user, namespace))
    while True:
        try:
            get_queue_depths_and_publish_to_cloudwatch(
                host + ":" + port,
                user,
                password,
                "/",
                namespace)
        except Exception as ex:
            print(ex)
        sleep(60)

#from https://github.com/trailbehind/AWS-Utilities/blob/master/rabbitmq-to-cloudwatch.py