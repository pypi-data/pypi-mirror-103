import math

from simses.commons.state.technology.lithium_ion import LithiumIonState
from simses.technology.lithium_ion.cell.type import CellType
from simses.commons.log import Logger
from simses.technology.lithium_ion.degradation.calendar.calendar_degradation import \
    CalendarDegradationModel


class LTOLMOCalendarDegradationModel(CalendarDegradationModel):

    def __init__(self, cell_type: CellType):
        super().__init__(cell_type)
        self.__log: Logger = Logger(type(self).__name__)

        self.__capacity_loss = 0
        self.__initial_capacity = self._cell.get_nominal_capacity()
        self.__capacity_loss_cal = cell_type.get_calendar_capacity_loss_start()

        self.__A_QLOSS = -1.034  # constant
        self.__B_QLOSS = 0.6754  # constant

        self.__resistance_increase = 0

        self.__K_REF_RINC = 3.4194 * 10 ** (-10)  # pu*s^(-0.5)
        self.__A_RINC = -8638.8  # K
        self.__B_RINC = 29.992  # constan
        self.__C_RINC = -3.3903  # constant
        self.__D_RINC = 1.5604  # constant
        self.__EA_RINC = 71827  # J/mol

        self.__TEMP_REF = 298.15  # K
        self.__SOC_REF = 1  # pu
        self.__R = 8.3144598  # J/(K*mol)

    def calculate_degradation(self, time: float, battery_state: LithiumIonState) -> None:
        # Source:
        # Thomas Bank, Jan Feldmann, Sebastian Klamor, Stephan Bihn, Dirk Uwe Sauer:
        # Extensive aging analysis of high-power lithium titanate oxide batteries:
        # Impact of the passive electrode effect
        # Journal of Power Sources 473 (2020) 228566, https://doi.org/10.1016/j.jpowsour.2020.228566

        time_passed = time - battery_state.time
        soc = battery_state.soc
        # According to the source, if the SOC is smaller then 0.7 there is no calendar aging
        if soc < 0.70:
            capacity_loss = 0
        else:
            qloss: float = self.__capacity_loss_cal  # in pu
            #
            virtual_time: float = ((((1 - qloss) * 100 - 100)/(self.__A_QLOSS * soc + self.__B_QLOSS)) ** 2)  # in weeks
            rel_capacity_status = lambda time: ((self.__A_QLOSS * soc + self.__B_QLOSS) * math.sqrt(time) + 100) / 100
            total_time = virtual_time + time_passed / 86400  # in weeks
            capacity_loss = (1-rel_capacity_status(total_time)) - self.__capacity_loss_cal
        # Total calendrical capacity loss
        self.__capacity_loss_cal += capacity_loss
        # Delta calendrical capacity loss
        self.__capacity_loss = capacity_loss * self.__initial_capacity

    def calculate_resistance_increase(self, time: float, battery_state: LithiumIonState) -> None:
        soc = battery_state.soc
        temp = battery_state.temperature
        time_passed = time - battery_state.time

        resistance_increase = time_passed * (self.__K_REF_RINC * math.exp(
            -self.__EA_RINC / self.__R * (1 / temp - 1 / self.__TEMP_REF)) * (
                                                       self.__C_RINC * (soc - 0.5) ** 2 + self.__D_RINC))

        self.__resistance_increase = resistance_increase # pu

    def get_degradation(self) -> float:
        return self.__capacity_loss

    def get_resistance_increase(self) -> float:
        return self.__resistance_increase

    def reset(self, battery_state: LithiumIonState) -> None:
        self.__capacity_loss = 0
        self.__resistance_increase = 0

    def close(self) -> None:
        pass
