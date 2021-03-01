#!/usr/bin/env python
# coding=utf-8

"""
# :author: Terry Li
# :url: https://github.com/WenJieLife
# :copyright: © 2020-present Terry Li
# :motto: I believe that the God rewards the diligent.
"""
import paho.mqtt.client as mqtt
import time
import random


class MockDevice:
	def __init__(self, host, port=1883, qos=0):
		self.client = mqtt.Client()
		self.client.connect(host, port, 60)
		self.qos = qos
		self.topic = "Device-push-topic"

	def start(self):
		self.client.on_publish = self.on_publish_callback
		self.first_push_topic()
		self.mock_device_of_loop_push_msg()

	# self.client.loop_forever()

	@staticmethod
	def on_publish_callback(client, userdata, mid):
		"""当使用publish发送的消息已传输到代理时将触发此回调"""
		print("publish到Broker已完成")

	def first_push_topic(self):
		"""首次推送主题"""
		self.client.publish("Device-push-topic", payload="Created Done!", qos=self.qos)  # 发布"Producer"主题
		print("[{}] Topic is Created!".format(self.topic))

	def mock_device_of_loop_push_msg(self):
		push_times = 1
		while 1:
			rd_time = random.uniform(5.0, 10.0)
			time.sleep(rd_time)
			topic_list = ["Device-push-topic/01", "Device-push-topic/02"]
			rd_topic = random.choice(topic_list)
			print(rd_topic, rd_time)
			self.client.publish(rd_topic, payload="{}".format(push_times), qos=self.qos)
			print("推送信息到Broker-topic:{}]".format(rd_topic))
			push_times += 1


if __name__ == '__main__':
	HOST = "127.0.0.1"
	PORT = 1883
	mq_server = MockDevice(HOST, PORT)
	mq_server.start()
