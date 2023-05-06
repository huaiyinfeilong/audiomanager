# coding=utf-8

from ctypes import windll, wintypes, create_unicode_buffer
import os


class AudioManager(object):
	def __init__(self):
		self._loadLibrary()

	# 夹在DLL
	def _loadLibrary(self):
		dllPath = os.path.join(os.path.dirname(__file__), "LibAudioMgr.dll")
		self.api = windll.LoadLibrary(dllPath)

	# 初始化
	def initialize(self):
		self.api.LAM_Initialize()

	# 逆初始化
	def uninitialize(self):
		self.api.LAM_Uninitialize()

	# 获取播放设备数量
	def getPlaybackDeviceCount(self):
		dwCount = wintypes.DWORD(self.api.LAM_GetPlaybackDeviceCount())
		return dwCount.value

	# 获取播放设备名称
	def getPlaybackDeviceName(self, index):
		dwIndex = wintypes.DWORD(index)
		dwLength = wintypes.DWORD(1024)
		lpszName = create_unicode_buffer(dwLength.value)
		self.api.LAM_GetPlaybackDeviceName(dwIndex, lpszName, dwLength)
		return lpszName.value

	# 获取录音设备数量
	def getRecordingDeviceCount(self):
		dwCount = wintypes.DWORD(self.api.LAM_GetRecordingDeviceCount())
		return dwCount.value

	# 获取录音设备名称
	def getRecordingDeviceName(self, index):
		dwIndex = wintypes.DWORD(index)
		dwLength = wintypes.DWORD(1024)
		lpszName = create_unicode_buffer(dwLength.value)
		self.api.LAM_GetRecordingDeviceName(dwIndex, lpszName, dwLength)
		return lpszName.value

# 获取会话数量
	def getSessionCount(self):
		dwCount = wintypes.DWORD(self.api.LAM_GetSessionCount())
		return dwCount.value

	# 获取会话名称
	def getSessionName(self, index):
		dwIndex = wintypes.DWORD(index)
		dwLength = wintypes.DWORD(1024)
		lpszName = create_unicode_buffer(dwLength.value)
		self.api.LAM_GetSessionName(dwIndex, lpszName, dwLength)
		return lpszName.value
