# coding=utf-8

from .audioManager import AudioManager
import ui
import addonHandler
import nvwave
import os
import config
from synthDriverHandler import getSynth, setSynth
import tones

def playSoundOut(directionLeft=True):
	wavePath = os.path.dirname(__file__)
	waveFilename = "left.wav" if directionLeft else "right.wav"
	if not waveFilename:
		return
	wavePathFilename = os.path.join(wavePath, "sound", waveFilename)
	nvwave.playWaveFile(wavePathFilename)


addonHandler.initTranslation()


# Translators: Volume field name
CONSTANT_VOLUME = _("Volume")
# Translators: Volume up
CONSTANT_VOLUME_UP = _("Volume up")
# Translators: Volume down
CONSTANT_VOLUME_DOWN = _("Volume down")
# Translators: Maxmium volume
CONSTANT_MAXIMUM_VOLUME = _("Maximum volume")
# Translators: Minimual volume
CONSTANT_MINIMUAL_VOLUME = _("Minimual volume")
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
		if count == 0:
			return
		self.current += 1
		if self.current >= count - 1:
			playSoundOut(False)
			self.current = count - 1
		name = self.audioManager.getPlaybackDeviceName(self.current)
		volume = self.audioManager.getPlaybackDeviceVolume(self.current)
		mute = self.audioManager.getPlaybackDeviceMute(self.current)
		message = ""
		if mute:
			message = f"{_(CONSTANT_MUTED)}, "
		default = self.audioManager.GetDefaultPlaybackDevice()
		if self.current == default:
			message = f"{message}{_(CONSTANT_DEFAULT_PLAYBACK_DEVICE)}, "
		message = f"{message}{name}; {_(CONSTANT_VOLUME)}: {volume}"
		ui.message(message)
		self.audioManager.uninitialize()

	# 上一个播放设备
	def previous(self):
		self.audioManager.initialize()
		count = self.audioManager.getPlaybackDeviceCount()
		if count == 0:
			return
		self.current -= 1
		if self.current <= 0:
			playSoundOut()
			self.current = 0
		name = self.audioManager.getPlaybackDeviceName(self.current)
		volume = self.audioManager.getPlaybackDeviceVolume(self.current)
		mute = self.audioManager.getPlaybackDeviceMute(self.current)
		message = ""
		if mute:
			message = f"{_(CONSTANT_MUTED)}, "
		default = self.audioManager.GetDefaultPlaybackDevice()
		if self.current == default:
			message = f"{message}{_(CONSTANT_DEFAULT_PLAYBACK_DEVICE)}, "
		message = f"{message}{name}; {_(CONSTANT_VOLUME)}: {volume}"
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
		message = f"{volume}"
		if volume == 100:
			message = f"{message} {_(CONSTANT_MAXIMUM_VOLUME)}"
		elif volume == 0:
			message = f"{message} {_(CONSTANT_MINIMUAL_VOLUME)}"
		else:
			message = f"{message} {_(CONSTANT_VOLUME_UP)}"
		message = f"{message} {name}"
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
		message = f"{volume}"
		if volume == 100:
			message = f"{message} {_(CONSTANT_MAXIMUM_VOLUME)}"
		elif volume == 0:
			message = f"{message} {_(CONSTANT_MINIMUAL_VOLUME)}"
		else:
			message = f"{message} {_(CONSTANT_VOLUME_DOWN)}"
		message = f"{message} {name}"
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
		if count == 0:
			return
		self.current += 1
		if self.current >= count - 1:
			playSoundOut(False)
			self.current = count - 1
		name = self.audioManager.getRecordingDeviceName(self.current)
		volume = self.audioManager.getRecordingDeviceVolume(self.current)
		mute = self.audioManager.getRecordingDeviceMute(self.current)
		message = ""
		if mute:
			message = f"{_(CONSTANT_MUTED)}, "
		default = self.audioManager.GetDefaultRecordingDevice()
		if self.current == default:
			message = f"{message}{_(CONSTANT_DEFAULT_RECORDING_DEVICE)}, "
		message = f"{message}{name}; {_(CONSTANT_VOLUME)}: {volume}"
		ui.message(message)
		self.audioManager.uninitialize()

	def previous(self):
		self.audioManager.initialize()
		count = self.audioManager.getRecordingDeviceCount()
		if count == 0:
			return
		self.current -= 1
		if self.current <= 0:
			playSoundOut()
			self.current = 0
		name = self.audioManager.getRecordingDeviceName(self.current)
		volume = self.audioManager.getRecordingDeviceVolume(self.current)
		mute = self.audioManager.getRecordingDeviceMute(self.current)
		message = ""
		if mute:
			message = f"{_(CONSTANT_MUTED)}, "
		default = self.audioManager.GetDefaultRecordingDevice()
		if self.current == default:
			message = f"{message}{_(CONSTANT_DEFAULT_RECORDING_DEVICE)}, "
		message = f"{message}{name}; {_(CONSTANT_VOLUME)}: {volume}"
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
		message = f"{volume}"
		if volume == 100:
			message = f"{message} {_(CONSTANT_MAXIMUM_VOLUME)}"
		elif volume == 0:
			message = f"{message} {_(CONSTANT_MINIMUAL_VOLUME)}"
		else:
			message = f"{message} {_(CONSTANT_VOLUME_UP)}"
		message = f"{message} {name}"
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
		message = f"{volume}"
		if volume == 100:
			message = f"{message} {_(CONSTANT_MAXIMUM_VOLUME)}"
		elif volume == 0:
			message = f"{message} {_(CONSTANT_MINIMUAL_VOLUME)}"
		else:
			message = f"{message} {_(CONSTANT_VOLUME_DOWN)}"
		message = f"{message} {name}"
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
	currentPlaybackDevice = 0
	currentRecordingDevice = 0

	def next(self):
		self.audioManager.initialize()
		count = self.audioManager.getSessionCount()
		if count == 0:
			return
		self.current += 1
		if self.current >= count - 1:
			playSoundOut(False)
			self.current = count - 1
		name = self.audioManager.getSessionName(self.current)
		volume = self.audioManager.getSessionVolume(self.current)
		mute = self.audioManager.getSessionMute(self.current)
		message = ""
		if mute:
			message = f"{_(CONSTANT_MUTED)}, "
		message = f"{message}{name}; {CONSTANT_VOLUME}: {volume}"
		ui.message(message)
		self.audioManager.uninitialize()

	def previous(self):
		self.audioManager.initialize()
		count = self.audioManager.getSessionCount()
		if count == 0:
			return
		self.current -= 1
		if self.current <= 0:
			playSoundOut()
			self.current = 0
		name = self.audioManager.getSessionName(self.current)
		volume = self.audioManager.getSessionVolume(self.current)
		mute = self.audioManager.getSessionMute(self.current)
		message = ""
		if mute:
			message = f"{_(CONSTANT_MUTED)}, "
		message = f"{message}{name}; {CONSTANT_VOLUME}: {volume}"
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
		message = f"{volume}"
		if volume == 100:
			message = f"{message} {_(CONSTANT_MAXIMUM_VOLUME)}"
		elif volume == 0:
			message = f"{message} {_(CONSTANT_MINIMUAL_VOLUME)}"
		else:
			message = f"{message} {_(CONSTANT_VOLUME_UP)}"
		message = f"{message} {name}"
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
		message = f"{volume}"
		if volume == 100:
			message = f"{message} {_(CONSTANT_MAXIMUM_VOLUME)}"
		elif volume == 0:
			message = f"{message} {_(CONSTANT_MINIMUAL_VOLUME)}"
		else:
			message = f"{message} {_(CONSTANT_VOLUME_DOWN)}"
		message = f"{message} {name}"
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

	# 下一个会话播放设备
	def nextPlaybackDevice(self):
		self.audioManager.initialize()
		sessionCount = self.audioManager.getSessionCount()
		# 获取当前会话索引
		self.current = (self.current + sessionCount) % sessionCount
		# 设置会话播放设备
		deviceCount = self.audioManager.getPlaybackDeviceCount()
		self.currentPlaybackDevice = (self.currentPlaybackDevice + deviceCount + 1) % deviceCount
		# 如果会话是NVDA进程则不设置播放设备，因为设置后将导致系统默认播放设备被锁定
		sessionName = self.audioManager.getSessionName(self.current)
		if sessionName != 'NVDA':
			self.audioManager.setSessionPlaybackDevice(self.current, self.currentPlaybackDevice)
		self.currentPlaybackDevice = self.audioManager.GetSessionPlaybackDevice(self.current)
		if self.currentPlaybackDevice > deviceCount or self.currentPlaybackDevice < 0:
			self.currentPlaybackDevice = self.audioManager.GetDefaultPlaybackDevice()
		name = self.audioManager.getPlaybackDeviceName(self.currentPlaybackDevice)
		message = ""
		if self.currentPlaybackDevice == self.audioManager.GetDefaultPlaybackDevice():
			message = f"{_(CONSTANT_DEFAULT_PLAYBACK_DEVICE)}, "
		message = f"{message}{name}"
		ui.message(message)
		self.audioManager.uninitialize()

	# 上一个会话播放设备
	def previousPlaybackDevice(self):
		self.audioManager.initialize()
		sessionCount = self.audioManager.getSessionCount()
		# 获取当前会话索引
		self.current = (self.current + sessionCount) % sessionCount
		# 设置会话播放设备
		deviceCount = self.audioManager.getPlaybackDeviceCount()
		self.currentPlaybackDevice = (self.currentPlaybackDevice + deviceCount - 1) % deviceCount
		# 如果会话是NVDA进程则不设置播放设备，因为设置后将导致系统默认播放设备被锁定
		sessionName = self.audioManager.getSessionName(self.current)
		if sessionName != 'NVDA':
			self.audioManager.setSessionPlaybackDevice(self.current, self.currentPlaybackDevice)
		self.currentPlaybackDevice = self.audioManager.GetSessionPlaybackDevice(self.current)
		if self.currentPlaybackDevice > deviceCount or self.currentPlaybackDevice < 0:
			self.currentPlaybackDevice = self.audioManager.GetDefaultPlaybackDevice()
		name = self.audioManager.getPlaybackDeviceName(self.currentPlaybackDevice)
		message = ""
		if self.currentPlaybackDevice == self.audioManager.GetDefaultPlaybackDevice():
			message = f"{_(CONSTANT_DEFAULT_PLAYBACK_DEVICE)}, "
		message = f"{message}{name}"
		ui.message(message)
		self.audioManager.uninitialize()

	# 下一个会话录音设备
	def nextRecordingDevice(self):
		self.audioManager.initialize()
		sessionCount = self.audioManager.getSessionCount()
		# 获取当前会话索引
		self.current = (self.current + sessionCount) % sessionCount
		# 设置会话播放设备
		deviceCount = self.audioManager.getRecordingDeviceCount()
		self.currentRecordingDevice = (self.currentRecordingDevice + deviceCount + 1) % deviceCount
		# 如果会话是NVDA进程则不设置录音设备，因为设置后将导致系统默认录音设备被锁定
		sessionName = self.audioManager.getSessionName(self.current)
		if sessionName != 'NVDA':
			self.audioManager.setSessionRecordingDevice(self.current, self.currentRecordingDevice)
		self.currentRecordingDevice = self.audioManager.getSessionRecordingDevice(self.current)
		if self.currentRecordingDevice > deviceCount or self.currentRecordingDevice < 0:
			self.currentRecordingDevice = self.audioManager.GetDefaultRecordingDevice()
		name = self.audioManager.getRecordingDeviceName(self.currentRecordingDevice)
		message = ""
		if self.currentRecordingDevice == self.audioManager.GetDefaultRecordingDevice():
			message = f"{_(CONSTANT_DEFAULT_RECORDING_DEVICE)}, "
		message = f"{message}{name}"
		ui.message(message)
		self.audioManager.uninitialize()

	# 上一个会话录音设备
	def previousRecordingDevice(self):
		self.audioManager.initialize()
		sessionCount = self.audioManager.getSessionCount()
		# 获取当前会话索引
		self.current = (self.current + sessionCount) % sessionCount
		# 设置会话播放设备
		deviceCount = self.audioManager.getRecordingDeviceCount()
		self.currentRecordingDevice = (self.currentRecordingDevice + deviceCount - 1) % deviceCount
		# 如果会话是NVDA进程则不设置录音设备，因为设置后将导致系统默认录音设备被锁定
		sessionName = self.audioManager.getSessionName(self.current)
		if sessionName != 'NVDA':
			self.audioManager.setSessionRecordingDevice(self.current, self.currentRecordingDevice)
		self.currentRecordingDevice = self.audioManager.getSessionRecordingDevice(self.current)
		if self.currentRecordingDevice > deviceCount or self.currentRecordingDevice < 0:
			self.currentRecordingDevice = self.audioManager.GetDefaultRecordingDevice()
		name = self.audioManager.getRecordingDeviceName(self.currentRecordingDevice)
		message = ""
		if self.currentRecordingDevice == self.audioManager.GetDefaultRecordingDevice():
			message = f"{_(CONSTANT_DEFAULT_RECORDING_DEVICE)}, "
		message = f"{message}{name}"
		ui.message(message)
		self.audioManager.uninitialize()

	# 重置所有会话设备
	def resetDefault(self):
		self.audioManager.initialize()
		self.audioManager.resetAllSessionDevice()
		self.audioManager.uninitialize()


# NVDA输出设备导航器类
class NVDAOutputDeviceNavigator(object):
	current = 0

	# 获取当前所有可用输出设备
	def _getOutputDevices(self):
		# Note: code mainly taken from NVDA gui/settingsDialogs.py (class SynthesizerSelectionDialog)
		deviceNames = nvwave.getOutputDeviceNames()
		# #11349: On Windows 10 20H1 and 20H2, Microsoft Sound Mapper returns an empty string.
		if deviceNames[0] in ("", "Microsoft Sound Mapper"):
			deviceNames[0] = _("Microsoft Sound Mapper")
		return deviceNames

	# 获取NVDA当前使用的输出设备
	def _getCurrentOutputDevice(self):
		index = 0
		try:
			index = self._getOutputDevices().index(config.conf["speech"]["outputDevice"])
		except Exception:
			pass
		return index

	# 设置输出设备
	def _setOutputDevice(self, device):
		if not device:
			return
		config.conf["speech"]["outputDevice"] = device
		tones.terminate()
		setSynth(getSynth().name)
		tones.initialize()

	# 下一个输出设备
	def next(self):
		devices = self._getOutputDevices()
		count = len(devices)
		current = self._getCurrentOutputDevice()
		current = (current + count + 1) % count
		device = devices[current]
		self._setOutputDevice(device)
		ui.message(device)

	# 上一个输出设备
	def previous(self):
		devices = self._getOutputDevices()
		count = len(devices)
		current = self._getCurrentOutputDevice()
		current = (current + count - 1) % count
		device = devices[current]
		self._setOutputDevice(device)
		ui.message(device)
