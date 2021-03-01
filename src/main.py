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
from threading import Thread
from kivy.config import Config
# Config.set('graphics', 'resizable', False)  # 窗体可变设置为False
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import ListProperty, StringProperty, \
	NumericProperty, BooleanProperty, AliasProperty, ObjectProperty

from kivy.core.window import Window


class CheckoutSubscriber:
	def __init__(self, console_cursor, topic, host, username, passwd, port=1883, qos=0):
		self.client = mqtt.Client()
		if username:
			self.client.username_pw_set(
				username=username, password=passwd)
		self.topic = topic
		self.qos = qos
		self.client.connect(host, port, 60)
		self.client.on_connect = self.on_connect
		self.client.on_disconnect = self.on_disconnect
		self.client.on_message = self.on_message
		self.client.on_subscribe = self.on_subscribe
		self.topic_dic = dict()
		self.console = console_cursor
		self.log_file_save_path = '../log/mq_hunter.log'

	def start_checkout(self):
		self.client.loop_forever()

	def subscribe(self):
		# print("Initiate a subscription request with the topic [{}]".format(self.topic))
		self.console("Initiate a subscription request with the topic [{}]".format(self.topic))
		self.client.subscribe(self.topic, qos=self.qos)

	def on_connect(self, client, userdata, flags, rc):
		# print("Connected with result code " + str(rc))
		self.console("****" * 30)
		self.console(">-----  Connection successful, Code is {} -----<".format(str(rc)))
		self.console(">-----  The location of the log file is [{}] ----<".format(self.log_file_save_path))
		self.subscribe()  # 确保连接成功后再订阅消息

	@staticmethod
	def on_disconnect(client, userdata, rc):
		if rc != 0:
			print("Unexpected disconnection %s" % rc)

	def on_subscribe(self, client, userdata, mid, granted_qos):
		"""当Broker响应了订阅请求时触发此回调"""
		# print("Broker已收到你的订阅请求, qos={}".format(granted_qos))
		self.console("Broker has received your subscription request , QOS={}".format(granted_qos))

	def on_message(self, client, userdata, message):

		"""当代理收到客户订阅主题的消息时将触发此回调"""
		wait_time = 0.00
		if message.topic not in self.topic_dic.keys():
			self.topic_dic[message.topic] = round(time.time(), 2)
		else:
			wait_time = time.time() - self.topic_dic[message.topic]

			# 刷新记录点
			self.topic_dic[message.topic] = round(time.time(), 2)
		# print("收到新消息! => [主题:{}---消息:{}]".format(message.topic,message.payload.decode('utf-8')))
		self.console("==" * 40)
		self.console("received a new message! => [Topic:{}---Messaged:{}]".format(message.topic,
																				  message.payload.decode('utf-8')))
		if wait_time != 0.00:
			# print("主题[{}]距离上次同一主题上报的时间间隔为{:.2f}秒".format(message.topic, wait_time))
			# self.console(
			# 	"Topic:{}--Messaged:{}--The time interval from the last report of the same subject is:{:.2f}seconds.".format(message.topic, message.payload.decode('utf-8'),
			# 													wait_time))
			self.console(">>>>>> Topic:{}--Messaged:{}".format(message.topic, message.payload.decode('utf-8')))
			self.console(">>>>>> The time interval from the last report of the same subject is: {:.2f} seconds.".format(
				wait_time))
			self.console("==" * 40)
		with open(self.log_file_save_path, mode='a', encoding="utf-8") as f:
			f.write('_-------------------------------------------------------------------------_')
			f.write('\r\n')
			f.write("主题:{}--消息:{}--距离上次同一主题上报的时间间隔为:{:.2f}秒".format(message.topic, message.payload.decode('utf-8'),
																	wait_time))
			f.write('\r\n')
			f.write('|-------------------------------------------------------------------------|')
			f.write('\r\n')


class mqHunter(FloatLayout):
	connect_status = BooleanProperty(defaultvalue=False)

	@staticmethod
	def get_version():
		with open('../RELEASE', 'r') as f:
			version = "Beta {}".format(f.read())
		# version = 'Beta 0.12'
		return version if version else "unknown"

	def clear_btn(self):
		self.ids.HOST.text = self.ids.PORT.text = self.ids.TOPIC.text = self.ids.QOS.text = ''
		print("All cleared")

	def _connect_mq(self, host, port, username, passwd, topic, qos):
		try:
			self.cs = CheckoutSubscriber(self.console_cursor, topic, host, username, passwd, port, qos)
			self.connect_status = True
			self.cs.start_checkout()

		except ConnectionRefusedError as crerr:
			self.console_cursor("{}.--- Please check the connection configuration".format(crerr))
		except Exception as e:
			self.console_cursor("{}".format(e))

	def connect_mq_btn(self):
		if self.connect_status:
			self.cs.client.disconnect()
			self.connect_status = False
			self.console_cursor(">----- Connection closed -----<")
			self.console_cursor("****" * 30)
		else:
			if self.ids.HOST.text and self.ids.PORT.text and self.ids.TOPIC.text and self.ids.QOS.text:
				host, port, username, passwd, topic, qos = self.ids.HOST.text, int(
					self.ids.PORT.text), self.ids.U.text, self.ids.P.text, self.ids.TOPIC.text, int(
					self.ids.QOS.text)
				mq_thread = Thread(target=self._connect_mq, args=(host, port, username, passwd, topic, qos,))
				mq_thread.setDaemon(True)
				mq_thread.start()
			else:
				self.console_cursor("---  Please connect the parameters completely")

	def console_cursor(self, text):
		text = text + '\n'
		self.ids.console.text += text


class hunterViewApp(App):
	def build(self):
		Window.size = (800, 550)
		Window.minimum_width, Window.minimum_height = 680, 480
		self.title = 'MQ Hunter - Design by @TerryLi'
		return mqHunter()


if __name__ == '__main__':
	hunterViewApp().run()
