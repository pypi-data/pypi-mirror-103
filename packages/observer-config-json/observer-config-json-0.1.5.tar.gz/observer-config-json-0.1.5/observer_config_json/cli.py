from facade_edit_file_json import FACADE_EDIT_FILE_JSON
from threading import Thread
import time as timelib

class OBSERVER_CONFIG_JSON():
	def __init__(self,file_name,**kwargs):
		self._config_default={}
		self._consumer_conf={}
		for key, value in kwargs.items():
			if value != '':
				self._config_default[key] = value
				self._consumer_conf[key]={}
				print(key)
		self.conf = FACADE_EDIT_FILE_JSON(file_name)
		if self.conf.read(out=True)!=[]:
			self._consumer_conf =  self.conf.json_value
		print(self._consumer_conf)
		thread = Thread(target=self._update, args=())  # создаем поток
		thread.start()

	def _update(self):
		self._consumer_conf_str = str(self._consumer_conf)
		while True:
			if self._consumer_conf_str != str(self._consumer_conf):
				self.conf.new(self._consumer_conf)
			timelib.sleep(60)


	def set(self,_consumer_id,**kwargs):
		for key,value in kwargs.items():
			if key not in self._consumer_conf:
				self._consumer_conf[key] = {}
			if value != '':
				self._consumer_conf[key][str(_consumer_id)]=value

	def set_default(self,**kwargs):
		for key,value in kwargs.items():
			self._config_default[key]=value

	def get_default(self,key):
			if key not in self._config_default:
				self._config_default[key] = ''
			return self._config_default[key]

	def get(self,_consumer_id,key):
		print(self._consumer_conf)
		if key not in  self._consumer_conf:
			self._consumer_conf[key]={}
		print(self._consumer_conf)
		if str(_consumer_id) not in self._consumer_conf[key]:
			self._consumer_conf[key][str(_consumer_id)]=self.get_default(key)
		return self._consumer_conf[key][str(_consumer_id)]
