import smbus as bus
from preamp_data import PreampData


class Preamp:
    i2cBus = bus.SMBus(1)
    _driverAddr = 0x44

    _addr_main_source = 0  # 0b01000000 #
    _addr_loudness = 65  # 0b01000001 #
    _addr_soft_mute = 66  # 0b01000010 #
    _addr_main_volume = 67  # 0b01000011 #
    _addr_treble = 68  # 0b01000100 #
    _addr_middle = 69  # 0b01000101 #
    _addr_bass = 70  # 0b01000110 #
    _addr_subwoofer_setup = 72  # 0b01001000 #
    _addr_second_source = 71  # 0b01000111 #
    _addr_mix_gain = 73  # 0b01001001 #
    _addr_l_f_speaker = 74  # 0b01001010 #
    _addr_r_f_speaker = 75  # 0b01001011 #
    _addr_l_r_speaker = 76  # 0b01001100 #
    _addr_r_r_speaker = 77  # 0b01001101 #
    _addr_mix_level = 78  # 0b01001110 #
    _addr_subwoofer_volume = 79  # 0b01001111 #
    _addr_driver_setup = 80  # 0b01010000 #

    # settings keys for config
    # main data keys
    _keyDataMainSource = 'keyDataMainSource'
    _keyDataSecondSource = 'keyDataSecondSource'
    _keyDataLoudness = 'keyDataLoudness'
    _keyDataSoftMute = 'keyDataSoftMute'
    _keyDataTreble = 'keyDataTreble'
    _keyDataMiddle = 'keyDataMiddle'
    _keyDataBass = 'keyDataBass'
    _keyDataSubSetup = 'keyDataSubSetup'
    _keyDataMixLevel = 'keyDataMixLevel'
    _keyMainVolume = 'keyMainVolume'
    _keyLFSpeaker = 'keyLFSpeaker'
    _keyRFSpeaker = 'keyRFSpeaker'
    _keyLRSpeaker = 'keyLRSpeaker'
    _keyRRSpeaker = 'keyRRSpeaker'
    _keySubVolume = 'keySubVolume'
    _keyMixGain = 'keyMixGain'
    _keyDataDriverSetup = 'keyDataDriverSetup'

    _keyVolumesSoftStep = 'keyVolumesSoftStep'

    # value keys
    _keyMainSourceValue = 'keyMainSourceValue'
    _keyMainSourceGain = 'keyMainSourceGain'
    _keySecondSourceValue = 'keySecondSourceValue'
    _keySecondSourceGain = 'keySecondSourceGain'
    _keySecondSourceRearSource = 'keySecondSourceRearSource'
    _keyLoudnessValue = 'keyLoudnessValue'
    _keyLoudnessFreq = 'keyLoudnessFreq'
    _keyLoudnessBoost = 'keyLoudnessBoost'
    _keyLoudnessSoftStep = 'keyLoudnessSoftStep'
    _keySoftMuteValue = 'keySoftMuteValue'
    _keySoftMuteEnable = 'keySoftMuteEnable'
    _keySoftMutePin = 'keySoftMutePin'
    _keySoftMuteTime = 'keySoftMuteTime'
    _keySoftMuteTimeStep = 'keySoftMuteTimeStep'
    _keyTrebleValue = 'keyTrebleValue'
    _keyTrebleCenterFreq = 'keyTrebleCenterFreq'
    _keyTrebleReferenceOutput = 'keyTrebleReferenceOutput'
    _keyMiddleValue = 'keyMiddleValue'
    _keyMiddleQFactor = 'keyMiddleQFactor'
    _keyMiddleSoftStep = 'keyMiddleSoftStep'
    _keyBassValue = 'keyBassValue'
    _keyBassQFactor = 'keyBassQFactor'
    _keyBassSoftStep = 'keyBassSoftStep'
    _keySubSetupCutFreq = 'keySubSetupCutFreq'
    _keySubSetupMiddleFreq = 'keySubSetupMiddleFreq'
    _keySubSetupBassFreq = 'keySubSetupBassFreq'
    _keySubSetupDcMode = 'keySubSetupDcMode'
    _keySubSetupSmooth = 'keySubSetupSmooth'
    _keyMixLevelValue = 'keyMixLevelValue'
    _keyMixLevelLFS = 'keyMixLevelLFS'
    _keyMixLevelRFS = 'keyMixLevelRFS'
    _keyMixLevelEnable = 'keyMixLevelEnable'
    _keyMixLevelSubEnable = 'keyMixLevelSubEnable'
    _keyGainEffectForDso = 'keyGainEffectForDso'
    _keySpectrumQFactor = 'keySpectrumQFactor'
    _keySpectrumSource = 'keySpectrumSource'
    _keySpectrumRun = 'keySpectrumRun'
    _keyChipReset = 'keyChipReset'
    _keyChipResetMode = 'keyChipResetMode'
    _keyChipClockSource = 'keyChipClockSource'
    _keyCouplingMode = 'keyCouplingMode'

    def __init__(self, preamp_data):
        self._preamp_data = preamp_data

        self._set_volume_map()

        # data to write on device over I2C (bin values)
        self._DataMainSource = 0
        self._DataSecondSource = 0
        self._DataLoudness = 0
        self._DataSoftMute = 0
        self._DataTreble = 0
        self._DataMiddle = 0
        self._DataBass = 0
        self._DataSubSetup = 0
        self._DataMixLevel = 0
        self._DataDriverSetup = 0

        # volumes data
        self._MainVolume = 0
        self._LFSpeaker = 0
        self._RFSpeaker = 0
        self._LRSpeaker = 0
        self._RRSpeaker = 0
        self._SubVolume = 0
        self._MixGain = 0

        # values saved on self and in persistence
        self._VolumesSoftStep = 0

        self._MainSourceValue = self._preamp_data.get(self._keyMainSourceValue)
        self._MainSourceGain = self._preamp_data.get(self._keyMainSourceGain)
        self._SecondSourceValue = self._preamp_data.get(self._keySecondSourceValue)
        self._SecondSourceGain = self._preamp_data.get(self._keySecondSourceGain)
        self._SecondSourceRearSource = self._preamp_data.get(self._keySecondSourceRearSource)
        self._LoudnessValue = self._preamp_data.get(self._keyLoudnessValue)
        self._LoudnessFreq = self._preamp_data.get(self._keyLoudnessFreq)
        self._LoudnessBoost = self._preamp_data.get(self._keyLoudnessBoost)
        self._LoudnessSoftStep = self._preamp_data.get(self._keyLoudnessSoftStep)
        self._SoftMuteValue = self._preamp_data.get(self._keySoftMuteValue)
        self._SoftMuteEnable = self._preamp_data.get(self._keySoftMuteEnable)
        self._SoftMutePin = self._preamp_data.get(self._keySoftMutePin)
        self._SoftMuteTime = self._preamp_data.get(self._keySoftMuteTime)
        self._SoftMuteTimeStep = self._preamp_data.get(self._keySoftMuteTimeStep)
        self._TrebleValue = self._preamp_data.get(self._keyTrebleValue)
        self._TrebleCenterFreq = self._preamp_data.get(self._keyTrebleCenterFreq)
        self._TrebleReferenceOutput = self._preamp_data.get(self._keyTrebleReferenceOutput)
        self._MiddleValue = self._preamp_data.get(self._keyMiddleValue)
        self._MiddleQFactor = self._preamp_data.get(self._keyMiddleQFactor)
        self._MiddleSoftStep = self._preamp_data.get(self._keyMiddleSoftStep)
        self._BassValue = self._preamp_data.get(self._keyBassValue)
        self._BassQFactor = self._preamp_data.get(self._keyBassQFactor)
        self._BassSoftStep = self._preamp_data.get(self._keyBassSoftStep)
        self._SubSetupCutFreq = self._preamp_data.get(self._keySubSetupCutFreq)
        self._SubSetupMiddleFreq = self._preamp_data.get(self._keySubSetupMiddleFreq)
        self._SubSetupBassFreq = self._preamp_data.get(self._keySubSetupBassFreq)
        self._SubSetupDcMode = self._preamp_data.get(self._keySubSetupDcMode)
        self._SubSetupSmooth = self._preamp_data.get(self._keySubSetupSmooth)
        self._MixLevelValue = self._preamp_data.get(self._keyMixLevelValue)
        self._MixLevelLFS = self._preamp_data.get(self._keyMixLevelLFS)
        self._MixLevelRFS = self._preamp_data.get(self._keyMixLevelRFS)
        self._MixLevelEnable = self._preamp_data.get(self._keyMixLevelEnable)
        self._MixLevelSubEnable = self._preamp_data.get(self._keyMixLevelSubEnable)
        self._GainEffectForDso = self._preamp_data.get(self._keyGainEffectForDso)

        # driver setup
        self._SpectrumQFactor = self._preamp_data.get(self._keySpectrumQFactor)
        self._SpectrumSource = self._preamp_data.get(self._keySpectrumSource)
        self._SpectrumRun = self._preamp_data.get(self._keySpectrumRun)
        self._ChipReset = self._preamp_data.get(self._keyChipReset)
        self._ChipResetMode = self._preamp_data.get(self._keyChipResetMode)
        self._ChipClockSource = self._preamp_data.get(self._keyChipClockSource)
        self._CouplingMode = self._preamp_data.get(self._keyCouplingMode)

        self.reset()

    # init volume map
    def _set_volume_map(self):
        _volumeMap = dict()
        vol = 0
        value = 96
        while value > 15:
            _volumeMap[vol] = value
            value -= 1
            vol += 1
        value = 0
        while value < 16:
            _volumeMap[vol] = value
            value += 1
            vol += 1
        self._volumeMap = _volumeMap

    # ########### common op ############

    @staticmethod
    def limit_value(value, high, low=0):
        if value > high:
            value = high
        if value < low:
            value = low
        return value

    def write(self, addr, data):
        self.i2cBus.write_byte_data(self._driverAddr, addr, data)
        return self

    # bit op
    # data - the data to modify
    # value - the value to add to data
    # mask - length (bin)
    # pos - from position (right to left)
    # ex setBits(0b11111111, 0b0, 0b1111,11) => 0b11000011
    # - puts a zero(4bit length) on pos 2
    # ex setBits(0b11111111, 0b100, 0b1111,11) => 0b11010011
    # - puts 4(0b100) on pos 2 and a length(mask) 4bit
    @staticmethod
    def set_bits(data, value, mask, pos):
        data = (data & ~(mask << pos)) | (value << pos)
        return data

    # reset to saved state
    def reset(self):
        self.setMainSource(self._preamp_data.get(self._keyMainSourceValue), 1)
        self.setMainSourceGain(self._preamp_data.get(self._keyMainSourceGain), 1)
        self.setSecondSource(self._preamp_data.get(self._keySecondSourceValue), 1)
        self.setSecondSourceGain(self._preamp_data.get(self._keySecondSourceGain), 1)
        self.setSecondSourceRearSource(self._preamp_data.get(self._keySecondSourceRearSource), 1)
        self.setLoudness(self._preamp_data.get(self._keyLoudnessValue), 1)
        self.setLoudnessFreq(self._preamp_data.get(self._keyLoudnessFreq), 1)
        self.setLoudnessBoost(self._preamp_data.get(self._keyLoudnessBoost), 1)
        self.setLoudnessSoftStep(self._preamp_data.get(self._keyLoudnessSoftStep), 1)
        self.setSoftMute(self._preamp_data.get(self._keySoftMuteValue), 1)
        self.setSoftMuteEnable(self._preamp_data.get(self._keySoftMuteEnable), 1)
        self.setSoftMutePin(self._preamp_data.get(self._keySoftMutePin), 1)
        self.setSoftMuteTime(self._preamp_data.get(self._keySoftMuteTime), 1)
        self.setSoftMuteTimeStep(self._preamp_data.get(self._keySoftMuteTimeStep), 1)
        self.setTreble(self._preamp_data.get(self._keyTrebleValue), 1)
        self.setTrebleCenterFreq(self._preamp_data.get(self._keyTrebleCenterFreq), 1)
        self.setTrebleReferenceOutput(self._preamp_data.get(self._keyTrebleReferenceOutput), 1)
        self.setMiddle(self._preamp_data.get(self._keyMiddleValue), 1)
        self.setMiddleQFactor(self._preamp_data.get(self._keyMiddleQFactor), 1)
        self.setMiddleSoftStep(self._preamp_data.get(self._keyMiddleSoftStep), 1)
        self.setBass(self._preamp_data.get(self._keyBassValue), 1)
        self.setBassQFactor(self._preamp_data.get(self._keyBassQFactor), 1)
        self.setBassSoftStep(self._preamp_data.get(self._keyBassSoftStep), 1)
        self.setSubSetupCutFreq(self._preamp_data.get(self._keySubSetupCutFreq), 1)
        self.setSubSetupMiddleFreq(self._preamp_data.get(self._keySubSetupMiddleFreq), 1)
        self.setSubSetupBassFreq(self._preamp_data.get(self._keySubSetupBassFreq), 1)
        self.setSubSetupDcMode(self._preamp_data.get(self._keySubSetupDcMode), 1)
        self.setSubSetupSmooth(self._preamp_data.get(self._keySubSetupSmooth), 1)
        self.setMixLevel(self._preamp_data.get(self._keyMixLevelValue), 1)
        self.setMixLevelLFS(self._preamp_data.get(self._keyMixLevelLFS), 1)
        self.setMixLevelRFS(self._preamp_data.get(self._keyMixLevelRFS), 1)
        self.setMixLevelEnable(self._preamp_data.get(self._keyMixLevelEnable), 1)
        self.setMixLevelSubEnable(self._preamp_data.get(self._keyMixLevelSubEnable), 1)
        self.setGainEffectForDso(self._preamp_data.get(self._keyGainEffectForDso), 1)
        self.setSpectrumQFactor(self._preamp_data.get(self._keySpectrumQFactor), 1)
        self.setSpectrumSource(self._preamp_data.get(self._keySpectrumSource), 1)
        self.setSpectrumRun(self._preamp_data.get(self._keySpectrumRun), 1)
        self.setChipReset(self._preamp_data.get(self._keyChipReset), 1)
        self.setChipResetMode(self._preamp_data.get(self._keyChipResetMode), 1)
        self.setChipClockSource(self._preamp_data.get(self._keyChipClockSource), 1)
        self.setCouplingMode(self._preamp_data.get(self._keyCouplingMode), 1)

        self.set_volumes_soft_step(self._preamp_data.get(self._keyVolumesSoftStep))
        self._reinit_volumes()
        # coupling mode, clock source, reset, spectrum
        # self.write(self._addr_driver_setup, 80)

    # reinit volumes
    def _reinit_volumes(self):
        self.set_main_volume(self._preamp_data.get(self._keyMainVolume), self._VolumesSoftStep)
        self.set_front_left_speaker_volume(self._preamp_data.get(self._keyLFSpeaker), self._VolumesSoftStep)
        self.set_front_right_speaker_volume(self._preamp_data.get(self._keyRFSpeaker), self._VolumesSoftStep)
        self.set_rear_left_speaker_volume(self._preamp_data.get(self._keyLRSpeaker), self._VolumesSoftStep)
        self.set_rear_right_speaker_volume(self._preamp_data.get(self._keyRRSpeaker), self._VolumesSoftStep)
        self.set_subwoofer_volume(self._preamp_data.get(self._keySubVolume), self._VolumesSoftStep)
        self.setMixGain(self._preamp_data.get(self._keyMixGain), self._VolumesSoftStep)

    # reset all  values to default
    def reset_to_default(self):
        self._preamp_data.get_defaults()
        self.reset()

    def save_all(self):
        self._preamp_data.save_all(self)

    # set soft_step for all volumes
    # also init volumes
    def set_volumes_soft_step(self, soft_step):
        self._VolumesSoftStep = self.limit_value(soft_step, 1)
        self._preamp_data.set(self._keyVolumesSoftStep, self._VolumesSoftStep).save()
        self._reinit_volumes()
        return self

    # get soft_step (general soft step)
    def get_volumes_soft_step(self):
        return self._VolumesSoftStep

    # get data from spectrumn analizer
    def get_spectrum_data(self):
        return self._spectrum.get_data()

    # ################### generated class content ###################

    #  ############# VOLUMES ##############

    # set master volume
    # value 0-96 +0, +1...+15 -0, -1, -2...-78, -79, mute dB
    def set_main_volume(self, value, soft_step=None):
        if soft_step is None:
            soft_step = self._VolumesSoftStep

        self._MainVolume = self._set_volume(value, self._addr_main_volume, self._keyMainVolume, soft_step)
        return self

    def get_main_volume(self):
        return self._MainVolume

    # set left front speaker volume
    # value 0-96 +0, +1...+15 -0, -1, -2...-78, -79, mute dB
    def set_front_left_speaker_volume(self, value, soft_step=None):
        if soft_step is None:
            soft_step = self._VolumesSoftStep

        self._LFSpeaker = self._set_volume(value, self._addr_l_f_speaker, self._keyLFSpeaker, soft_step)
        return self

    def get_front_left_speaker_volume(self):
        return self._LFSpeaker

    # set right front speaker volume
    # value 0-96 +0, +1...+15 -0, -1, -2...-78, -79, mute dB
    def set_front_right_speaker_volume(self, value, soft_step=None):
        if soft_step is None:
            soft_step = self._VolumesSoftStep

        self._RFSpeaker = self._set_volume(value, self._addr_r_f_speaker, self._keyRFSpeaker, soft_step)
        return self

    def get_front_right_speaker_volume(self):
        return self._RFSpeaker

    # set left rear speaker volume
    # value 0-96 +0, +1...+15 -0, -1, -2...-78, -79, mute dB
    def set_rear_left_speaker_volume(self, value, soft_step=None):
        if soft_step is None:
            soft_step = self._VolumesSoftStep

        self._LRSpeaker = self._set_volume(value, self._addr_l_r_speaker, self._keyLRSpeaker, soft_step)
        return self

    def get_rear_left_speaker_volume(self):
        return self._LRSpeaker

    # set right rear speaker volume
    # value 0-96 +0, +1...+15 -0, -1, -2...-78, -79, mute dB
    def set_rear_right_speaker_volume(self, value, soft_step=None):
        if soft_step is None:
            soft_step = self._VolumesSoftStep

        self._RRSpeaker = self._set_volume(value, self._addr_r_r_speaker, self._keyRRSpeaker, soft_step)
        return self

    def get_rear_right_speaker_volume(self):
        return self._RRSpeaker

    # set woofer volume
    # value 0-96 +0, +1...+15 -0, -1, -2...-78, -79, mute dB
    def set_subwoofer_volume(self, value, soft_step=None):
        if soft_step is None:
            soft_step = self._VolumesSoftStep

        self._SubVolume = self._set_volume(value, self._addr_subwoofer_volume, self._keySubVolume, soft_step)
        return self

    def get_subwoofer_volume(self):
        return self._SubVolume

    # set mix gain effect volume
    # value 0-96 +0, +1...+15 -0, -1, -2...-78, -79, mute dB
    def set_mix_gain(self, value, soft_step=None):
        if soft_step is None:
            soft_step = self._VolumesSoftStep

        self._MixGain = self._set_volume(value, self._addr_mix_gain, self._keyMixGain, soft_step)
        return self

    def get_mix_gain(self):
        return self._MixGain

    # set general volume
    def _set_volume(self, value, addr, saveKey=False, soft_step=0):
        volume = self.limit_value(value, 96)
        data = self.set_bits(self._volumeMap[volume], soft_step, 1, 7)
        self.write(addr, data)
        if saveKey:
            self._preamp_data.set(saveKey, volume).save()
        return volume

    # ############### IC op ##############

    # MainSource
    # value 0-5 5 = mute
    def setMainSource(self, value, save=1):
        value = self.limit_value(value, 5)
        self.setSoftMute(1)

        self._DataMainSource = self.set_bits(self._DataMainSource, value, 7, 0)
        self.write(self._addr_main_source, self._DataMainSource)
        self._MainSourceValue = value
        if save:
            self._preamp_data.set(self._keyDataMainSource, self._DataMainSource).save()
            self._preamp_data.set(self._keyMainSourceValue, value).save()

        self.setSoftMute(0)
        return self

    def getMainSource(self):
        return self._MainSourceValue

    # MainSourceGain
    # value 0-15 -- 0 to +15bB
    def setMainSourceGain(self, value, save=1):
        value = self.limit_value(value, 15)
        self.setSoftMute(1)

        self._DataMainSource = self.set_bits(self._DataMainSource, value, 15, 3)
        self.write(self._addr_main_source, self._DataMainSource)
        self._MainSourceGain = value
        if save:
            self._preamp_data.set(self._keyMainSourceGain, value).save()
            self._preamp_data.set(self._keyDataMainSource, self._DataMainSource).save()

        self.setSoftMute(0)

        return self

    def getMainSourceGain(self):
        return self._MainSourceGain

    # SecondSource
    # value 0-5 5 = mute
    def setSecondSource(self, value, save=1):
        value = self.limit_value(value, 5)
        self._DataSecondSource = self.set_bits(self._DataSecondSource, value, 7, 0)
        self.write(self._addr_second_source, self._DataSecondSource)
        self._SecondSourceValue = value
        if save:
            self._preamp_data.set(self._keyDataSecondSource, self._DataSecondSource).save()
            self._preamp_data.set(self._keySecondSourceValue, value).save()
        return self

    def getSecondSource(self):
        return self._SecondSourceValue

    # SecondSourceGain
    # value 0-15 0 to 15 dB
    def setSecondSourceGain(self, value, save=1):
        value = self.limit_value(value, 15)
        self._DataSecondSource = self.set_bits(self._DataSecondSource, value, 15, 3)
        self.write(self._addr_second_source, self._DataSecondSource)
        self._SecondSourceGain = value
        if save:
            self._preamp_data.set(self._keySecondSourceGain, value).save()
            self._preamp_data.set(self._keyDataSecondSource, self._DataSecondSource).save()
        return self

    def getSecondSourceGain(self):
        return self._SecondSourceGain

    # SecondSource - use for rear
    # value 0/1 0- main source, 1- second source
    def setSecondSourceRearSource(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataSecondSource = self.set_bits(self._DataSecondSource, value, 1, 7)
        self.write(self._addr_second_source, self._DataSecondSource)
        self._SecondSourceRearSource = value
        if save:
            self._preamp_data.set(self._keySecondSourceRearSource, value).save()
            self._preamp_data.set(self._keyDataSecondSource, self._DataSecondSource).save()
        return self

    def getSecondSourceRearSource(self):
        return self._SecondSourceRearSource

    # Loudness
    # value 0-15 0 to -15 dB
    def setLoudness(self, value, save=1):
        value = self.limit_value(value, 15)
        self._DataLoudness = self.set_bits(self._DataLoudness, value, 15, 0)
        self.write(self._addr_loudness, self._DataLoudness)
        self._LoudnessValue = value
        if save:
            self._preamp_data.set(self._keyDataLoudness, self._DataLoudness).save()
            self._preamp_data.set(self._keyLoudnessValue, value).save()
        return self

    def getLoudness(self):
        return self._LoudnessValue

    # Loudness frequency
    # value 0-3 0-flat, 1-400Hz, 2-800Hz, 3-2400Hz
    def setLoudnessFreq(self, value, save=1):
        value = self.limit_value(value, 3)
        self._DataLoudness = self.set_bits(self._DataLoudness, value, 3, 4)
        self.write(self._addr_loudness, self._DataLoudness)
        self._LoudnessFreq = value
        if save:
            self._preamp_data.set(self._keyLoudnessFreq, value).save()
            self._preamp_data.set(self._keyDataLoudness, self._DataLoudness).save()
        return self

    def getLoudnessFreq(self):
        return self._LoudnessFreq

    # Loudness high boost
    # value 0-1 on/off
    def setLoudnessBoost(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataLoudness = self.set_bits(self._DataLoudness, value, 1, 6)
        self.write(self._addr_loudness, self._DataLoudness)
        self._LoudnessBoost = value
        if save:
            self._preamp_data.set(self._keyLoudnessBoost, value).save()
            self._preamp_data.set(self._keyDataLoudness, self._DataLoudness).save()
        return self

    def getLoudnessBoost(self):
        return self._LoudnessBoost

    # Loudness soft step
    # value 0-1 on/off
    def setLoudnessSoftStep(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataLoudness = self.set_bits(self._DataLoudness, value, 1, 7)
        self.write(self._addr_loudness, self._DataLoudness)
        self._LoudnessSoftStep = value
        if save:
            self._preamp_data.set(self._keyLoudnessSoftStep, value).save()
            self._preamp_data.set(self._keyDataLoudness, self._DataLoudness).save()
        return self

    def getLoudnessSoftStep(self):
        return self._LoudnessSoftStep

    # SoftMute On/Off
    # value 1 - 0 on/off
    def setSoftMute(self, value, save=1):
        value = self.limit_value(value, 1)
        value = not bool(value)  # value 0-1 on/off

        self._DataSoftMute = self.set_bits(self._DataSoftMute, value, 1, 0)
        self.write(self._addr_soft_mute, self._DataSoftMute)
        self._SoftMuteValue = value
        if save:
            self._preamp_data.set(self._keyDataSoftMute, self._DataSoftMute).save()
            self._preamp_data.set(self._keySoftMuteValue, value).save()
        return self

    def getSoftMute(self):
        return self._SoftMuteValue

    # SoftMute On/Off == setSoftMute
    # value 1 - 0 on/off
    def setSoftMuteEnable(self, value, save=1):
        value = self.limit_value(value, 1)
        value = not bool(value)  # value 0-1 on/off

        self._DataSoftMute = self.set_bits(self._DataSoftMute, value, 1, 0)
        self.write(self._addr_soft_mute, self._DataSoftMute)
        self._SoftMuteEnable = value
        if save:
            self._preamp_data.set(self._keySoftMuteEnable, value).save()
            self._preamp_data.set(self._keyDataSoftMute, self._DataSoftMute).save()
        return self

    def getSoftMuteEnable(self):
        return self._SoftMuteEnable

    # SoftMute pin influence for mute ?????
    # value 0-1 ??
    def setSoftMutePin(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataSoftMute = self.set_bits(self._DataSoftMute, value, 1, 1)
        self.write(self._addr_soft_mute, self._DataSoftMute)
        self._SoftMutePin = value
        if save:
            self._preamp_data.set(self._keySoftMutePin, value).save()
            self._preamp_data.set(self._keyDataSoftMute, self._DataSoftMute).save()
        return self

    def getSoftMutePin(self):
        return self._SoftMutePin

    # SoftMute soft mute time
    # 0-2  0.48, 0.96, 1.23 ms
    def setSoftMuteTime(self, value, save=1):
        value = self.limit_value(value, 2)
        self._DataSoftMute = self.set_bits(self._DataSoftMute, value, 7, 2)
        self.write(self._addr_soft_mute, self._DataSoftMute)
        self._SoftMuteTime = value
        if save:
            self._preamp_data.set(self._keySoftMuteTime, value).save()
            self._preamp_data.set(self._keyDataSoftMute, self._DataSoftMute).save()
        return self

    def getSoftMuteTime(self):
        return self._SoftMuteTime

    # SoftMute soft step time
    # 0-7 0.160, 0.321, 0.642, 1.28, 2.56, 5.21, 10.24, 20.48 ms
    def setSoftMuteTimeStep(self, value, save=1):
        value = self.limit_value(value, 7)
        self._DataSoftMute = self.set_bits(self._DataSoftMute, value, 7, 4)
        self.write(self._addr_soft_mute, self._DataSoftMute)
        self._SoftMuteTimeStep = value
        if save:
            self._preamp_data.set(self._keySoftMuteTimeStep, value).save()
            self._preamp_data.set(self._keyDataSoftMute, self._DataSoftMute).save()
        return self

    def getSoftMuteTimeStep(self):
        return self._SoftMuteTimeStep

    # Treble Gain
    # value -15 - +15 -15 to +15dB
    def setTreble(self, value, save=1):
        value = self.limit_value(value, 15, -15)
        sign = 1
        if value < 0:
            sign = 0
        self._DataTreble = self.set_bits(self._DataTreble, abs(value), 15, 0)
        self._DataTreble = self.set_bits(self._DataTreble, sign, 1, 4)
        self.write(self._addr_treble, self._DataTreble)
        self._TrebleValue = value
        if save:
            self._preamp_data.set(self._keyDataTreble, self._DataTreble).save()
            self._preamp_data.set(self._keyTrebleValue, value).save()
        return self

    def getTreble(self):
        return self._TrebleValue

    # Treble center freq
    # value 0-3 10.0, 12.5, 15.0, 17.5 kHz
    def setTrebleCenterFreq(self, value, save=1):
        value = self.limit_value(value, 3)
        self._DataTreble = self.set_bits(self._DataTreble, value, 3, 5)
        self.write(self._addr_treble, self._DataTreble)
        self._TrebleCenterFreq = value
        if save:
            self._preamp_data.set(self._keyTrebleCenterFreq, value).save()
            self._preamp_data.set(self._keyDataTreble, self._DataTreble).save()
        return self

    def getTrebleCenterFreq(self):
        return self._TrebleCenterFreq

    # Treble soft step
    # value 0-1
    def setTrebleReferenceOutput(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataTreble = self.set_bits(self._DataTreble, value, 1, 7)
        self.write(self._addr_treble, self._DataTreble)
        self._TrebleReferenceOutput = value
        if save:
            self._preamp_data.set(self._keyTrebleReferenceOutput, value).save()
            self._preamp_data.set(self._keyDataTreble, self._DataTreble).save()
        return self

    def getTrebleReferenceOutput(self):
        return self._TrebleReferenceOutput

    # Middle gain
    # value -15 - +15 => -15 to +15 dB
    def setMiddle(self, value, save=1):
        value = self.limit_value(value, 15, -15)
        sign = 1
        if value < 0:
            sign = 0
        self._DataMiddle = self.set_bits(self._DataMiddle, abs(value), 15, 0)
        self._DataMiddle = self.set_bits(self._DataMiddle, sign, 1, 4)
        self.write(self._addr_middle, self._DataMiddle)
        self._MiddleValue = value
        if save:
            self._preamp_data.set(self._keyDataMiddle, self._DataMiddle).save()
            self._preamp_data.set(self._keyMiddleValue, value).save()
        return self

    def getMiddle(self):
        return self._MiddleValue

    # Middle Q Factor
    # value 0-3 => 0.5, 0.75, 1, 1.25
    def setMiddleQFactor(self, value, save=1):
        value = self.limit_value(value, 3)
        self._DataMiddle = self.set_bits(self._DataMiddle, value, 3, 5)
        self.write(self._addr_middle, self._DataMiddle)
        self._MiddleQFactor = value
        if save:
            self._preamp_data.set(self._keyMiddleQFactor, value).save()
            self._preamp_data.set(self._keyDataMiddle, self._DataMiddle).save()
        return self

    def getMiddleQFactor(self):
        return self._MiddleQFactor

    # Middle soft step enable
    # value 0-1 on/off
    def setMiddleSoftStep(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataMiddle = self.set_bits(self._DataMiddle, value, 1, 7)
        self.write(self._addr_middle, self._DataMiddle)
        self._MiddleSoftStep = value
        if save:
            self._preamp_data.set(self._keyMiddleSoftStep, value).save()
            self._preamp_data.set(self._keyDataMiddle, self._DataMiddle).save()
        return self

    def getMiddleSoftStep(self):
        return self._MiddleSoftStep

    # Bass gain
    # value -15 - +15 => -15 to +15 dB
    def setBass(self, value, save=1):
        value = self.limit_value(value, 15, -15)
        sign = 1
        if value < 0:
            sign = 0
        self._DataBass = self.set_bits(self._DataBass, abs(value), 15, 0)
        self._DataBass = self.set_bits(self._DataBass, sign, 1, 4)
        self.write(self._addr_bass, self._DataBass)
        self._BassValue = value
        if save:
            self._preamp_data.set(self._keyDataBass, self._DataBass).save()
            self._preamp_data.set(self._keyBassValue, value).save()
        return self

    def getBass(self):
        return self._BassValue

    # Bass Q Factor
    # value 0-3 => 0.5, 0.75, 1, 1.25
    def setBassQFactor(self, value, save=1):
        value = self.limit_value(value, 3)
        self._DataBass = self.set_bits(self._DataBass, value, 3, 5)
        self.write(self._addr_bass, self._DataBass)
        self._BassQFactor = value
        if save:
            self._preamp_data.set(self._keyBassQFactor, value).save()
            self._preamp_data.set(self._keyDataBass, self._DataBass).save()
        return self

    def getBassQFactor(self):
        return self._BassQFactor

    # Bass soft step
    # value 0-1  on/off
    def setBassSoftStep(self, value, save=1):
        value = self.limit_value(value, 0)
        self._DataBass = self.set_bits(self._DataBass, value, 0, 0)
        self.write(self._addr_bass, self._DataBass)
        self._BassSoftStep = value
        if save:
            self._preamp_data.set(self._keyBassSoftStep, value).save()
            self._preamp_data.set(self._keyDataBass, self._DataBass).save()
        return self

    def getBassSoftStep(self):
        return self._BassSoftStep

    # SubSetup cut off freq
    # value 0-3 flat, 80, 120, 160 Hz
    def setSubSetupCutFreq(self, value, save=1):
        value = self.limit_value(value, 3)
        self._DataSubSetup = self.set_bits(self._DataSubSetup, value, 3, 0)
        self.write(self._addr_subwoofer_setup, self._DataSubSetup)
        self._SubSetupCutFreq = value
        if save:
            self._preamp_data.set(self._keySubSetupCutFreq, value).save()
            self._preamp_data.set(self._keyDataSubSetup, self._DataSubSetup).save()
        return self

    def getSubSetupCutFreq(self):
        return self._SubSetupCutFreq

    # SubSetup middle center freq
    # value 0-3 500, 1000, 1500, 2000 Hz
    def setSubSetupMiddleFreq(self, value, save=1):
        value = self.limit_value(value, 3)
        self._DataSubSetup = self.set_bits(self._DataSubSetup, value, 3, 2)
        self.write(self._addr_subwoofer_setup, self._DataSubSetup)
        self._SubSetupMiddleFreq = value
        if save:
            self._preamp_data.set(self._keySubSetupMiddleFreq, value).save()
            self._preamp_data.set(self._keyDataSubSetup, self._DataSubSetup).save()
        return self

    def getSubSetupMiddleFreq(self):
        return self._SubSetupMiddleFreq

    # SubSetup bass freq
    # value 0-3 60, 80, 100, 200 Hz
    def setSubSetupBassFreq(self, value, save=1):
        value = self.limit_value(value, 3)
        self._DataSubSetup = self.set_bits(self._DataSubSetup, value, 3, 4)
        self.write(self._addr_subwoofer_setup, self._DataSubSetup)
        self._SubSetupBassFreq = value
        if save:
            self._preamp_data.set(self._keySubSetupBassFreq, value).save()
            self._preamp_data.set(self._keyDataSubSetup, self._DataSubSetup).save()
        return self

    def getSubSetupBassFreq(self):
        return self._SubSetupBassFreq

    # SubSetup dc mode
    # value 0-1 on/off
    def setSubSetupDcMode(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataSubSetup = self.set_bits(self._DataSubSetup, value, 1, 6)
        self.write(self._addr_subwoofer_setup, self._DataSubSetup)
        self._SubSetupDcMode = value
        if save:
            self._preamp_data.set(self._keySubSetupDcMode, value).save()
            self._preamp_data.set(self._keyDataSubSetup, self._DataSubSetup).save()
        return self

    def getSubSetupDcMode(self):
        return self._SubSetupDcMode

    # SubSetup shooting filter
    # value 0-1 on/off
    def setSubSetupSmooth(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataSubSetup = self.set_bits(self._DataSubSetup, value, 1, 7)
        self.write(self._addr_subwoofer_setup, self._DataSubSetup)
        self._SubSetupSmooth = value
        if save:
            self._preamp_data.set(self._keySubSetupSmooth, value).save()
            self._preamp_data.set(self._keyDataSubSetup, self._DataSubSetup).save()
        return self

    def getSubSetupSmooth(self):
        return self._SubSetupSmooth

    # MixLevel gain effect for dso filter
    # value 0-11 4,6,8,...18,20,22,0 dB
    def setMixLevel(self, value, save=1):
        value = self.limit_value(value, 11)
        self._DataMixLevel = self.set_bits(self._DataMixLevel, value, 15, 4)
        self.write(self._addr_mix_level, self._DataMixLevel)
        self._MixLevelValue = value
        if save:
            self._preamp_data.set(self._keyDataMixLevel, self._DataMixLevel).save()
            self._preamp_data.set(self._keyMixLevelValue, value).save()
        return self

    def getMixLevel(self):
        return self._MixLevelValue

    # MixLevel mix to left front speaker
    # value 0-1 on/off
    def setMixLevelLFS(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataMixLevel = self.set_bits(self._DataMixLevel, value, 1, 0)
        self.write(self._addr_mix_level, self._DataMixLevel)
        self._MixLevelLFS = value
        if save:
            self._preamp_data.set(self._keyMixLevelLFS, value).save()
            self._preamp_data.set(self._keyDataMixLevel, self._DataMixLevel).save()
        return self

    def getMixLevelLFS(self):
        return self._MixLevelLFS

    # MixLevel mix to right front speaker
    # value 0-1 on/off
    def setMixLevelRFS(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataMixLevel = self.set_bits(self._DataMixLevel, value, 1, 1)
        self.write(self._addr_mix_level, self._DataMixLevel)
        self._MixLevelRFS = value
        if save:
            self._preamp_data.set(self._keyMixLevelRFS, value).save()
            self._preamp_data.set(self._keyDataMixLevel, self._DataMixLevel).save()
        return self

    def getMixLevelRFS(self):
        return self._MixLevelRFS

    # MixLevel enable 
    # value 0-1 on/off
    def setMixLevelEnable(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataMixLevel = self.set_bits(self._DataMixLevel, value, 1, 2)
        self.write(self._addr_mix_level, self._DataMixLevel)
        self._MixLevelEnable = value
        if save:
            self._preamp_data.set(self._keyMixLevelEnable, value).save()
            self._preamp_data.set(self._keyDataMixLevel, self._DataMixLevel).save()
        return self

    def getMixLevelEnable(self):
        return self._MixLevelEnable

    # MixLevel enable subwoofer (OUTLR2 && OUTRR2)
    # value 0-1 on/off
    def setMixLevelSubEnable(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataMixLevel = self.set_bits(self._DataMixLevel, value, 1, 3)
        self.write(self._addr_mix_level, self._DataMixLevel)
        self._MixLevelSubEnable = value
        if save:
            self._preamp_data.set(self._keyMixLevelSubEnable, value).save()
            self._preamp_data.set(self._keyDataMixLevel, self._DataMixLevel).save()
        return self

    def getMixLevelSubEnable(self):
        return self._MixLevelSubEnable

    # Gain effect for dso filter
    # value 4,6,...20,22, 0,0 dB - 0, 1, --- 11
    def setGainEffectForDso(self, value, save=1):
        value = self.limit_value(value, 11)
        self._DataMixLevel = self.set_bits(self._DataMixLevel, value, 15, 4)
        self.write(self._addr_mix_level, self._DataMixLevel)
        self._GainEffectForDso = value
        if save:
            self._preamp_data.set(self._keyGainEffectForDso, value).save()
            self._preamp_data.set(self._keyDataMixLevel, self._DataMixLevel).save()
        return self

    def getGainEffectForDso(self):
        return self._GainEffectForDso

    # Spectrum q factor
    # value 1/0
    def setSpectrumQFactor(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataDriverSetup = self.set_bits(self._DataDriverSetup, value, 1, 0)
        self.write(self._addr_driver_setup, self._DataDriverSetup)
        self._SpectrumQFactor = value
        if save:
            self._preamp_data.set(self._keySpectrumQFactor, value).save()
            self._preamp_data.set(self._keyDataDriverSetup, self._DataDriverSetup).save()
        return self

    def getSpectrumQFactor(self):
        return self._SpectrumQFactor

    # Spectrum source
    # value bass/inGain 0/1
    def setSpectrumSource(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataDriverSetup = self.set_bits(self._DataDriverSetup, value, 1, 2)
        self.write(self._addr_driver_setup, self._DataDriverSetup)
        self._SpectrumSource = value
        if save:
            self._preamp_data.set(self._keySpectrumSource, value).save()
            self._preamp_data.set(self._keyDataDriverSetup, self._DataDriverSetup).save()
        return self

    def getSpectrumSource(self):
        return self._SpectrumSource

    # Enable Spectrum
    # value 0/1
    def setSpectrumRun(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataDriverSetup = self.set_bits(self._DataDriverSetup, value, 1, 3)
        self.write(self._addr_driver_setup, self._DataDriverSetup)
        self._SpectrumRun = value
        if save:
            self._preamp_data.set(self._keySpectrumRun, value).save()
            self._preamp_data.set(self._keyDataDriverSetup, self._DataDriverSetup).save()
        return self

    def getSpectrumRun(self):
        return self._SpectrumRun

    # Auto reset
    # value 0/1
    def setChipReset(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataDriverSetup = self.set_bits(self._DataDriverSetup, value, 1, 4)
        self.write(self._addr_driver_setup, self._DataDriverSetup)
        self._ChipReset = value
        if save:
            self._preamp_data.set(self._keyChipReset, value).save()
            self._preamp_data.set(self._keyDataDriverSetup, self._DataDriverSetup).save()
        return self

    def getChipReset(self):
        return self._ChipReset

    # Chip reset mode
    # value IIC/Auto 0/1
    def setChipResetMode(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataDriverSetup = self.set_bits(self._DataDriverSetup, value, 1, 1)
        self.write(self._addr_driver_setup, self._DataDriverSetup)
        self._ChipResetMode = value
        if save:
            self._preamp_data.set(self._keyChipResetMode, value).save()
            self._preamp_data.set(self._keyDataDriverSetup, self._DataDriverSetup).save()
        return self

    def getChipResetMode(self):
        return self._ChipResetMode

    # Set chip clock source
    # internal/external 0/1
    def setChipClockSource(self, value, save=1):
        value = self.limit_value(value, 1)
        self._DataDriverSetup = self.set_bits(self._DataDriverSetup, value, 1, 5)
        self.write(self._addr_driver_setup, self._DataDriverSetup)
        self._ChipClockSource = value
        if save:
            self._preamp_data.set(self._keyChipClockSource, value).save()
            self._preamp_data.set(self._keyDataDriverSetup, self._DataDriverSetup).save()
        return self

    def getChipClockSource(self):
        return self._ChipClockSource

    # Chip coupling mode
    # DC coupling(without DSO), AC (after in gain), DC (with DSO), AC (after bass)
    # 0, 1, 2, 3
    def setCouplingMode(self, value, save=1):
        value = self.limit_value(value, 3)
        self._DataDriverSetup = self.set_bits(self._DataDriverSetup, value, 3, 6)
        self.write(self._addr_driver_setup, self._DataDriverSetup)
        self._CouplingMode = value
        if save:
            self._preamp_data.set(self._keyCouplingMode, value).save()
            self._preamp_data.set(self._keyDataDriverSetup, self._DataDriverSetup).save()
        return self

    def getCouplingMode(self):
        return self._CouplingMode
