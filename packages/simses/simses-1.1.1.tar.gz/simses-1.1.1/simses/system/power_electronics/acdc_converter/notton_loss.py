import numpy as np

from simses.commons.log import Logger
from simses.system.power_electronics.acdc_converter.abstract_acdc_converter import AcDcConverter


class NottonLossAcDcConverter(AcDcConverter):

    # Notton Type 2 inverter
    __P0 = 0.0072
    __K = 0.0345

    __VOLUMETRIC_POWER_DENSITY = 143 * 1e6  # W / m3
    __GRAVIMETRIC_POWER_DENSITY = 17000  # W/kg
    __SPECIFIC_SURFACE_AREA = 0.0001  # in m2 / W  # TODO add exact values
    # Exemplary value from:
    # (https://www.iisb.fraunhofer.de/en/research_areas/vehicle_electronics/dcdc_converters/High_Power_Density.html)
    # ( https://www.apcuk.co.uk/app/uploads/2018/02/PE_Full_Pack.pdf )

    def __init__(self, max_power):
        super().__init__(max_power)
        self.__log: Logger = Logger(type(self).__name__)

    def to_ac(self, ac_power: float, voltage: float) -> float:
        if ac_power >= 0:
            return 0
        return min(ac_power - self.__get_loss(ac_power), 0)

    def to_dc(self, ac_power: float, voltage: float) -> float:
        if ac_power <= 0:
            return 0
        else:
            return max(ac_power - self.__get_loss(ac_power), 0)

    def to_dc_reverse(self, dc_power: float, voltage: float) -> float:
        if dc_power == 0:
            return 0.0
        elif dc_power < 0:
            self.__log.error('Power DC should be positive in to DC reverse function, but is '
                             + str(dc_power) + 'W. Check function update_ac_power_from.')
            return 0.0
        else:
            p = - dc_power / (1 - dc_power * self.__K / self.max_power)
            q = - self.__P0 * dc_power / (1 / self.max_power - abs(dc_power) * self.__K / self.max_power ** 2)
            self.__log.debug('P_DC: ' + str(dc_power))
            power_ac = max(0.0, -p / 2 + np.sqrt((p / 2) ** 2 - q))
            self.__log.debug('P_AC: ' + str(power_ac))
            return power_ac

    def to_ac_reverse(self, dc_power: float, voltage: float) -> float:
        if dc_power == 0:
            return 0.0
        elif dc_power > 0:
            self.__log.error('Power DC should be negative in to AC reverse function, but is '
                             + str(dc_power) + 'W. Check function update_ac_power_from.')
            return 0.0
        else:
            p = self.max_power / self.__K
            q = (self.__P0 * self.max_power ** 2 - abs(dc_power) * self.max_power) / self.__K
            self.__log.debug('P_DC: ' + str(dc_power))
            power_ac = min(0.0, -(-p / 2 + np.sqrt((p / 2) ** 2 - q)))
            self.__log.debug('P_AC: ' + str(power_ac))
            return power_ac

    def __get_loss(self, power: float) -> float:
        return abs(self.__P0 * self.max_power + (self.__K / self.max_power) * power ** 2)

    @property
    def volume(self) -> float:
        return self.max_power / self.__VOLUMETRIC_POWER_DENSITY

    @property
    def mass(self):
        return self.max_power / self.__GRAVIMETRIC_POWER_DENSITY

    @property
    def surface_area(self) -> float:
        return self.max_power * self.__SPECIFIC_SURFACE_AREA

    @classmethod
    def create_instance(cls, max_power: float, power_electronics_config=None):
        return NottonLossAcDcConverter(max_power)

    def close(self) -> None:
        pass
