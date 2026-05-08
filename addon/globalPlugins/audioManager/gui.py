# coding=utf-8

import addonHandler
import config
import gui
from gui import nvdaControls
from gui.settingsDialogs import SettingsPanel
import wx

addonHandler.initTranslation()

class AudioManagerSettingsPanel(SettingsPanel):
    # Translators: Title of the settings panel
    title = _("Audio Manager")

    def makeSettings(self, settingsSizer):
        sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

        # Translators: Label for volume step spin control
        self.volumeStepSpin = sHelper.addLabeledControl(
            _("Volume change step (&%):"),
            nvdaControls.SelectOnFocusSpinCtrl,
            min=1, max=20, initial=config.conf["audioManager"]["volumeStep"]
        )
        self.volumeStepSpin.SetToolTip(_("Determines how many percent volume changes when pressing volume up/down. Range 1-20."))

    def onSave(self):
        config.conf["audioManager"]["volumeStep"] = self.volumeStepSpin.GetValue()