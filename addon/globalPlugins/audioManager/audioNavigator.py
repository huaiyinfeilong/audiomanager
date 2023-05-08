# coding=utf-8

from .audioManager import AudioManager
import ui
import addonHandler
from logHandler import log


addonHandler.initTranslation()

# Translators: Volume field name
CONSTANT_VOLUME = _("Volume")
# Translators: Volume up
CONSTANT_VOLUME_UP = _("Volume up")
# Translators: Volume down
CONSTANT_VOLUME_DOWN = _("Volume down")
# Translators: Muted
CONSTANT_MUTED = _("Muted")
# Translators: Unmuted
CONSTANT_UNMUTED = _("Unmuted")


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

	# 下一个播放设备
	def next(self):
		self.audioManager.initialize()
		count = self.audioManager.getPlaybackDeviceCount()
		self.current = (self.current + count + 1) % count
		name = self.audioManager.getPlaybackDeviceName(self.current)
		volume = self.audioManager.getPlaybackDeviceVolume(self.current)
		message = f"{self.current + 1}: {name}; {_(CONSTANT_VOLUME)}: {volume}"
		ui.message(message)
		self.audioManager.uninitialize()

	# 上一个播放设备
	def previous(self):
		self.audioManager.initialize()
		count = self.audioManager.getPlaybackDeviceCount()
		self.current = (self.current + count - 1) % count
		name = self.audioManager.getPlaybackDeviceName(self.current)
		volume = self.audioManager.getPlaybackDeviceVolume(self.current)
		message = "{}: {}; {}: {}".format((self.current + 1), name, _(CONSTANT_VOLUME), volume)
		ui.message(message)
		self.audioManager.uninitialize()

	# 增加播放设备音量
	def volumeUp(self):
		self.audioManager.initialize()
		volume = self.audioManager.getPlaybackDeviceVolume(self.current)
		volume += 1
		volume = 100 if volume > 100 else volume
		name = self.audioManager.getPlaybackDeviceName(self.current)
		self.audioManager.setPlaybackDeviceVolume(self.current, volume)
		message = f"{volume} {name}"
		ui.message(message)
		self.audioManager.uninitialize()

	# 减少播放设备音量
	def volumeDown(self):
		self.audioManager.initialize()
		volume = self.audioManager.getPlaybackDeviceVolume(self.current)
		volume -= 1
		volume = 0 if volume < 0 else volume
		name = self.audioManager.getPlaybackDeviceName(self.current)
		self.audioManager.setPlaybackDeviceVolume(self.current, volume)
		message = f"{volume} {name}"
		ui.message(message)
		self.audioManager.uninitialize()

	# 静音播放设备
	def mute(self):
		self.audioManager.initialize()
		mute = self.audioManager.getPlaybackDeviceMute(self.current)
		self.audioManager.setPlaybackDeviceMute(self.current, not mute)
		mute = self.audioManager.getPlaybackDeviceMute(self.current)
		state = _(CONSTANT_MUTED) if mute else _(CONSTANT_UNMUTED)
		name = self.audioManager.getPlaybackDeviceName(self.current)
		message = f"{state} {name}"
		ui.message(message)
		self.audioManager.uninitialize()


# 录音设备导航器类
class RecordingDeviceNavigator(AudioNavigator):
	current = 0

	def next(self):
		self.audioManager.initialize()
		count = self.audioManager.getRecordingDeviceCount()
		self.current = (self.current + count + 1) % count
		name = self.audioManager.getRecordingDeviceName(self.current)
		volume = self.audioManager.getRecordingDeviceVolume(self.current)
		message = "{}: {}; {}: {}".format((self.current + 1), name, _(CONSTANT_VOLUME), volume)
		ui.message(message)
		self.audioManager.uninitialize()

	def previous(self):
		self.audioManager.initialize()
		count = self.audioManager.getRecordingDeviceCount()
		self.current = (self.current + count - 1) % count
		name = self.audioManager.getRecordingDeviceName(self.current)
		volume = self.audioManager.getRecordingDeviceVolume(self.current)
		message = "{}: {}; {}: {}".format((self.current + 1), name, _(CONSTANT_VOLUME), volume)
		ui.message(message)
		self.audioManager.uninitialize()

	# 增加录音设备音量
	def volumeUp(self):
		self.audioManager.initialize()
		volume = self.audioManager.getRecordingDeviceVolume(self.current)
		volume += 1
		volume = 100 if volume > 100 else volume
		name = self.audioManager.getRecordingDeviceName(self.current)
		self.audioManager.setRecordingDeviceVolume(self.current, volume)
		message = f"{volume} {name}"
		ui.message(message)
		self.audioManager.uninitialize()

	# 减少录音设备音量
	def volumeDown(self):
		self.audioManager.initialize()
		volume = self.audioManager.getRecordingDeviceVolume(self.current)
		volume -= 1
		volume = 0 if volume < 0 else volume
		name = self.audioManager.getRecordingDeviceName(self.current)
		self.audioManager.setRecordingDeviceVolume(self.current, volume)
		message = f"{volume} {name}"
		ui.message(message)
		self.audioManager.uninitialize()


# 会话导航器类
class SessionNavigator(AudioNavigator):
	current = 0

	def next(self):
		self.audioManager.initialize()
		count = self.audioManager.getSessionCount()
		self.current = (self.current + count + 1) % count
		name = self.audioManager.getSessionName(self.current)
		volume = self.audioManager.getSessionVolume(self.current)
		message = f"{self.current + 1}: {name}; {_(CONSTANT_VOLUME)}: {volume}"
		ui.message(message)
		self.audioManager.uninitialize()

	def previous(self):
		self.audioManager.initialize()
		count = self.audioManager.getSessionCount()
		self.current = (self.current + count - 1) % count
		name = self.audioManager.getSessionName(self.current)
		volume = self.audioManager.getSessionVolume(self.current)
		message = f"{self.current + 1}: {name}; {_(CONSTANT_VOLUME)}: {volume}"
		ui.message(message)
		self.audioManager.uninitialize()

	# 增加会话音量
	def volumeUp(self):
		self.audioManager.initialize()
		volume = self.audioManager.getSessionVolume(self.current)
		volume += 1
		volume = 100 if volume > 100 else volume
		name = self.audioManager.getSessionName(self.current)
		self.audioManager.setSessionVolume(self.current, volume)
		message = f"{volume} {name}"
		ui.message(message)
		self.audioManager.uninitialize()

	# 减少会话音量
	def volumeDown(self):
		self.audioManager.initialize()
		volume = self.audioManager.getSessionVolume(self.current)
		volume -= 1
		volume = 0 if volume < 0 else volume
		name = self.audioManager.getSessionName(self.current)
		self.audioManager.setSessionVolume(self.current, volume)
		message = f"{volume} {name}"
		ui.message(message)
		self.audioManager.uninitialize()
