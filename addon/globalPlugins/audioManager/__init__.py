# coding=utf-8

import globalPluginHandler
import addonHandler
import scriptHandler
from .audioManager import AudioManager
from .audioNavigator import PlaybackDeviceNavigator, RecordingDeviceNavigator, SessionNavigator


addonHandler.initTranslation()

# Translators: Category name
CATEGORY_NAME = _("Audio Manager")


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# 插件初始化
	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		self.audioNavigator = None
		self.playbackDeviceNavigator = PlaybackDeviceNavigator()
		self.recordingDeviceNavigator = RecordingDeviceNavigator()
		self.sessionNavigator = SessionNavigator()

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
		self.recordingDeviceNavigator.next()
		self.audioNavigator = self.recordingDeviceNavigator

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Previous Recording device
		description=_("Previous Recording device"),
		gesture="kb:CONTROL+WINDOWS+ALT+NUMPAD1"
	)
	def script_PrevrecordingDevice(self, gesture):
		self.recordingDeviceNavigator.previous()
		self.audioNavigator = self.recordingDeviceNavigator

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Next Sessioning device
		description=_("Next Session"),
		gesture="kb:CONTROL+WINDOWS+ALT+NUMPAD9"
	)
	def script_nextSession(self, gesture):
		self.sessionNavigator.next()
		self.audioNavigator = self.sessionNavigator

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Previous Sessioning device
		description=_("Previous Session"),
		gesture="kb:CONTROL+WINDOWS+ALT+NUMPAD7"
	)
	def script_PrevsessioningDevice(self, gesture):
		self.sessionNavigator.previous()
		self.audioNavigator = self.sessionNavigator

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Volume up
		description=_("Volume up"),
		gesture="kb:CONTROL+WINDOWS+ALT+NUMPAD8"
	)
	def script_volumeUp(self, gesture):
		self.audioNavigator.volumeUp()

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Volume down
		description=_("Volume down"),
		gesture="kb:CONTROL+WINDOWS+ALT+NUMPAD2"
	)
	def script_volumeDown(self, gesture):
		self.audioNavigator.volumeDown()

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Mute or unmute the device
		description=_("Mute or unmute the device"),
		gesture="kb:CONTROL+WINDOWS+ALT+NUMPAD5"
	)
	def script_mute(self, gesture):
		self.audioNavigator.mute()

	@scriptHandler.script(
		category=CATEGORY_NAME,
		# Translators: Set to as default device
		description=_("Set to as default device"),
		gesture="kb:CONTROL+WINDOWS+ALT+NUMPADENTER"
	)
	def script_asDefault(self, gesture):
		self.audioNavigator.asDefault()
