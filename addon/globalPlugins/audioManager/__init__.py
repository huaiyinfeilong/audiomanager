# coding=utf-8

import globalPluginHandler
import addonHandler
import scriptHandler
import ui
from .audioManager import AudioManager
from .audioNavigator import PlaybackDeviceNavigator


addonHandler.initTranslation()

# Translators: Category name
CATEGORY_NAME = _("Audio Manager")


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# 插件初始化
	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		self.audioNavigator = None
		self.playbackDeviceNavigator = PlaybackDeviceNavigator()
		self.audioManager = AudioManager()
		self.audioManager.initialize()
		self.currentPlaybackDeviceIndex = 0
		self.playbackDeviceCount = self.audioManager.getPlaybackDeviceCount()
		self.currentrecordingDeviceIndex = 0
		self.recordingDeviceCount = self.audioManager.getRecordingDeviceCount()
		self.currentSessionIndex = 0
		self.sessionCount = self.audioManager.getSessionCount()

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Next playback device
		description=_("Next playback device"),
		gesture="kb:CONTROL+WINDOWS+ALT+NUMPAD6"
	)
	def script_nextPlaybackDevice(self, gesture):
		self.playbackDeviceNavigator.next()
		self.audioNavigator = self.playbackDeviceNavigator

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Previous playback device
		description=_("Previous playback device"),
		gesture="kb:CONTROL+WINDOWS+ALT+NUMPAD4"
	)
	def script_PrevPlaybackDevice(self, gesture):
		self.playbackDeviceNavigator.previous()
		self.audioNavigator = self.playbackDeviceNavigator

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Next Recording device
		description=_("Next Recording device"),
		gesture="kb:CONTROL+WINDOWS+ALT+NUMPAD3"
	)
	def script_nextrecordingDevice(self, gesture):
		self.audioManager.initialize()
		self.currentrecordingDeviceIndex = (self.currentrecordingDeviceIndex + self.recordingDeviceCount + 1) \
		% self.recordingDeviceCount
		name = self.audioManager.getRecordingDeviceName(self.currentrecordingDeviceIndex)
		name = "{}: {}".format(self.currentrecordingDeviceIndex + 1, name)
		ui.message(name)

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Previous Recording device
		description=_("Previous Recording device"),
		gesture="kb:CONTROL+WINDOWS+ALT+NUMPAD1"
	)
	def script_PrevrecordingDevice(self, gesture):
		self.audioManager.initialize()
		self.currentrecordingDeviceIndex = (self.currentrecordingDeviceIndex + self.recordingDeviceCount - 1) \
		% self.recordingDeviceCount
		name = self.audioManager.getRecordingDeviceName(self.currentrecordingDeviceIndex)
		name = "{}: {}".format(self.currentrecordingDeviceIndex + 1, name)
		ui.message(name)

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Next Sessioning device
		description=_("Next Session"),
		gesture="kb:CONTROL+WINDOWS+ALT+NUMPAD9"
	)
	def script_nextSession(self, gesture):
		self.audioManager.initialize()
		self.currentSessionIndex = (self.currentSessionIndex + self.sessionCount + 1) \
		% self.sessionCount
		name = self.audioManager.getSessionName(self.currentSessionIndex)
		name = "{}: {}".format(self.currentSessionIndex + 1, name)
		ui.message(name)

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Previous Sessioning device
		description=_("Previous Session"),
		gesture="kb:CONTROL+WINDOWS+ALT+NUMPAD7"
	)
	def script_PrevsessioningDevice(self, gesture):
		self.audioManager.initialize()
		self.currentSessionIndex = (self.currentSessionIndex + self.sessionCount - 1) \
		% self.sessionCount
		name = self.audioManager.getSessionName(self.currentSessionIndex)
		name = "{}: {}".format(self.currentSessionIndex + 1, name)
		ui.message(name)
