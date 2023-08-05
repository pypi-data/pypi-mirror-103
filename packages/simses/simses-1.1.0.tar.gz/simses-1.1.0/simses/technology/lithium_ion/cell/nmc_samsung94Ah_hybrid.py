import numpy as np
import pandas as pd
from scipy import interpolate
from scipy.interpolate import RegularGridInterpolator

from simses.commons.config.data.battery import BatteryDataConfig
from simses.commons.config.simulation.battery import BatteryConfig
from simses.commons.log import Logger
from simses.commons.state.technology.lithium_ion import LithiumIonState
from simses.technology.lithium_ion.cell.electric.properties import ElectricalCellProperties
from simses.technology.lithium_ion.cell.format.abstract import CellFormat
from simses.technology.lithium_ion.cell.format.prismatic import PrismaticCell
from simses.technology.lithium_ion.cell.thermal.properties import ThermalCellProperties
from simses.technology.lithium_ion.cell.type import CellType


class Samsung94AhNMCHybrid(CellType):
    """This hybrid cell class uses a temperature dependent OCV curves as well as SOC, temperature and
    charge/discharge-rate dependent internal resistance from lab tests, combined with a published degradation
    model based on Naumann et al. Note: While the cell parameters are from a NMC cell, the degradation model is from
    a LFP cell."""

    __SOC_HEADER = 'SOC'
    __SOC_IDX = 0
    __TEMP_IDX = 1
    __C_Rate_IDX = 2

    __CELL_VOLTAGE = 3.68  # V
    __CELL_CAPACITY = 94.0  # Ah
    __MAX_VOLTAGE: float = 4.15  # V
    __MIN_VOLTAGE: float = 2.7  # V
    __MIN_TEMPERATURE: float = 233.15  # K
    __MAX_TEMPERATURE: float = 333.15  # K
    __MAX_CHARGE_RATE: float = 2.0  # 1/h
    __MAX_DISCHARGE_RATE: float = 2.0  # 1/h
    __SELF_DISCHARGE_RATE: float = 0.0  # X.X%-soc per day, e.g., 0.015 for 1.5% SOC loss per day
    __MASS: float = 2.1  # kg per cell
    __SPECIFIC_HEAT: float = 1000  # J/kgK
    __CONVECTION_COEFFICIENT: float = 15  # W/m2K

    __HEIGHT: float = 125.0  # mm
    __WIDTH: float = 45.0  # mm
    __LENGTH: float = 173.0  # mm

    __COULOMB_EFFICIENCY: float = 1.0  # p.u

    __ELECTRICAL_PROPS: ElectricalCellProperties = ElectricalCellProperties(__CELL_VOLTAGE, __CELL_CAPACITY,
                                                                            __MIN_VOLTAGE, __MAX_VOLTAGE,
                                                                            __MAX_CHARGE_RATE, __MAX_DISCHARGE_RATE,
                                                                            __SELF_DISCHARGE_RATE, __COULOMB_EFFICIENCY)
    __THERMAL_PROPS: ThermalCellProperties = ThermalCellProperties(__MIN_TEMPERATURE, __MAX_TEMPERATURE, __MASS,
                                                                   __SPECIFIC_HEAT, __CONVECTION_COEFFICIENT)
    __CELL_FORMAT: CellFormat = PrismaticCell(__HEIGHT, __WIDTH, __LENGTH)

    def __init__(self, voltage: float, capacity: float, soh: float, battery_config: BatteryConfig,
                 battery_data_config: BatteryDataConfig):
        super().__init__(voltage, capacity, soh, self.__ELECTRICAL_PROPS, self.__THERMAL_PROPS, self.__CELL_FORMAT,
                         battery_config)
        self.__log: Logger = Logger(type(self).__name__)
        rint_file: str = battery_data_config.nmc_samsung94test_rint_file
        # # Reading out the Ri.csv data
        internal_resistance = pd.read_csv(rint_file, delimiter=';', decimal=",")  # Ohm
        soc_arr = internal_resistance.iloc[:, self.__SOC_IDX]
        temp_arr = internal_resistance.iloc[:4, self.__TEMP_IDX]
        c_rate_arr = internal_resistance.iloc[:6, self.__C_Rate_IDX]
        rint_mat_ch = internal_resistance.iloc[:, 3:27]
        rint_mat_dch = internal_resistance.iloc[:, 27:]
        # Converting rint_mat_ch & rint_mat_dch into numpy arrays
        rint_mat_ch = rint_mat_ch.values
        rint_mat_dch = rint_mat_dch.values
        # Initializing empty 3D arrays for Rint_ch, Rint_dch - shape - (6, 21, 4)
        rint_mat_ch_tensor = np.ones((6, 21, 4))
        rint_mat_dch_tensor = np.ones((6, 21, 4))
        cursor = 0
        # Fill both tensors - rint_mat_ch_tensor & rint_mat_dch_tensor - with data from excel sheet
        for i in range(4):
            for j in range(6):
                rint_mat_ch_tensor[j, :, i] = rint_mat_ch_tensor[j, :, i] * rint_mat_ch[:, cursor]
                rint_mat_dch_tensor[j, :, i] = rint_mat_dch_tensor[j, :, i] * rint_mat_dch[:, cursor]
                cursor += 1
        self.__rint_ch_rgi = RegularGridInterpolator((c_rate_arr, soc_arr, temp_arr), rint_mat_ch_tensor)  # interpolation with SOC in p.u.
        self.__rint_dch_rgi = RegularGridInterpolator((c_rate_arr, soc_arr, temp_arr), rint_mat_dch_tensor)  # interpolation with SOC in p.u.
        # OCV fit parameters from datasheet values for the different temperatures, poly7 fit
        p1 = np.array([3.719e-13, 3.423e-13, 3.799e-13, 4.225e-13])
        p2 = np.array([-1.269e-10, -1.182e-10, -1.339e-10, -1.506e-10])
        p3 = np.array([1.762e-08, 1.657e-08, 1.911e-08, 2.169e-08])
        p4 = np.array([-1.307e-06, -1.24e-06, -1.445e-06, -1.644e-06])
        p5 = np.array([5.83e-05, 5.6e-05, 6.467e-05, 7.264e-05])
        p6 = np.array([-0.001617, -0.001584, -0.001772, -0.001932])
        p7 = np.array([0.02963, 0.02986, 0.03189, 0.03338])
        p8 = np.array([3.316, 3.307, 3.297, 3.29])

        # Collecting the p-values into matrix for the 1D interpolation
        poly7_values = np.array([p1, p2, p3, p4, p5, p6, p7, p8])
        self.__poly7_values_interp = interpolate.interp1d(temp_arr, poly7_values)  # interpolation with SOC in %

    def get_internal_resistance(self, battery_state: LithiumIonState) -> float:
        # temperature window limited between 5°C and 35°C due to test conditions
        if battery_state.temperature > 308.15:
            temperature: float = 308.15
            self.__log.warn("The cell resistance model is only parameterized up to 35°C.")
        elif battery_state.temperature < 278.15:
            temperature: float = 278.15
            self.__log.warn("The cell resistance model is only parameterized down to 5°C.")
        else:
            temperature: float = battery_state.temperature
        # current power limited between 0.25 C-rate and 1.5 C-rate due to test conditions
        c_rate: float = battery_state.current / self.get_nominal_capacity()
        if c_rate < 0.25:
            c_rate = 0.25
            # self.__log.warn("The cell resistance model only works with minimum current power of 0.25 C-rate.")
        if c_rate > 1.5:
            c_rate = 1.5
            self.__log.warn("The cell resistance model only works with maximum current power of 1.5 C-rate.")
        soc: float = max(0.0, min(1.0, battery_state.soc))
        # interpolation phase Ri - for charge and discharge direction
        if battery_state.is_charge:
            rint = self.__rint_ch_rgi([c_rate, soc, temperature]) / 1000  # division with 1000 - change values into Ohm
        else:
            rint = self.__rint_dch_rgi([c_rate, soc, temperature]) / 1000  # division with 1000 - change values into Ohm
        return float(rint) / self.get_parallel_scale() * self.get_serial_scale()

    def get_open_circuit_voltage(self, battery_state: LithiumIonState) -> float:
        soc = battery_state.soc
        # temperature window limited between 5°C and 35°C due to test conditions
        if battery_state.temperature > 308.15:
            temperature: float = 308.15
            self.__log.warn("The cell OCV model is only parameterized up to 35°C.")
        elif battery_state.temperature < 278.15:
            temperature: float = 278.15
            self.__log.warn("The cell OCV model is only parameterized down to 5°C.")
        else:
            temperature: float = battery_state.temperature
        # new poly7 values for given temperature
        poly7_data_new = self.__poly7_values_interp(temperature)
        soc_percent = 100 * soc
        ocv = poly7_data_new[0] * soc_percent ** 7 + poly7_data_new[1] * soc_percent ** 6 \
              + poly7_data_new[2] * soc_percent ** 5 + poly7_data_new[3] * soc_percent ** 4 \
              + poly7_data_new[4] * soc_percent ** 3 + poly7_data_new[5] * soc_percent ** 2 \
              + poly7_data_new[6] * soc_percent + poly7_data_new[7]
        return ocv * self.get_serial_scale()

    def get_capacity(self, battery_state: LithiumIonState) -> float:
        return self.get_nominal_capacity()

    def close(self):
        self.__log.close()
