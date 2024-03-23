import sys
import glob
import serial

from typing import List


def serial_ports() -> List[str]:
    """
    Function to list serial available ports on the system

    Returns:
        List[str]: List of available serial ports
    """

    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('This platform is not supported!')

    available_ports = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()

            available_ports.append(port)
        except (OSError, serial.SerialException):
            pass

    return available_ports
