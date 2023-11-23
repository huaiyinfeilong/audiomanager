# coding=utf-8

import addonHandler
import gui
import wx
import winVersion


addonHandler.initTranslation()


# 获取冲突的插件
def getIncompatibleAddons(names):
	addons = []
	for addon in addonHandler.getAvailableAddons():
		if addon.name in names:
			addons.append(addon)
	return addons


# Determine if the system version is higher than Win 10
def isSupportedSystem():
	return winVersion.getWinVer() >= winVersion.WIN10


def onInstall():
	def showUnsupportedDialog():
		# Translators: The system you are using is not supported. This add-on needs to be running on a Windows 10 or higher system.
		gui.messageBox(_("The system you are using is not supported. This add-on needs to be running on a Windows 10 or higher system."), _("Warning"))
		raise Exception("Unsupported system.")
	# 检查系统版本是否为或高于Win 10，若不满足条件则退出安装
	if not isSupportedSystem():
		wx.CallAfter(showUnsupportedDialog)
	# 获取已安装的不兼容的插件列表
	names = ["AudioControl"]
	addons = getIncompatibleAddons(names)
	def showQuestionDialog():
		result = gui.messageBox(
			# Translators: The message
			_("We have detected a conflict between the 'AudioControl' add-on you have installed and the add-on you are currently installing. Click 'Yes' to automatically uninstall and install the conflicting add-on or click' No 'to install without uninstalling."),
			# Translators: The title
			_("Warning"),
			wx.YES_NO | wx.YES_DEFAULT)
		if result == wx.YES:
			for addon in addons:
				addon.requestRemove()
	if addons != []:
		wx.CallAfter(showQuestionDialog)
