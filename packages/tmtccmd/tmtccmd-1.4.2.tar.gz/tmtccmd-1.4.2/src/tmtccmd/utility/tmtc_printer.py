#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
"""
@file
    tmtcc_config.py
@date
    01.11.2019
@brief
    Class that performs all printing functionalities
"""
import os
import enum

from tmtccmd.ecss.tc import PusTelecommand
from tmtccmd.ecss.tm import PusTelemetry
from tmtccmd.pus_tm.service_8_functional_cmd import Service8TM
from tmtccmd.pus_tm.factory import PusTmQueueT
from tmtccmd.pus_tm.service_3_base import Service3Base
from tmtccmd.utility.tmtcc_logger import get_logger

LOGGER = get_logger()


class DisplayMode(enum.Enum):
    """ List of display modes """
    SHORT = enum.auto()
    LONG = enum.auto()


class TmTcPrinter:
    """
    This class handles printing to the command line and to files.
    """
    def __init__(self, display_mode: DisplayMode.LONG, do_print_to_file: bool = True,
                 print_tc: bool = True):
        """
        :param display_mode:
        :param do_print_to_file: if true, print to file
        :param print_tc: if true, print TCs
        """
        self.display_mode = display_mode
        self.do_print_to_file = do_print_to_file
        self.print_tc = print_tc
        self.__print_buffer = ""
        # global print buffer which will be useful to print something to file
        self.__file_buffer = ""
        # TODO: Full print not working yet
        # List implementation to store multiple strings
        self.file_buffer_list = []

    def set_display_mode(self, display_mode: DisplayMode):
        self.display_mode = display_mode

    def print_telemetry_queue(self, tm_queue: PusTmQueueT):
        """
        Print the telemetry queue which should contain lists of TM class instances.
        """
        for tm_list in tm_queue:
            for tm_packet in tm_list:
                self.print_telemetry(tm_packet)

    def print_telemetry(self, packet: PusTelemetry):
        """
        This function handles printing telemetry
        :param packet:
        :return:
        """
        if not isinstance(packet, PusTelemetry):
            LOGGER.warning("Passed packet is not instance of PusTelemetry!")
            return
        # LOGGER.debug(packet.return_full_packet_string())
        if self.display_mode == DisplayMode.SHORT:
            self.__handle_short_print(packet)
        else:
            self.__handle_long_tm_print(packet)
        self.__handle_wiretapping_packet(packet)

        # Handle special packet types
        if packet.get_service() == 8 and packet.get_subservice() == 130:
            from typing import cast
            self.__handle_data_reply_packet(cast(Service8TM, packet))
        if packet.get_service() == 3 and \
                (packet.get_subservice() == 25 or packet.get_subservice() == 26):
            from typing import cast
            self.__handle_hk_print(cast(Service3Base, packet))
        if packet.get_service() == 3 and \
                (packet.get_subservice() == 10 or packet.get_subservice() == 12):
            from typing import cast
            self.__handle_hk_definition_print(cast(Service3Base, packet))

        from tmtccmd.core.globals_manager import get_global
        from tmtccmd.core.definitions import CoreGlobalIds
        if get_global(CoreGlobalIds.PRINT_RAW_TM):
            self.__print_buffer = "TM Data:" + "\n" + self.return_data_string(packet.get_tm_data())
            LOGGER.info(self.__print_buffer)
            self.add_print_buffer_to_file_buffer()

    def __handle_short_print(self, tm_packet: PusTelemetry):
        self.__print_buffer = "Received TM[" + str(tm_packet.get_service()) + "," + str(
            tm_packet.get_subservice()) + "]"
        LOGGER.info(self.__print_buffer)
        self.add_print_buffer_to_file_buffer()

    def __handle_long_tm_print(self, tm_packet: PusTelemetry):
        """
        Main function to print the most important information inside the telemetry
        :param tm_packet:
        :return:
        """
        self.__print_buffer = "Received Telemetry: " + tm_packet.print_info
        LOGGER.info(self.__print_buffer)
        self.add_print_buffer_to_file_buffer()
        try:
            self.__handle_column_header_print(tm_packet)
            self.__handle_tm_content_print(tm_packet)
            self.__handle_additional_printout(tm_packet)
        except TypeError as error:
            LOGGER.warning(f"Type Error when trying to print TM Packet"
                           f" [{tm_packet.get_service()} , {tm_packet.get_subservice()}]")
            LOGGER.warning(error)

    def __handle_column_header_print(self, tm_packet: PusTelemetry):
        header_list = []
        tm_packet.append_telemetry_column_headers(header_list=header_list)
        self.__print_buffer = str(header_list)
        LOGGER.info(self.__print_buffer)
        self.add_print_buffer_to_file_buffer()

    def __handle_tm_content_print(self, tm_packet: PusTelemetry):
        """
        :param tm_packet:
        :return:
        """
        content_list = []
        tm_packet.append_telemetry_content(content_list=content_list)
        self.__print_buffer = str(content_list)
        LOGGER.info(self.__print_buffer)
        self.add_print_buffer_to_file_buffer()

    def __handle_additional_printout(self, tm_packet: PusTelemetry):
        additional_printout = tm_packet.get_custom_printout()
        if additional_printout != "":
            self.__print_buffer = additional_printout
            LOGGER.info(self.__print_buffer)

    def __handle_hk_print(self, tm_packet: Service3Base):
        """
        Prints HK _tm_data previously set by TM receiver
        :param tm_packet:
        :return:
        """
        from tmtccmd.core.globals_manager import get_global
        from tmtccmd.core.definitions import CoreGlobalIds
        print_hk = get_global(CoreGlobalIds.PRINT_HK)
        if print_hk:
            self.__print_buffer = f"HK Data from Object ID {tm_packet.object_id:#010x} and " \
                                  f"set ID {tm_packet.set_id}:"
            self.__print_hk(tm_packet)
            self.__print_validity_buffer(tm_packet)

    def __handle_hk_definition_print(self, tm_packet: Service3Base):
        """
        :param tm_packet:
        :return:
        """
        from tmtccmd.core.globals_manager import get_global
        from tmtccmd.core.definitions import CoreGlobalIds
        print_hk = get_global(CoreGlobalIds.PRINT_HK)
        if print_hk:
            self.__print_buffer = f"HK Definition from Object ID {tm_packet.object_id:#010x} " \
                                  f"and set ID {tm_packet.set_id}:"
            self.__print_hk(tm_packet)

    def __print_hk(self, tm_packet: Service3Base):
        """
        :param tm_packet:
        :return:
        """
        if not isinstance(tm_packet.hk_content, list):
            LOGGER.error("Invalid HK content format! Needs to be list.")
            return
        if len(tm_packet.hk_content) == 0:
            return

        LOGGER.info(self.__print_buffer)
        self.add_print_buffer_to_file_buffer()
        self.__print_buffer = str(tm_packet.hk_header)
        LOGGER.info(self.__print_buffer)
        self.add_print_buffer_to_file_buffer()
        self.__print_buffer = str(tm_packet.hk_content)
        LOGGER.info(self.__print_buffer)
        self.add_print_buffer_to_file_buffer()

    def __print_validity_buffer(self, tm_packet: Service3Base):
        """
        :param tm_packet:
        :return:
        """
        if len(tm_packet.validity_buffer) == 0:
            return
        self.__print_buffer = "Valid: "
        LOGGER.info(self.__print_buffer)
        self.add_print_buffer_to_file_buffer()
        self.__handle_validity_buffer_print(
            tm_packet.validity_buffer, tm_packet.number_of_parameters
        )

    def __handle_validity_buffer_print(self, validity_buffer: bytearray, number_of_parameters):
        """
        :param validity_buffer:
        :param number_of_parameters:
        :return:
        """
        self.__print_buffer = "["
        counter = 0
        for index, byte in enumerate(validity_buffer):
            for bit in range(1, 9):
                if self.bit_extractor(byte, bit) == 1:
                    self.__print_buffer = self.__print_buffer + "Yes"
                else:
                    self.__print_buffer = self.__print_buffer + "No"
                counter += 1
                if counter == number_of_parameters:
                    self.__print_buffer = self.__print_buffer + "]"
                    break
                self.__print_buffer = self.__print_buffer + ", "
        LOGGER.info(self.__print_buffer)
        self.add_print_buffer_to_file_buffer()

    def __handle_wiretapping_packet(self, wiretapping_packet: PusTelemetry):
        """
        :param wiretapping_packet:
        :return:
        """
        if wiretapping_packet.get_service() == 2 and (wiretapping_packet.get_subservice() == 131 or
                                                      wiretapping_packet.get_subservice() == 130):
            self.__print_buffer = "Wiretapping Packet or Raw Reply from TM [" + \
                                  str(wiretapping_packet.get_service()) + "," + \
                                  str(wiretapping_packet.get_subservice()) + "]: "
            self.__print_buffer = self.__print_buffer + wiretapping_packet.return_source_data()
            LOGGER.info(self.__print_buffer)
            self.add_print_buffer_to_file_buffer()

    def __handle_data_reply_packet(self, srv8_tm: Service8TM):
        """
        Handles the PUS Service 8 data reply types.
        :return:
        """
        try:
            if srv8_tm.custom_data_content is [] or srv8_tm.custom_data_header is []:
                self.__print_buffer = f"Service 8 Direct Command Reply TM[8,130] with TM data: " \
                                      f"{srv8_tm.return_source_data()}"
            else:
                self.__print_buffer = f"{srv8_tm.custom_data_header}{os.linesep}"
                self.__print_buffer += f"{srv8_tm.custom_data_content}{os.linesep}"
                LOGGER.info(f"Service 8 data for object ID {srv8_tm.object_id_key} "
                            f"and action ID {srv8_tm.source_action_id}:")
                LOGGER.info(str(srv8_tm.custom_data_header))
                LOGGER.info(str(srv8_tm.custom_data_content))
            self.add_print_buffer_to_file_buffer()
        except AttributeError:
            LOGGER.warning("Service 8 packet format invalid, no custom_data_content or custom_data_header found!")
            return

    def print_string(self, string: str, add_cr_to_file_buffer: bool = False):
        """
        Print a string and adds it to the file buffer.
        :param string:
        :param add_cr_to_file_buffer:
        :return:
        """
        self.__print_buffer = string
        LOGGER.info(self.__print_buffer)
        if self.do_print_to_file:
            self.add_print_buffer_to_file_buffer(add_cr_to_file_buffer)

    def add_to_print_string(self, string_to_add: str = ""):
        """ Add a specific string to the current print buffer """
        self.__print_buffer += string_to_add

    def add_print_buffer_to_file_buffer(self, add_cr_to_file_buffer: bool = False,
                                        cr_before: bool = True):
        """
        Add to file buffer. Some options to optimize the output.
        """
        if self.do_print_to_file:
            if add_cr_to_file_buffer:
                if cr_before:
                    self.__file_buffer += "\r\n" + self.__print_buffer + "\r\n"
                else:
                    self.__file_buffer += self.__print_buffer + "\r\n\r\n"
            else:
                self.__file_buffer += self.__print_buffer + "\r\n"

    def add_print_buffer_to_buffer_list(self):
        """ Add the current print buffer to the buffer list """
        self.file_buffer_list.append(self.__file_buffer)

    def clear_file_buffer(self):
        """ Clears the file buffer """
        self.__file_buffer = ""

    def print_to_file(self, log_name: str = "log/tmtc_log.txt", clear_file_buffer: bool = False):
        """
        :param log_name:
        :param clear_file_buffer:
        :return:
        """
        try:
            file = open(log_name, 'w')
        except FileNotFoundError:
            LOGGER.info("Log directory does not exists, creating log folder.")
            os.mkdir('log')
            file = open(log_name, 'w')
        file.write(self.__file_buffer)
        if clear_file_buffer:
            self.__file_buffer = ""
        LOGGER.info("Log file written to %s", log_name)
        file.close()

    def print_file_buffer_list_to_file(self, log_name: str = "log/tmtc_log.txt",
                                       clear_list: bool = True):
        """
        Joins the string list and prints it to an output file.
        :param log_name:
        :param clear_list:
        :return:
        """
        try:
            file = open(log_name, 'w')
        except FileNotFoundError:
            LOGGER.info("Log directory does not exists, creating log folder.")
            os.mkdir('log')
            file = open(log_name, 'w')
        file_buffer = ''.join(self.file_buffer_list)
        file.write(file_buffer)
        if clear_list:
            self.file_buffer_list = []
        LOGGER.info("Log file written to %s", log_name)
        file.close()

    @staticmethod
    def bit_extractor(byte: int, position: int):
        """

        :param byte:
        :param position:
        :return:
        """
        shift_number = position + (6 - 2 * (position - 1))
        return (byte >> shift_number) & 1

    def print_telecommand(self, tc_packet: bytes, tc_packet_obj: PusTelecommand = None):
        """
        This function handles the printing of Telecommands
        :param tc_packet:
        :param tc_packet_obj:
        :return:
        """
        if self.print_tc:
            if len(tc_packet) == 0:
                LOGGER.error("TMTC Printer: Empty packet was sent, configuration error")
                return
            if tc_packet_obj is None:
                return
            if self.display_mode == DisplayMode.SHORT:
                self.__handle_short_tc_print(tc_packet_obj=tc_packet_obj)
            else:
                self.__handle_long_tc_print(tc_packet_obj=tc_packet_obj)

    def __handle_short_tc_print(self, tc_packet_obj: PusTelecommand):
        """
        Brief TC print
        :param tc_packet_obj:
        :return:
        """
        self.__print_buffer = \
            f"Sent TC[{tc_packet_obj.get_service()}, {tc_packet_obj.get_subservice()}] with SSC " \
            f"{tc_packet_obj.get_ssc()}"
        LOGGER.info(self.__print_buffer)
        self.add_print_buffer_to_file_buffer()

    def __handle_long_tc_print(self, tc_packet_obj: PusTelecommand):
        """
        Long TC print
        :param tc_packet_obj:
        :return:
        """
        try:
            self.__print_buffer = \
                f"Telecommand TC[{tc_packet_obj.get_service()}, {tc_packet_obj.get_subservice()}] " \
                f"with SSC {tc_packet_obj.get_ssc()} sent with data " \
                f"{self.return_data_string(tc_packet_obj.get_app_data())}"
            LOGGER.info(self.__print_buffer)
            self.add_print_buffer_to_file_buffer()
        except TypeError as error:
            LOGGER.error("TMTC Printer: Type Error! Traceback: %s", error)

    def print_data(self, byte_array: bytearray):
        """
        :param byte_array:
        :return: None
        """
        string = self.return_data_string(byte_array)
        LOGGER.info(string)

    @staticmethod
    def return_data_string(byte_array: bytearray) -> str:
        """
        Converts a bytearray to string format for printing
        :param byte_array:
        :return:
        """
        str_to_print = "["
        for byte in byte_array:
            str_to_print += str(hex(byte)) + " , "
        str_to_print = str_to_print.rstrip(' ')
        str_to_print = str_to_print.rstrip(',')
        str_to_print += ']'
        return str_to_print
