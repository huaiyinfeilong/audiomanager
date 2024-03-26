# coding=utf-8

from ctypes import WinDLL, wintypes, create_unicode_buffer
import os
from logHandler import log
import addonHandler
import api


addonHandler.initTranslation()

# Translators: System volume
CONSTANT_SYSTEM_SOUND = _("System sound")

class AudioManager(object):
	def __init__(self):
		self._loadLibrary()

	# 夹在DLL
	def _loadLibrary(self):
		path = os.environ.get('PATH')
		currentPath = os.path.dirname(__file__)
		# 添加当前目录到path环境变量
		if currentPath not in path.split(os.pathsep):
			os.environ['PATH'] = os.pathsep.join([path, currentPath])
		dllPath = os.path.join(currentPath, "LibAudioMgr.dll")
		self.api = WinDLL(dllPath)
		# 初始化
		self.LAM_Initialize = self.api.LAM_Initialize
		# 逆初始化
		self.LAM_Uninitialize = self.api.LAM_Uninitialize
		# 获取播放设备数量
		self.LAM_GetPlaybackDeviceCount = self.api.LAM_GetPlaybackDeviceCount
		self.LAM_GetPlaybackDeviceCount.restype = wintypes.DWORD
		# 获取播放设备名称
		self.LAM_GetPlaybackDeviceName = self.api.LAM_GetPlaybackDeviceName
		self.LAM_GetPlaybackDeviceName.argtypes = (wintypes.DWORD, wintypes.LPWSTR, wintypes.DWORD)
		self.LAM_GetPlaybackDeviceName.restype = wintypes.DWORD
		# 获取播放设备音量
		self.LAM_GetPlaybackDeviceVolume = self.api.LAM_GetPlaybackDeviceVolume
		self.LAM_GetPlaybackDeviceVolume.argtypes = (wintypes.DWORD,)
		self.LAM_GetPlaybackDeviceVolume.restype = wintypes.DWORD
		# 设置播放设备音量
		self.LAM_SetPlaybackDeviceVolume = self.api.LAM_SetPlaybackDeviceVolume
		self.LAM_SetPlaybackDeviceVolume .argtypes = (wintypes.DWORD, wintypes.DWORD)
		# 设置播放设备静音
		self.LAM_SetPlaybackDeviceMute = self.api.LAM_SetPlaybackDeviceMute
		self.LAM_SetPlaybackDeviceMute.argtypes = (wintypes.DWORD, wintypes.BOOL)
		# 获取播放设备静音状态
		self.LAM_GetPlaybackDeviceMute = self.api.LAM_GetPlaybackDeviceMute
		self.LAM_GetPlaybackDeviceMute.args = (wintypes.DWORD,)
		self.LAM_GetPlaybackDeviceMute.restype = wintypes.BOOL
		# 设置默认播放设备
		self.LAM_SetDefaultPlaybackDevice = self.api.LAM_SetDefaultPlaybackDevice
		self.LAM_SetDefaultPlaybackDevice.argtypes = (wintypes.DWORD,)
		# 获取默认播放设备
		self.LAM_GetDefaultPlaybackDevice = self.api.LAM_GetDefaultPlaybackDevice
		self.LAM_GetDefaultPlaybackDevice.restype = wintypes.DWORD
		# 获取录音设备数量
		self.LAM_GetRecordingDeviceCount = self.api.LAM_GetRecordingDeviceCount
		self.LAM_GetRecordingDeviceCount.restype = wintypes.DWORD
		# 获取录音设备名称
		self.LAM_GetRecordingDeviceName = self.api.LAM_GetRecordingDeviceName
		self.LAM_GetRecordingDeviceName.argtypes = (wintypes.DWORD, wintypes.LPWSTR, wintypes.DWORD)
		self.LAM_GetRecordingDeviceName.restype = wintypes.DWORD
		# 获取录音设备音量
		self.LAM_GetRecordingDeviceVolume = self.api.LAM_GetRecordingDeviceVolume
		self.LAM_GetRecordingDeviceVolume.argtypes = (wintypes.DWORD,)
		self.LAM_GetRecordingDeviceVolume.restype = wintypes.DWORD
		# 设置录音设备音量
		self.LAM_SetRecordingDeviceVolume = self.api.LAM_SetRecordingDeviceVolume
		self.LAM_SetRecordingDeviceVolume .argtypes = (wintypes.DWORD, wintypes.DWORD)
		# 设置录音设备静音
		self.LAM_SetRecordingDeviceMute = self.api.LAM_SetRecordingDeviceMute
		self.LAM_SetRecordingDeviceMute.argtypes = (wintypes.DWORD, wintypes.BOOL)
		# 获取录音设备静音状态
		self.LAM_GetRecordingDeviceMute = self.api.LAM_GetRecordingDeviceMute
		self.LAM_GetRecordingDeviceMute.args = (wintypes.DWORD,)
		self.LAM_GetRecordingDeviceMute.restype = wintypes.BOOL
		# 设置默认录音设备
		self.LAM_SetDefaultRecordingDevice = self.api.LAM_SetDefaultRecordingDevice
		self.LAM_SetDefaultRecordingDevice.argtypes = (wintypes.DWORD,)
		# 获取默认录音设备
		self.LAM_GetDefaultRecordingDevice = self.api.LAM_GetDefaultRecordingDevice
		self.LAM_GetDefaultRecordingDevice.restype = wintypes.DWORD
		# 获取会话数量
		self.LAM_GetSessionCount = self.api.LAM_GetSessionCount
		self.LAM_GetSessionCount.restype = wintypes.DWORD
		# 获取会话名称
		self.LAM_GetSessionName = self.api.LAM_GetSessionName
		self.LAM_GetSessionName.argtypes = (wintypes.DWORD, wintypes.LPWSTR, wintypes.DWORD)
		self.LAM_GetSessionName.restype = wintypes.DWORD
		# 获取会话音量
		self.LAM_GetSessionVolume = self.api.LAM_GetSessionVolume
		self.LAM_GetSessionVolume.argtypes = (wintypes.DWORD,)
		self.LAM_GetSessionVolume.restype = wintypes.DWORD
		# 设置会话音量
		self.LAM_SetSessionVolume = self.api.LAM_SetSessionVolume
		self.LAM_SetSessionVolume .argtypes = (wintypes.DWORD, wintypes.DWORD)
		# 设置会话静音
		self.LAM_SetSessionMute = self.api.LAM_SetSessionMute
		self.LAM_SetSessionMute.argtypes = (wintypes.DWORD, wintypes.BOOL)
		# 获取会话静音状态
		self.LAM_GetSessionMute = self.api.LAM_GetSessionMute
		self.LAM_GetSessionMute.args = (wintypes.DWORD,)
		self.LAM_GetSessionMute.restype = wintypes.BOOL
		# 获取会话播放设备
		self.LAM_GetSessionPlaybackDevice = self.api.LAM_GetSessionPlaybackDevice
		self.LAM_GetSessionPlaybackDevice.argstype = (wintypes.DWORD,)
		self.LAM_GetSessionPlaybackDevice.restype = wintypes.DWORD
		# 设置会话播放设备
		self.LAM_SetSessionPlaybackDevice = self.api.LAM_SetSessionPlaybackDevice
		self.LAM_SetSessionPlaybackDevice.argstype = (wintypes.DWORD, wintypes.DWORD)
		# 设置会话录音设备
		self.LAM_SetSessionRecordingDevice = self.api.LAM_SetSessionRecordingDevice
		self.LAM_SetSessionRecordingDevice.argtypes = (wintypes.DWORD, wintypes.DWORD)
		# 获取会话录音设备
		self.LAM_GetSessionRecordingDevice = self.api.LAM_GetSessionRecordingDevice
		self.LAM_GetSessionRecordingDevice.argtypes = (wintypes.DWORD,)
		self.LAM_GetSessionRecordingDevice.restype = wintypes.DWORD
		# 重置所有会话设备
		self.LAM_ResetAllSessionDevice = self.api.LAM_ResetAllSessionDevice
		# 设置窗口静音
		self.LAM_SetWindowMute = self.api.LAM_SetWindowMute
		self.LAM_SetWindowMute.argstype = (wintypes.HWND, wintypes.BOOL)
		# 获取窗口静音状态
		self.LAM_GetWindowMute = self.api.LAM_GetWindowMute
		self.LAM_GetWindowMute.argtypes = (wintypes.HWND,)
		self.LAM_GetWindowMute.restype = wintypes.BOOL

	# 初始化
	def initialize(self):
		self.LAM_Initialize()

	# 逆初始化
	def uninitialize(self):
		self.LAM_Uninitialize()

	# 获取播放设备数量
	def getPlaybackDeviceCount(self):
		dwCount = wintypes.DWORD(self.LAM_GetPlaybackDeviceCount())
		return dwCount.value

	# 获取播放设备名称
	def getPlaybackDeviceName(self, index):
		dwIndex = wintypes.DWORD(index)
		dwLength = wintypes.DWORD(1024)
		lpszName = create_unicode_buffer(dwLength.value)
		self.LAM_GetPlaybackDeviceName(dwIndex, lpszName, dwLength)
		return lpszName.value

	# 获取播放设备音量
	def getPlaybackDeviceVolume(self, index):
		dwIndex = wintypes.DWORD(index)
		dwVolume = wintypes.DWORD(self.LAM_GetPlaybackDeviceVolume(dwIndex))
		return dwVolume.value

	# 设置播放设备音量
	def setPlaybackDeviceVolume(self, index, volume):
		dwIndex = wintypes.DWORD(index)
		dwVolume = wintypes.DWORD(volume)
		self.LAM_SetPlaybackDeviceVolume(dwIndex, dwVolume)

	# 设置播放设备静音状态
	def setPlaybackDeviceMute(self, index, mute):
		dwIndex = wintypes.DWORD(index)
		bMute = wintypes.BOOL(mute)
		self.LAM_SetPlaybackDeviceMute(dwIndex, bMute)

	# 获取播放设备静音状态
	def getPlaybackDeviceMute(self, index):
		dwIndex = wintypes.DWORD(index)
		mute = self.LAM_GetPlaybackDeviceMute(dwIndex)
		return wintypes.BOOL(mute)

	# 设置默认播放设备
	def SetDefaultPlaybackDevice(self, index):
		dwIndex = wintypes.DWORD(index)
		self.LAM_SetDefaultPlaybackDevice(dwIndex)

	# 获取默认播放设备
	def GetDefaultPlaybackDevice(self):
		return wintypes.DWORD(self.LAM_GetDefaultPlaybackDevice()).value

	# 获取录音设备数量		
	def getRecordingDeviceCount(self):
		dwCount = wintypes.DWORD(self.LAM_GetRecordingDeviceCount())
		return dwCount.value

	# 获取录音设备名称
	def getRecordingDeviceName(self, index):
		dwIndex = wintypes.DWORD(index)
		dwLength = wintypes.DWORD(1024)
		lpszName = create_unicode_buffer(dwLength.value)
		self.LAM_GetRecordingDeviceName(dwIndex, lpszName, dwLength)
		return lpszName.value

	# 获取录音设备音量
	def getRecordingDeviceVolume(self, index):
		dwIndex = wintypes.DWORD(index)
		dwVolume = wintypes.DWORD(self.LAM_GetRecordingDeviceVolume(dwIndex))
		return dwVolume.value

	# 设置录音设备音量
	def setRecordingDeviceVolume(self, index, volume):
		dwIndex = wintypes.DWORD(index)
		dwVolume = wintypes.DWORD(volume)
		self.LAM_SetRecordingDeviceVolume(dwIndex, dwVolume)

	# 设置录音设备静音状态
	def setRecordingDeviceMute(self, index, mute):
		dwIndex = wintypes.DWORD(index)
		bMute = wintypes.BOOL(mute)
		self.LAM_SetRecordingDeviceMute(dwIndex, bMute)

	# 获取录音设备静音状态
	def getRecordingDeviceMute(self, index):
		dwIndex = wintypes.DWORD(index)
		mute = self.LAM_GetRecordingDeviceMute(dwIndex)
		return wintypes.BOOL(mute)

	# 设置默认录音设备
	def SetDefaultRecordingDevice(self, index):
		dwIndex = wintypes.DWORD(index)
		self.LAM_SetDefaultRecordingDevice(dwIndex)

	# 获取默认录音设备
	def GetDefaultRecordingDevice(self):
		return wintypes.DWORD(self.LAM_GetDefaultRecordingDevice()).value

	# 获取会话数量
	def getSessionCount(self):
		dwCount = wintypes.DWORD(self.LAM_GetSessionCount())
		return dwCount.value

	# 获取会话名称
	def getSessionName(self, index):
		dwIndex = wintypes.DWORD(index)
		dwLength = wintypes.DWORD(1024)
		lpszName = create_unicode_buffer(dwLength.value)
		self.LAM_GetSessionName(dwIndex, lpszName, dwLength)
		if lpszName.value == "系统声音":
			return _(CONSTANT_SYSTEM_SOUND)
		return lpszName.value

	# 获取会话音量
	def getSessionVolume(self, index):
		dwIndex = wintypes.DWORD(index)
		dwVolume = wintypes.DWORD(self.LAM_GetSessionVolume(dwIndex))
		return dwVolume.value

	# 设置会话音量
	def setSessionVolume(self, index, volume):
		dwIndex = wintypes.DWORD(index)
		dwVolume = wintypes.DWORD(volume)
		self.LAM_SetSessionVolume(dwIndex, dwVolume)

	# 设置会话静音状态
	def setSessionMute(self, index, mute):
		dwIndex = wintypes.DWORD(index)
		bMute = wintypes.BOOL(mute)
		self.LAM_SetSessionMute(dwIndex, bMute)

	# 获取会话静音状态
	def getSessionMute(self, index):
		dwIndex = wintypes.DWORD(index)
		mute = self.LAM_GetSessionMute(dwIndex)
		return wintypes.BOOL(mute)

	# 获取会话播放设备
	def GetSessionPlaybackDevice(self, index):
		dwIndex = wintypes.DWORD(index)
		return wintypes.DWORD(self.LAM_GetSessionPlaybackDevice(dwIndex)).value

	# 设置会话播放设备
	def setSessionPlaybackDevice(self, sessionIndex, deviceIndex):
		dwSessionIndex = wintypes.DWORD(sessionIndex)
		dwDeviceIndex = wintypes.DWORD(deviceIndex)
		self.LAM_SetSessionPlaybackDevice(dwSessionIndex, dwDeviceIndex)

	# 设置会话录音设备
	def setSessionRecordingDevice(self, sessionIndex, deviceIndex):
		dwSessionIndex = wintypes.DWORD(sessionIndex)
		dwDeviceIndex = wintypes.DWORD(deviceIndex)
		self.LAM_SetSessionRecordingDevice(dwSessionIndex, dwDeviceIndex)

	# 获取会话录音设备
	def getSessionRecordingDevice(self, index):
		dwIndex = wintypes.DWORD(index)
		return wintypes.DWORD(self.LAM_GetSessionRecordingDevice(dwIndex)).value

	# 重置所有会话设备
	def resetAllSessionDevice(self):
		self.LAM_ResetAllSessionDevice()

	# 设置窗口静音
	def setWindowMute(self, mute):
		hWnd = wintypes.HWND(api.getNavigatorObject().windowHandle)
		self.LAM_SetWindowMute(hWnd, wintypes.BOOL(mute))

	# 获取窗口静音状态：
	def getWindowMute(self):
		return wintypes.BOOL(self.LAM_GetWindowMute(wintypes.HWND(api.getNavigatorObject().windowHandle))).value
