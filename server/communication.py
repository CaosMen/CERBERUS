from serial import Serial, SerialException

from logger import print_log

from utils.ports import serial_ports

from config import (
    SERIAL_PORT,
    SERIAL_BAUDRATE
)


class Communication:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Communication, cls).__new__(cls)

            cls.port = SERIAL_PORT
            cls.baudrate = SERIAL_BAUDRATE
            cls.serial_connection = None

        return cls._instance

    def connect(self) -> bool:
        try:
            if not self.serial_connection:
                self.serial_connection = Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                )

            print_log("info", f"Connection established with serial port: {self.port}.")

            return True

        except SerialException as e:
            print_log("error", f"Error connecting to serial port: {self.port}.")
            print_log("error", f"Error: {e}.")

            self.handle_serial_exception()

            return False

    def handle_serial_exception(self) -> None:
        serial_ports_available = serial_ports()

        if len(serial_ports_available) == 0:
            print_log("error", "No serial ports available.")
            return

        print_log("info", "Use one of the following available ports:")
        print_log("info", ", ".join(serial_ports_available))

    def write(self, data: str) -> None:
        if not self.serial_connection:
            print_log("error", "Serial connection not established.")
            return

        self.serial_connection.write(data.encode("utf-8"))

    def readline(self) -> str:
        if not self.serial_connection:
            print_log("error", "Serial connection not established.")
            return ""

        return self.serial_connection.readline().decode("utf-8").strip()
