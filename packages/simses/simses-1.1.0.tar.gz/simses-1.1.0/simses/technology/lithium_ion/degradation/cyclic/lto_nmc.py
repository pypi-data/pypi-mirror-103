import scipy.integrate as integrate
import math

from simses.commons.cycle_detection.cycle_detector import CycleDetector
from simses.commons.log import Logger
from simses.commons.state.technology.lithium_ion import LithiumIonState
from simses.technology.lithium_ion.cell.type import CellType
from simses.technology.lithium_ion.degradation.cyclic.cyclic_degradation import \
    CyclicDegradationModel

# TODO: Source


class LTONMCCyclicDegradationModel(CyclicDegradationModel):

    def __init__(self, cell_type: CellType, cycle_detector: CycleDetector):
        super().__init__(cell_type, cycle_detector)
        self.__log: Logger = Logger(type(self).__name__)

        self.__capacity_loss = 0
        self.__initial_capacity = self._cell.get_nominal_capacity()
        self.__capacity_loss_cyclic = cell_type.get_cyclic_capacity_loss_start()

        self.__A_QLOSS = -1.914 * 10 ** (-4)  # constant
        self.__B_QLOSS = 0.05655  # constant

        self.__resistance_increase = 0

        self.__A_RINC = -0.0020  # constant
        self.__B_RINC = 0.0021  # constant
        self.__C_RINC = 6.8477  # constant
        self.__D_RINC = 0.91882  # constant

    def calculate_degradation(self, battery_state: LithiumIonState) -> None:
        # Source:
        # Thomas Nemeth, Philipp Schröer, Matthias Kuipers, Dirk Uwe Sauer:
        # Lithium titanate oxide battery cells for high-power automotive applications -
        # Electro-thermal  properties, aging behavior and cost considerations,
        # Journal of Energy Storage 31 (2020) 101656, https://doi.org/10.1016/j.est.2020.101656

        qloss: float = self.__capacity_loss_cyclic  # in pu
        delta_fec: float = self._cycle_detector.get_delta_full_equivalent_cycle()  # in pu
        temperature: float = battery_state.temperature  # in K
        # No data available for Temperatures under 298.15 K and over 318.15 K
        # Therefore if Temperature is under/over 298.15 K/318.15 K the simulation uses 298.15 K/318.15 K
        if temperature < 298.15:
            temperature = 298.15
            self.__log.warn('Temperature is under 298.15K but the simulation used 298.15K.')
        if temperature > 318.15:
            temperature = 318.15
            self.__log.warn('Temperature is over 318.15K but the simulation used 318.15K.')
        #
        virtual_fec: float = ((1 - qloss) * 100 - 100) / (self.__A_QLOSS * temperature + self.__B_QLOSS)
        rel_capacity_status = lambda fec: ((self.__A_QLOSS * temperature + self.__B_QLOSS) * fec + 100) / 100  # in pu
        fec: float = virtual_fec + delta_fec
        capacity_loss = (1 - rel_capacity_status(fec)) - self.__capacity_loss_cyclic
        # Total cyclic capacity loss
        self.__capacity_loss_cyclic += capacity_loss  # in p.u.
        # Delta capacity loss
        self.__capacity_loss = capacity_loss * self._cell.get_nominal_capacity()  # in Ah

    def calculate_resistance_increase(self, battery_state: LithiumIonState) -> None:
        crate: float = self._cycle_detector.get_crate() * 3600 # in 1 / s -> *3600 -> in 1/h
        doc: float = self._cycle_detector.get_depth_of_cycle()  # in pu
        delta_fec: float = self._cycle_detector.get_delta_full_equivalent_cycle()  # in pu
        rinc: float = battery_state.resistance_increase * 100  # in pu -> *100 -> in %

        virtual_fec: float = rinc / ((self.__A_RINC * crate + self.__B_RINC) *
                                            (self.__C_RINC * (doc - 0.5)**3 + self.__D_RINC))

        resistance_increase = (self.__A_RINC * crate + self.__B_RINC) * \
                                  (self.__C_RINC * (doc - 0.5)**3 + self.__D_RINC) * (virtual_fec + delta_fec) - rinc

        # Delta resistance increase
        self.__resistance_increase = resistance_increase / 100  # in pu

    def get_degradation(self) -> float:
        capacity_loss = self.__capacity_loss
        self.__capacity_loss = 0    # Set value to 0, because cyclic losses are not calculated in each step
        return capacity_loss

    def get_resistance_increase(self) -> float:
        resistance_increase = self.__resistance_increase
        self.__resistance_increase = 0  # Set value to 0, because cyclic losses are not calculated in each step
        return resistance_increase

    def reset(self, lithium_ion_state: LithiumIonState) -> None:
        self.__capacity_loss = 0
        self.__resistance_increase = 0

    def close(self) -> None:
        self.__log.close()
