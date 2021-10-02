#!/usr/bin/env python3
import time
import sys
import serial
import argparse 

import socket

from serial.threaded import LineReader, ReaderThread

parser = argparse.ArgumentParser(description='LoRa Radio mode receiver.')
parser.add_argument('port', help="Serial port descriptor")
args = parser.parse_args()

s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, 0)
s.bind(("lo", 0))

class PrintLines(LineReader):

    def write_to_socket(self, packet):
        import socket

    def connection_made(self, transport):
        print("connection made")
        self.transport = transport
        self.send_cmd('sys get ver')
        self.send_cmd('mac pause')
        self.send_cmd('radio set pwr 10')
        self.send_cmd('radio rx 0')
        self.send_cmd("sys set pindig GPIO10 0")

    def handle_line(self, data):
        if data == "ok" or data == 'busy':
            return
        if data == "radio_err":
            self.send_cmd('radio rx 0')
            return
        
        self.send_cmd("sys set pindig GPIO10 1", delay=0)
        if data.find("radio_rx") == 0:
          data = data.split(' ', 1)[1].strip()
          # s.send(data.decode("hex"))
          print data.decode("hex")
        time.sleep(.1)
        self.send_cmd("sys set pindig GPIO10 0", delay=1)
        self.send_cmd('radio rx 0')

    def connection_lost(self, exc):
        if exc:
            print(exc)
        print("port closed")

    def send_cmd(self, cmd, delay=.5):
        self.transport.write(('%s\r\n' % cmd).encode('UTF-8'))
        time.sleep(delay)

ser = serial.Serial(args.port, baudrate=57600)
with ReaderThread(ser, PrintLines) as protocol:
    while(1):
        pass
