# coding=utf-8

from .audioManager import AudioManager
import ui
import addonHandler


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
# Translators: As default playback device
CONSTANT_AS_DEFAULT_PLAYBACK_DEVICE = _("As default playback device")
# Translators: As default recording device
CONSTANT_AS_DEFAULT_RECORDING_DEVICE = _("As default recording device")
# Translators: Default playback device
CONSTANT_DEFAULT_PLAYBACK_DEVICE = _("Default playback device")
# Translators: Default recording device
CONSTANT_DEFAULT_RECORDING_DEVICE = _("Default recording device")

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

	def asDefault(self):
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
		mute = self.audioManager.getPlaybackDeviceMute(self.current)
		message = f"{self.current + 1}:"
		if mute:
			message = f"{message} {_(CONSTANT_MUTED)},"
		message = f"{message} {name}; {_(CONSTANT_VOLUME)}: {volume}"
		default = self.audioManager.GetDefaultPlaybackDevice()
		if self.current == default:
			message = f"{message}; {_(CONSTANT_DEFAULT_PLAYBACK_DEVICE)}"
		ui.message(message)
		self.audioManager.uninitialize()

	# 上一个播放设备
	def previous(self):
		self.audioManager.initialize()
		count = self.audioManager.getPlaybackDeviceCount()
		self.current = (self.current + count - 1) % count
		name = self.audioManager.getPlaybackDeviceName(self.current)
		volume = self.audioManager.getPlaybackDeviceVolume(self.current)
		mute = self.audioManager.getPlaybackDeviceMute(self.current)
		message = f"{self.current + 1}:"
		if mute:
			message = f"{message} {_(CONSTANT_MUTED)},"
		message = f"{message} {name}; {CONSTANT_VOLUME}: {volume}"
		default = self.audioManager.GetDefaultPlaybackDevice()
		if self.current == default:
			message = f"{message}; {_(CONSTANT_DEFAULT_PLAYBACK_DEVICE)}"
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

	def asDefault(self):
		self.audioManager.initialize()
		self.audioManager.SetDefaultPlaybackDevice(self.current)
		self.current = self.audioManager.GetDefaultPlaybackDevice()
		name = self.audioManager.getPlaybackDeviceName(self.current)
		message = f"{name} {_(CONSTANT_AS_DEFAULT_PLAYBACK_DEVICE)}"
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
		mute = self.audioManager.getRecordingDeviceMute(self.current)
		message = f"{self.current + 1}:"
		if mute:
			message = f"{message} {_(CONSTANT_MUTED)},"
		message = f"{message} {name}; {CONSTANT_VOLUME}: {volume}"
		default = self.audioManager.GetDefaultRecordingDevice()
		if self.current == default:
			message = f"{message}; {_(CONSTANT_DEFAULT_RECORDING_DEVICE)}"
		ui.message(message)
		self.audioManager.uninitialize()

	def previous(self):
		self.audioManager.initialize()
		count = self.audioManager.getRecordingDeviceCount()
		self.current = (self.current + count - 1) % count
		name = self.audioManager.getRecordingDeviceName(self.current)
		volume = self.audioManager.getRecordingDeviceVolume(self.current)
		mute = self.audioManager.getRecordingDeviceMute(self.current)
		message = f"{self.current + 1}:"
		if mute:
			message = f"{message} {_(CONSTANT_MUTED)},"
		message = f"{message} {name}; {CONSTANT_VOLUME}: {volume}"
		default = self.audioManager.GetDefaultRecordingDevice()
		if self.current == default:
			message = f"{message}; {_(CONSTANT_DEFAULT_RECORDING_DEVICE)}"
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

	# 静音录音设备
	def mute(self):
		self.audioManager.initialize()
		mute = self.audioManager.getRecordingDeviceMute(self.current)
		self.audioManager.setRecordingDeviceMute(self.current, not mute)
		mute = self.audioManager.getRecordingDeviceMute(self.current)
		state = _(CONSTANT_MUTED) if mute else _(CONSTANT_UNMUTED)
		name = self.audioManager.getRecordingDeviceName(self.current)
		message = f"{state} {name}"
		ui.message(message)
		self.audioManager.uninitialize()

	# 设置默认录音设备
	def asDefault(self):
		self.audioManager.initialize()
		self.audioManager.SetDefaultRecordingDevice(self.current)
		self.current = self.audioManager.GetDefaultRecordingDevice()
		name = self.audioManager.getRecordingDeviceName(self.current)
		message = f"{name} {_(CONSTANT_AS_DEFAULT_RECORDING_DEVICE)}"
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
		mute = self.audioManager.getSessionMute(self.current)
		message = f"{self.current + 1}:"
		if mute:
			message = f"{message} {_(CONSTANT_MUTED)},"
		message = f"{message} {name}; {CONSTANT_VOLUME}: {volume}"
		ui.message(message)
		self.audioManager.uninitialize()

	def previous(self):
		self.audioManager.initialize()
		count = self.audioManager.getSessionCount()
		self.current = (self.current + count - 1) % count
		name = self.audioManager.getSessionName(self.current)
		volume = self.audioManager.getSessionVolume(self.current)
		mute = self.audioManager.getSessionMute(self.current)
		message = f"{self.current + 1}:"
		if mute:
			message = f"{message} {_(CONSTANT_MUTED)},"
		message = f"{message} {name}; {CONSTANT_VOLUME}: {volume}"
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

	# 静音会话
	def mute(self):
		self.audioManager.initialize()
		mute = self.audioManager.getSessionMute(self.current)
		self.audioManager.setSessionMute(self.current, not mute)
		mute = self.audioManager.getSessionMute(self.current)
		state = _(CONSTANT_MUTED) if mute else _(CONSTANT_UNMUTED)
		name = self.audioManager.getSessionName(self.current)
		message = f"{state} {name}"
		ui.message(message)
		self.audioManager.uninitialize()

	# 继承基类，空实现
	def asDefault(self):
		# 什么也不用做
		pass
