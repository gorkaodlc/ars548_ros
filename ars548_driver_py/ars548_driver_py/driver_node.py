import socket
import struct
import ctypes
from threading import Thread

import rclpy
from rclpy.node import Node

from ars548_messages.msg import Status, DetectionList, ObjectList

from .structures import (
    UDPStatus,
    DetectionList as DetectionListStruct,
    ObjectList as ObjectListStruct,
    STATUS_MESSAGE_PAYLOAD,
    DETECTION_MESSAGE_PAYLOAD,
    OBJECT_MESSAGE_PAYLOAD,
)

class Ars548DriverPy(Node):
    def __init__(self):
        super().__init__('ars_548_driver_py')
        self.declare_parameter('localIP', '10.13.1.166')
        self.declare_parameter('radarIP', '10.13.1.113')
        self.declare_parameter('radarPort', 42102)
        self.declare_parameter('frameID', 'ARS_548')
        self.declare_parameter('multicastIP', '224.0.2.2')
        self.declare_parameter('overrideStamp', True)

        self.local_ip = self.get_parameter('localIP').get_parameter_value().string_value
        self.multicast_ip = self.get_parameter('multicastIP').get_parameter_value().string_value
        self.port = self.get_parameter('radarPort').get_parameter_value().integer_value
        self.frame_id = self.get_parameter('frameID').get_parameter_value().string_value
        self.override_stamp = self.get_parameter('overrideStamp').get_parameter_value().bool_value

        self.status_pub = self.create_publisher(Status, 'Status', 10)
        self.object_pub = self.create_publisher(ObjectList, 'ObjectList', 10)
        self.detection_pub = self.create_publisher(DetectionList, 'DetectionList', 10)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.port))
        mreq = struct.pack('=4s4s', socket.inet_aton(self.multicast_ip), socket.inet_aton(self.local_ip))
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.sock.setblocking(False)

        self.thread = Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        while rclpy.ok():
            try:
                data, _ = self.sock.recvfrom(65535)
            except BlockingIOError:
                continue
            nbytes = len(data)
            if nbytes == STATUS_MESSAGE_PAYLOAD:
                status = UDPStatus.from_buffer_copy(data)
                if status.is_valid():
                    self.status_pub.publish(status.to_ros())
            elif nbytes == DETECTION_MESSAGE_PAYLOAD:
                if len(data) >= ctypes.sizeof(DetectionListStruct):
                    det = DetectionListStruct.from_buffer_copy(data[:ctypes.sizeof(DetectionListStruct)])
                    if det.is_valid():
                        msg = det.to_ros(self.frame_id, self.override_stamp, self.get_clock())
                        self.detection_pub.publish(msg)
            elif nbytes == OBJECT_MESSAGE_PAYLOAD:
                if len(data) >= ctypes.sizeof(ObjectListStruct):
                    obj = ObjectListStruct.from_buffer_copy(data[:ctypes.sizeof(ObjectListStruct)])
                    if obj.is_valid():
                        msg = obj.to_ros(self.frame_id, self.override_stamp, self.get_clock())
                        self.object_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Ars548DriverPy()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()

if __name__ == '__main__':
    main()
