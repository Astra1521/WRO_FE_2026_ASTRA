# -*- coding: UTF-8 -*-

import smbus
import time

TOF_ADDR = 0x08

TOF_REGISTER_TOTAL_SIZE = 48

TOF_ADDR_MODE = 0x0C
TOF_ADDR_ID = 0x0D
TOF_ADDR_UART_BAUDRATE = 0x10
TOF_ADDR_SYSTEM_TIME = 0x20
TOF_ADDR_DIS = 0x24
TOF_ADDR_DIS_STATUS = 0x28
TOF_ADDR_SIGNAL_STRENGTH = 0x2A
TOF_ADDR_RANGE_PRECISION = 0x2C


class TOF_Sense:

    def __init__(self, bus=1):
        self.bus = smbus.SMBus(bus)
        self.last_distance = None
        self.last_strength = None
        self.last_status = None

    def read_block(self, reg, length):
        return self.bus.read_i2c_block_data(TOF_ADDR, reg, length)

    def write_byte(self, reg, value):
        self.bus.write_i2c_block_data(TOF_ADDR, reg, [value & 0xFF])

    def read_frame(self):
        """
        Read the complete sensor register map.
        """

        data1 = self.read_block(0x00, 24)
        data2 = self.read_block(0x18, 24)

        return data1 + data2

    def decode(self, pdata):

        info = {}

        info["mode"] = pdata[TOF_ADDR_MODE] & 0x07

        info["id"] = pdata[TOF_ADDR_ID]

        info["baudrate"] = (
            pdata[TOF_ADDR_UART_BAUDRATE]
            | (pdata[TOF_ADDR_UART_BAUDRATE + 1] << 8)
            | (pdata[TOF_ADDR_UART_BAUDRATE + 2] << 16)
            | (pdata[TOF_ADDR_UART_BAUDRATE + 3] << 24)
        )

        info["system_time"] = (
            pdata[TOF_ADDR_SYSTEM_TIME]
            | (pdata[TOF_ADDR_SYSTEM_TIME + 1] << 8)
            | (pdata[TOF_ADDR_SYSTEM_TIME + 2] << 16)
            | (pdata[TOF_ADDR_SYSTEM_TIME + 3] << 24)
        )

        info["distance"] = (
            pdata[TOF_ADDR_DIS]
            | (pdata[TOF_ADDR_DIS + 1] << 8)
            | (pdata[TOF_ADDR_DIS + 2] << 16)
            | (pdata[TOF_ADDR_DIS + 3] << 24)
        )

        info["status"] = (
            pdata[TOF_ADDR_DIS_STATUS]
            | (pdata[TOF_ADDR_DIS_STATUS + 1] << 8)
        )

        info["strength"] = (
            pdata[TOF_ADDR_SIGNAL_STRENGTH]
            | (pdata[TOF_ADDR_SIGNAL_STRENGTH + 1] << 8)
        )

        info["precision"] = pdata[TOF_ADDR_RANGE_PRECISION]

        return info

    def get_data(self, retries=3):

        for _ in range(retries):

            try:

                pdata = self.read_frame()

                info = self.decode(pdata)

                if info["status"] == 1:

                    self.last_distance = info["distance"]
                    self.last_strength = info["strength"]
                    self.last_status = 1

                    return info

                time.sleep(0.003)

            except OSError:
                time.sleep(0.003)

        if self.last_distance is not None:

            return {
                "mode": None,
                "id": None,
                "baudrate": None,
                "system_time": None,
                "distance": self.last_distance,
                "status": 0,
                "strength": self.last_strength,
                "precision": None,
            }

        return None

    def get_distance(self):

        data = self.get_data()

        if data is None:
            return None

        return data["distance"]

    def print_data(self):

        data = self.get_data()

        if data is None:
            print("No valid data")
            return

        print("-----------------------------")
        print("ID:", data["id"])
        print("Distance:", data["distance"], "mm")
        print("Status:", data["status"])
        print("Signal:", data["strength"])
        print("Precision:", data["precision"])
        print("System Time:", data["system_time"])
        print("-----------------------------")

    def IIC_Change_Mode_To_UART(self):
        self.write_byte(0x0C, 0x00)
        print("Mode changed to UART")