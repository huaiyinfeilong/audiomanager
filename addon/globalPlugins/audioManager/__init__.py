# coding=utf-8

import globalPluginHandler
import addonHandler
import scriptHandler
from .audioManager import AudioManager
from .audioNavigator import PlaybackDeviceNavigator, RecordingDeviceNavigator, SessionNavigator, NVDAOutputDeviceNavigator
import ui
import wx
import config


addonHandler.initTranslation()

# Translators: Category name
CATEGORY_NAME = _("Audio Manager")


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# 插件初始化
	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		confspec = {
			"lockMicrophoneVolume": "boolean(default=False)",
			"microphoneVolume": "integer(default=50)"
		}
		config.conf.spec["audioManager"] = confspec
		self.audioNavigator = None
		self.playbackDeviceNavigator = PlaybackDeviceNavigator()
		self.recordingDeviceNavigator = RecordingDeviceNavigator()
		self.sessionNavigator = SessionNavigator()
		self.microphoneVolume = 0
		self.lockMicrophoneVolume = config.conf["audioManager"]["lockMicrophoneVolume"]
		# 如果配置中开启了麦克风音量锁定，则加载保存的上次的麦克风音量
		self.microphoneVolume = config.conf["audioManager"]["microphoneVolume"] if self.lockMicrophoneVolume else 0
		self.timer = wx.Timer()
		self.timer.Bind(wx.EVT_TIMER, self.onTimer)
		self.timer.Start(100)
		self.nvdaOutputDeviceNavigator = NVDAOutputDeviceNavigator()

	# 插件退出执行代码
	def terminate(self):
		# 如果开启了麦克风锁定，退出时保存麦克风音量，用以下次启动时作为麦克风默认音量
		if self.lockMicrophoneVolume:
			config.conf["audioManager"]["microphoneVolume"] = self.microphoneVolume

	# Reset the playback device and the recording device of all applications
	def _resetAllSessionDevice(self):
		manager = AudioManager()
		manager.initialize()
		manager.resetAllSessionDevice()
		manager.uninitialize()
		# Translators: Reset the playback and recording device of all audio applications
		ui.message(_("Reset the playback and recording device of all audio applications"))

# Reset the playback volume of all audio applications and unmute them
	def _resetAllSessionVolume(self):
		manager = AudioManager()
		manager.initialize()
		sessionCount = manager.getSessionCount()
		for i in range(sessionCount):
			manager.setSessionVolume(i, 100)
			manager.setSessionMute(i, False)
		manager.uninitialize()
		# Translators: Reset the playback volume of all audio applications and unmute them
		ui.message(_("Reset the playback volume of all audio applications and unmute them"))

	# 定时器，用以锁定麦克风音量
	def onTimer(self, event):
		if not self.lockMicrophoneVolume:
			return
		manager = AudioManager()
		manager.initialize()
		currentRecordingDevice = manager.GetDefaultRecordingDevice()
		manager.setRecordingDeviceVolume(currentRecordingDevice, self.microphoneVolume)
		manager.uninitialize()

	# 获取麦克风音量
	def getMicrophoneVolume(self):
		manager = AudioManager()
		manager.initialize()
		currentRecordingDevice = manager.GetDefaultRecordingDevice()
		volume = manager.getRecordingDeviceVolume(currentRecordingDevice)
		manager.uninitialize()
		return volume

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Next playback device
		description=_("Next playback device"),
		gestures=["kb(desktop):control+windows+alt+numpad6", "kb(laptop):control+windows+alt+pagedown"]
	)
	def script_nextPlaybackDevice(self, gesture):
		self.playbackDeviceNavigator.next()
		self.audioNavigator = self.playbackDeviceNavigator

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Previous playback device
		description=_("Previous playback device"),
		gestures=["kb(desktop):control+windows+alt+numpad4", "kb(laptop):control+windows+alt+pageup"]
	)
	def script_PrevPlaybackDevice(self, gesture):
		self.playbackDeviceNavigator.previous()
		self.audioNavigator = self.playbackDeviceNavigator

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Next Recording device
		description=_("Next Recording device"),
		gestures=["kb(desktop):control+windows+alt+numpad3", "kb(laptop):control+windows+alt+end"]
	)
	def script_nextrecordingDevice(self, gesture):
		self.recordingDeviceNavigator.next()
		self.audioNavigator = self.recordingDeviceNavigator

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Previous Recording device
		description=_("Previous Recording device"),
		gestures=["kb(desktop):control+windows+alt+numpad1","kb(laptop):control+windows+alt+home"]
	)
	def script_PrevrecordingDevice(self, gesture):
		self.recordingDeviceNavigator.previous()
		self.audioNavigator = self.recordingDeviceNavigator

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Next audio application
		description=_("Next audio application"),
		gestures=["kb(desktop):control+windows+alt+numpad9", "kb(laptop):control+windows+alt+rightarrow"]
	)
	def script_nextSession(self, gesture):
		self.sessionNavigator.next()
		self.audioNavigator = self.sessionNavigator

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Previous audio application
		description=_("Previous audio application"),
		gestures=["kb(desktop):control+windows+alt+numpad7", "kb(laptop):control+windows+alt+leftarrow"]
	)
	def script_previousSession(self, gesture):
		self.sessionNavigator.previous()
		self.audioNavigator = self.sessionNavigator

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Volume up
		description=_("Volume up"),
		gestures=["kb(desktop):control+windows+alt+numpad8", "kb(laptop):control+windows+alt+uparrow"]
	)
	def script_volumeUp(self, gesture):
		if self.audioNavigator is None:
			# Translators: Please select a device or audio application first
			ui.message(_("Please select a device or audio application first"))
			return
		self.audioNavigator.volumeUp()
		if isinstance(self.audioNavigator, RecordingDeviceNavigator):
			self.microphoneVolume = self.getMicrophoneVolume()
			if self.lockMicrophoneVolume is True:
				config.conf["audioManager"]["microphoneVolume"] = self.microphoneVolume

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Volume down
		description=_("Volume down"),
		gestures=["kb(desktop):control+windows+alt+numpad2", "kb(laptop):control+windows+alt+downarrow"]
	)
	def script_volumeDown(self, gesture):
		if self.audioNavigator is None:
			# Translators: Please select a device or audio application first
			ui.message(_("Please select a device or audio application first"))
			return
		self.audioNavigator.volumeDown()
		if isinstance(self.audioNavigator, RecordingDeviceNavigator):
			self.microphoneVolume = self.getMicrophoneVolume()
			if self.lockMicrophoneVolume is True:
				config.conf["audioManager"]["microphoneVolume"] = self.microphoneVolume

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Mute or unmute the playback or the recording devices
		description=_("Mute or unmute the playback or the recording devices"),
		gestures=["kb(desktop):control+windows+alt+numpad5", "kb(laptop):control+windows+alt+space"]
	)
	def script_mute(self, gesture):
		if self.audioNavigator is not None:
			self.audioNavigator.mute()
		else:
			# Translators: Please select a device or audio application first
			ui.message(_("Please select a device or audio application first"))

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Set to as default playback or recording device
		description=_("Set to as default playback or recording device"),
		gestures=["kb(desktop):control+windows+alt+numpadenter", "kb(laptop):control+windows+alt+enter"]
	)
	def script_asDefault(self, gesture):
		if isinstance(self.audioNavigator, PlaybackDeviceNavigator) or isinstance(self.audioNavigator, RecordingDeviceNavigator):
			self.audioNavigator.asDefault()
		else:
			# Translators: Please select a playback or recording device first
			ui.message(_("Please select a playback or recording device first"))

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Next the playback device of the audio application
		description=_("Next the playback device of the audio application"),
		gestures=["kb(desktop):control+windows+alt+numpadmultiply", "kb(laptop):control+windows+alt+]"]
	)
	def script_nextPlaybackDeviceOfApplication(self, gesture):
		if isinstance(self.audioNavigator, SessionNavigator):
			self.audioNavigator.nextPlaybackDevice()
		else:
			# Translators: Please select an audio application first
			ui.message(_("Please select an audio application first"))	

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Previous the playback device of the audio application
		description=_("Previous the playback device of the audio application"),
		gestures=["kb(desktop):shift+control+windows+alt+numpadmultiply", "kb(laptop):shift+control+windows+alt+]"]
	)
	def script_previousPlaybackDeviceOfApplication(self, gesture):
		if isinstance(self.audioNavigator, SessionNavigator):
			self.audioNavigator.previousPlaybackDevice()
		else:
			# Translators: Please select an audio application first
			ui.message(_("Please select an audio application first"))	

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Previous the recording device of the audio application
		description=_("Previous the recording device of the audio application"),
		gestures=["kb(desktop):shift+control+windows+alt+numpaddivide", "kb(laptop):shift+control+windows+alt+["]
	)
	def script_previousRecordingDeviceOfApplication(self, gesture):
		if isinstance(self.audioNavigator, SessionNavigator):
			self.audioNavigator.previousRecordingDevice()
		else:
			# Translators: Please select an audio application first
			ui.message(_("Please select an audio application first"))	

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Next the recording device of the audio application
		description=_("Next the recording device of the audio application"),
		gestures=["kb(desktop):control+windows+alt+numpaddivide", "kb(laptop):control+windows+alt+["]
	)
	def script_nextRecordingDeviceOfApplication(self, gesture):
		if isinstance(self.audioNavigator, SessionNavigator):
			self.audioNavigator.nextRecordingDevice()
		else:
			# Translators: Please select an audio application first
			ui.message(_("Please select an audio application first"))	

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Click to reset the playback and recording devices of all audio applications; Double click to reset the volume of all audio applications and unmute them
		description=_("Click to reset the playback and recording devices of all audio applications; Double click to reset the volume of all audio applications and unmute them"),
		gestures=["kb(desktop):control+windows+alt+numpadminus", "kb(laptop):control+windows+alt+backspace"]
	)
	def script_resetDefault(self, gesture):
		repeatCount = scriptHandler.getLastScriptRepeatCount()
		if repeatCount == 0:
			self._resetAllSessionDevice()
		elif repeatCount == 1:
			self._resetAllSessionVolume()

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Microphone switch
		description=_("Microphone switch"),
		gestures=["kb(desktop):shift+control+windows+alt+numpad2" ,"kb(laptop):shift+control+windows+alt+downarrow"]
	)
	def script_microphoneSwitch(self, gesture):
		manager = AudioManager()
		manager.initialize()
		currentRecordingDevice = manager.GetDefaultRecordingDevice()
		muteStatus = manager.getRecordingDeviceMute(currentRecordingDevice)
		muteStatus = not muteStatus
		manager.setRecordingDeviceMute(currentRecordingDevice, muteStatus)
		muteStatus = manager.getRecordingDeviceMute(currentRecordingDevice)
		# Translators: The microphone turned off and turned on
		message = _("The microphone turned off") if muteStatus else _("The microphone turned on")
		ui.message(message)
		manager.uninitialize()

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Soundswitch
		description=_("Sound switch"),
		gestures=["kb(desktop):shift+control+windows+alt+numpad5", "kb(laptop):shift+control+windows+alt+uparrow"]
	)
	def script_soundSwitch(self, gesture):
		manager = AudioManager()
		manager.initialize()
		currentPlaybackDevice = manager.GetDefaultPlaybackDevice()
		muteStatus = manager.getPlaybackDeviceMute(currentPlaybackDevice)
		muteStatus = not muteStatus
		manager.setPlaybackDeviceMute(currentPlaybackDevice, muteStatus)
		muteStatus = manager.getPlaybackDeviceMute(currentPlaybackDevice)
		# Translators: The sound turned off and turned on
		message = _("The sound turned off") if muteStatus else _("The sound turned on")
		ui.message(message)
		manager.uninitialize()

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Mute or unmute the current window application
		description=_("Mute or unmute the current window application"),
		gestures=["kb(desktop):shift+control+windows+alt+numpad8", "kb(laptop):shift+control+windows+alt+space"]
	)
	def script_muteWindow(self, gesture):
		manager = AudioManager()
		manager.initialize()
		mute = manager.getWindowMute()
		mute = not mute
		manager.setWindowMute(mute)
		mute = manager.getWindowMute()
		# Translators: The current window is muted or unmuted
		message = _("The current window is muted") if mute else _("The current window is unmuted.")
		ui.message(message)
		manager.uninitialize()

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Lock microphone volume
		description=_("Lock microphone volume"),
		gestures=["kb(desktop):control+windows+alt+numpaddelete", "kb(laptop):control+windows+alt+delete"]
	)
	def script_lockMicrophoneVolume(self, gesture):
		# 获取当前麦克风音量
		self.microphoneVolume = self.getMicrophoneVolume()
		self.lockMicrophoneVolume = not self.lockMicrophoneVolume
		if self.lockMicrophoneVolume is True:
			config.conf["audioManager"]["microphoneVolume"] = self.microphoneVolume
		# translators: Locked or unlocked the microphone volume
		message = _("Locked the microphone volume") if self.lockMicrophoneVolume \
		else _("Unlocked the microphone volume")
		config.conf["audioManager"]["lockMicrophoneVolume"] = self.lockMicrophoneVolume
		ui.message(message)

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Next NVDA playback device
		description=_("Next NVDA playback device"),
		gestures=["kb(desktop):control+windows+alt+numpadplus", "kb(laptop):control+windows+alt+\\"]
	)
	def script_nextNVDAOutputDevice(self, gesture):
		self.nvdaOutputDeviceNavigator.next()

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Previous NVDA playback device
		description=_("Previous NVDA playback device"),
		gestures=["kb(desktop):shift+control+windows+alt+numpadplus", "kb(laptop):shift+control+windows+alt+\\"]
	)
	def script_previousNVDAOutputDevice(self, gesture):
		self.nvdaOutputDeviceNavigator.previous()
