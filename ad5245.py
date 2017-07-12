"""AD5245 - device access class for the AD5245 I2C single channel digital potentiometer

This class provides access to control the AD5245 I2C device as well as helper
methods to set specific resistances and potential diferences when configured as
a rheostat or potential divider.

James Hogge, STFC Application Engineering Group.
"""

from i2c_device import I2CDevice

class AD5245(I2CDevice):
	"""AD5245 class.

	This class adds support for the AD5245 digital potentiometer allowing the
	wiper position to be controlled.
	"""	

	def __init__(self, address = 0x2c, **kwargs):
		"""Initialises the AD5245 device.
		:param addresss: Address of the AD5245 on the I2C bus
		:param kwargs: Parameters to pass to the I2CDevice
		"""

		I2CDevice.__init__(self, address, **kwargs)

		#Read back current wiper settings
                self.__wiper_pos = self.readU8(0)
                self.__tot_resistance = 100.0
                self.__low_pd = 0.0
                self.__high_pd = 3.3

        def set_total_resistance(self, resistance):
                """Sets the total resistance across the potentiometer for set_resistance()
                :param resistance: Total resistance between H- and L- (Kiloohms)
                """

                self.__tot_resistance = float(resistance)

        def set_resistance(self, resistance):
                """Sets the resistance of the wiper in rheostat mode
                :param resistance: Desired resistance between H- and W- (Kiloohms)
                """

                self.__wiper_pos = int(resistance / self.__tot_resistance * 256.0)
                self.write8(0, self.__wiper_pos)

        def set_terminal_PDs(self, low, high):
                """Sets the potential difference for H- and L- for set_PD()
                :param low: Low PD (Volts)
                :param high: High PD (Volts)
                """

                self.__low_pd = float(low)
                self.__high_pd = float(high)

        def set_PD(self, pd):
                """Sets the potential difference of the wiper in potential divider mode
                :param pd: Target potential difference (Volts)
                """

                self.__wiper_pos = int((pd - self.__low_pd) / (self.__high_pd - self.__low_pd) * 256.0)
                self.write8(0, self.__wiper_pos)

        def set_wiper(self, position):
                """Manually sets a wiper position
                :param position: Target position [0-255]
                """

                self.__wiper_pos = int(position)
                self.write8(0, self.__wiper_pos)

	def reset(self):
		"""Returns wiper to middle position
		"""

		self.__wiper_pos = 128
		self.write8(1 << 6, 128)
	
	def set_shutdown(self, enable):
                """Sets whether to use shutdown mode
                :param enable: true - device enters shutdown mode, false - normal operation
                """

                self.write8(1 << 5 if enable else 0, self.__wiper_pos)

