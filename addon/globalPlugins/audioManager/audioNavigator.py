# coding=utf-8

# 音频导航器接口类
class AudioNavigator(object):
	_exceptionMessage = "The method is unsupport called."

	def next(self):
		raise TypeError(self._exceptionMessage)

	def previous(self):
		raise TypeError(self._exceptionMessage)

	def mute(self):
		raise TypeError(self._exceptionMessage)

	def volumeUp(self):
		raise TypeError(self._exceptionMessage)

	def volumeDown():
		raise TypeError(self._exceptionMessage)


# 播放设备导航器类
class PlaybackDeviceNavigator(AudioNavigator):
	pass
