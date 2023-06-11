# coding=utf-8

import addonHandler
import gui
import wx


addonHandler.initTranslation()


# 获取冲突的插件
def getIncompatibleAddons(names):
	addons = []
	for addon in addonHandler.getAvailableAddons():
		if addon.name in names:
			addons.append(addon)
	return addons


def onInstall():
	# 获取已安装的不兼容的插件列表
	names = ["AudioControl"]
	addons = getIncompatibleAddons(names)
	def showQuestionDialog():
		result = gui.messageBox(
			# Translators: The message
			_("We have detected a conflict between the 'AudioControl' plugin you have installed and the plugin you are currently installing. Click 'Yes' to automatically uninstall and install the conflicting plugin, or click' No 'to install without uninstalling."),
			# Translators: The title
			_("Warning"),
			wx.YES_NO | wx.YES_DEFAULT)
		if result == wx.YES:
			for addon in addons:
				addon.requestRemove()
	if addons != []:
		wx.CallAfter(showQuestionDialog)
