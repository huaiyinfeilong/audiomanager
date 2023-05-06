# coding=utf-8
from .audioManager import AudioManager
import ui


# 音频导航器接口类
class AudioNavigator(object):
	_exceptionMessage = "The method is unsupport called."
	audioManager = AudioManager()

	def next(self):
		raise TypeError(self._exceptionMessage)

	def previous(self):
		raise TypeError(self._exceptionMessage)

	def mute(self):
		raise TypeError(self._exceptionMessage)

	def volumeUp(self):
		raise TypeError(self._exceptionMessage)

	def volumeDown(self):
		raise TypeError(self._exceptionMessage)


# 播放设备导航器类
class PlaybackDeviceNavigator(AudioNavigator):
	current = 0

	def next(self):
		self.audioManager.initialize()
		count = self.audioManager.getPlaybackDeviceCount()
		self.current = (self.current + count + 1) % count
		name = self.audioManager.getPlaybackDeviceName(self.current)
		message = "{}: {}".format((self.current + 1), name)
		ui.message(message)
		self.audioManager.uninitialize()

	def previous(self):
		self.audioManager.initialize()
		count = self.audioManager.getPlaybackDeviceCount()
		self.current = (self.current + count - 1) % count
		name = self.audioManager.getPlaybackDeviceName(self.current)
		message = "{}: {}".format((self.current + 1), name)
		ui.message(message)
		self.audioManager.uninitialize()
