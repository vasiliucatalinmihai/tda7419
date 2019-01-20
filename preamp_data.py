from storage import Storage


class PreampData:
    
    def __init__(self, storage):
        self._data = {}
        self._persistance = 'audio_processor'
        self._storage = storage
        self._storage.init(self._persistance)
        self.get_all_data()
        
    def set(self, key, value, save=0):
        self._data[key] = value
        if save:
            self.save_value(key, value)
        return self
    
    def get(self, key=0):
        if key == 0:
            return self._data
        data = self._data[key]
        return data
    
    def save(self):
        self._storage.set_all_data(self._persistance, self._data)
        return self

    def save_value(self, key, value):
        self._storage.set_data(self._persistance, key, value)
        return self

    # * get settings from file
    def get_all_data(self):
        if len(self._data) > 1:
            return self._data

        self._data = self._storage.get_data(self._persistance)

        if len(self._data) < 1:
            self.get_defaults()

        # add missing values from defaults
        defaults = self._get_default_data()
        if len(self._data) < len(defaults):
            defaults.update(self._data)
            self._data = defaults

        return self._data
    
    def save_all(self, driver):
        self.set(driver._keyDataMainSource, driver._DataMainSource)
        self.set(driver._keyDataSecondSource, driver._DataSecondSource)
        self.set(driver._keyDataLoudness, driver._DataLoudness)
        self.set(driver._keyDataSoftMute, driver._DataSoftMute)
        self.set(driver._keyDataTreble, driver._DataTreble)
        self.set(driver._keyDataMiddle, driver._DataMiddle)
        self.set(driver._keyDataBass, driver._DataBass)
        self.set(driver._keyDataSubSetup, driver._DataSubSetup)
        self.set(driver._keyDataMixLevel, driver._DataMixLevel)
        self.set(driver._keyDataDriverSetup, driver._DataDriverSetup)

        self.set(driver._keyMainVolume, driver._MainVolume)
        self.set(driver._keyLFSpeaker, driver._LFSpeaker)
        self.set(driver._keyRFSpeaker, driver._RFSpeaker)
        self.set(driver._keyLRSpeaker, driver._LRSpeaker)
        self.set(driver._keyRRSpeaker, driver._RRSpeaker)
        self.set(driver._keySubVolume, driver._SubVolume)
        self.set(driver._keyMixGain, driver._MixGain)
        
        self.set(driver._keyMainSourceValue, driver._MainSourceValue)
        self.set(driver._keyMainSourceGain, driver._MainSourceGain)
        self.set(driver._keySecondSourceValue, driver._SecondSourceValue)
        self.set(driver._keySecondSourceGain, driver._SecondSourceGain)
        self.set(driver._keySecondSourceRearSource, driver._SecondSourceRearSource)
        self.set(driver._keyLoudnessValue, driver._LoudnessValue)
        self.set(driver._keyLoudnessFreq, driver._LoudnessFreq)
        self.set(driver._keyLoudnessBoost, driver._LoudnessBoost)
        self.set(driver._keyLoudnessSoftStep, driver._LoudnessSoftStep)
        self.set(driver._keySoftMuteValue, driver._SoftMuteValue)
        self.set(driver._keySoftMuteEnable, driver._SoftMuteEnable)
        self.set(driver._keySoftMutePin, driver._SoftMutePin)
        self.set(driver._keySoftMuteTime, driver._SoftMuteTime)
        self.set(driver._keySoftMuteTimeStep, driver._SoftMuteTimeStep)
        self.set(driver._keyTrebleValue, driver._TrebleValue)
        self.set(driver._keyTrebleCenterFreq, driver._TrebleCenterFreq)
        self.set(driver._keyTrebleReferenceOutput, driver._TrebleReferenceOutput)
        self.set(driver._keyMiddleValue, driver._MiddleValue)
        self.set(driver._keyMiddleQFactor, driver._MiddleQFactor)
        self.set(driver._keyMiddleSoftStep, driver._MiddleSoftStep)
        self.set(driver._keyBassValue, driver._BassValue)
        self.set(driver._keyBassQFactor, driver._BassQFactor)
        self.set(driver._keyBassSoftStep, driver._BassSoftStep)
        self.set(driver._keySubSetupCutFreq, driver._SubSetupCutFreq)
        self.set(driver._keySubSetupMiddleFreq, driver._SubSetupMiddleFreq)
        self.set(driver._keySubSetupBassFreq, driver._SubSetupBassFreq)
        self.set(driver._keySubSetupDcMode, driver._SubSetupDcMode)
        self.set(driver._keySubSetupSmooth, driver._SubSetupSmooth)
        self.set(driver._keyMixLevelValue, driver._MixLevelValue)
        self.set(driver._keyMixLevelLFS, driver._MixLevelLFS)
        self.set(driver._keyMixLevelRFS, driver._MixLevelRFS)
        self.set(driver._keyMixLevelEnable, driver._MixLevelEnable)
        self.set(driver._keyMixLevelSubEnable, driver._MixLevelSubEnable)

        self.set(driver._keyGainEffectForDso, driver.GainEffectForDso)
        self.set(driver._keySpectrumQFactor, driver._SpectrumQFactor)
        self.set(driver._keySpectrumSource, driver._SpectrumSource)
        self.set(driver._keySpectrumRun, driver._SpectrumRun)
        self.set(driver._keyChipReset, driver._ChipReset)
        self.set(driver._keyChipResetMode, driver._ChipResetMode)
        self.set(driver._keyChipClockSource, driver._ChipClockSource)
        self.set(driver._keyCouplingMode, driver._CouplingMode)

        self._storage.set_all_data(self._persistance, self._data)
        
    def get_defaults(self):
        self._data = self._get_default_data()
        self._storage.set_all_data(self._persistance, self._data)
        return self

    @staticmethod
    def _get_default_data():
        return dict([
            ("keySoftMuteTimeStep", 0),
            ("keyBassSoftStep", 0),
            ("keyMainSourceValue", 0),
            ("keyMiddleQFactor", 0),
            ("keyTrebleCenterFreq", 0),
            ("keyDataBass", 31),
            ("keyLoudnessFreq", 0),
            ("keyDataMainSource", 72),
            ("keySecondSourceGain", 0),
            ("keyDataSubSetup", 0),
            ("keyLoudnessValue", 0),
            ("keySubSetupCutFreq", 0),
            ("keySoftMuteValue", 1),
            ("keySoftMuteEnable", 1),
            ("keyDataMiddle", 16),
            ("keySecondSourceRearSource", 0),
            ("keyTrebleValue", 0),
            ("keyMixLevelValue", 0),
            ("keyDataMixLevel", 0),
            ("keyLRSpeaker", 90),
            ("keyDataSecondSource", 0),
            ("keySubSetupBassFreq", 0),
            ("keyLFSpeaker", 90),
            ("keyDataSoftMute", 1),
            ("keyMiddleSoftStep", 0),
            ("keyMixLevelLFS", 0),
            ("keySubSetupDcMode", 0),
            ("keySubSetupMiddleFreq", 0),
            ("keySoftMutePin", 0),
            ("keySoftMuteTime", 0),
            ("keyTrebleReferenceOutput", 0),
            ("keyMiddleValue", 0),
            ("keyRFSpeaker", 90),
            ("keyMixGain", 9),
            ("keySecondSourceValue", 0),
            ("keyRRSpeaker", 90),
            ("keyLoudnessSoftStep", 0),
            ("keyLoudnessBoost", 0),
            ("keyMixLevelEnable", 0),
            ("keyDataTreble", 16),
            ("keyDataLoudness", 0),
            ("keyMainVolume", 5),
            ("keyMainSourceGain", 9),
            ("keyBassValue", 15),
            ("keyBassQFactor", 0),
            ("keyMixLevelSubEnable", 0),
            ("keySubVolume", 9),
            ("keySubSetupSmooth", 0),
            ("keyMixLevelRFS", 0),
            ("keyVolumesSoftStep", 0),
            ("keyDataDriverSetup", 0),
            ("keyGainEffectForDso", 0),
            ("keySpectrumQFactor", 0),
            ("keySpectrumSource", 0),
            ("keySpectrumRun", 0),
            ("keyChipReset", 0),
            ("keyChipResetMode", 0),
            ("keyChipClockSource", 0),
            ("keyCouplingMode", 0)
        ])
