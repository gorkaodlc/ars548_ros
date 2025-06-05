import ctypes
from ars548_messages.msg import Status, Detection, DetectionList, Object, ObjectList

ARS548_MAX_DETECTIONS = 800
ARS548_MAX_OBJECTS = 50
STATUS_MESSAGE_METHOD_ID = 380
STATUS_MESSAGE_PDU_LENGTH = 76
DETECTION_MESSAGE_METHOD_ID = 336
DETECTION_MESSAGE_PDU_LENGTH = 35328
OBJECT_MESSAGE_METHOD_ID = 329
OBJECT_MESSAGE_PDU_LENGTH = 9393
STATUS_MESSAGE_PAYLOAD = 84
DETECTION_MESSAGE_PAYLOAD = 35336
OBJECT_MESSAGE_PAYLOAD = 9401

class UDPStatus(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("ServiceID", ctypes.c_uint16),
        ("MethodID", ctypes.c_uint16),
        ("PayloadLength", ctypes.c_uint32),
        ("Timestamp_Nanoseconds", ctypes.c_uint32),
        ("Timestamp_Seconds", ctypes.c_uint32),
        ("Timestamp_SyncStatus", ctypes.c_uint8),
        ("SWVersion_Major", ctypes.c_uint8),
        ("SWVersion_Minor", ctypes.c_uint8),
        ("SWVersion_Patch", ctypes.c_uint8),
        ("Longitudinal", ctypes.c_float),
        ("Lateral", ctypes.c_float),
        ("Vertical", ctypes.c_float),
        ("Yaw", ctypes.c_float),
        ("Pitch", ctypes.c_float),
        ("PlugOrientation", ctypes.c_uint8),
        ("Length", ctypes.c_float),
        ("Width", ctypes.c_float),
        ("Height", ctypes.c_float),
        ("Wheelbase", ctypes.c_float),
        ("MaximumDistance", ctypes.c_uint16),
        ("FrequencySlot", ctypes.c_uint8),
        ("CycleTime", ctypes.c_uint8),
        ("TimeSlot", ctypes.c_uint8),
        ("HCC", ctypes.c_uint8),
        ("Powersave_Standstill", ctypes.c_uint8),
        ("SensorIPAddress_0", ctypes.c_uint32),
        ("SensorIPAddress_1", ctypes.c_uint32),
        ("ConfigurationCounter", ctypes.c_uint8),
        ("Status_LongitudinalVelocity", ctypes.c_uint8),
        ("Status_LongitudinalAcceleration", ctypes.c_uint8),
        ("Status_LateralAcceleration", ctypes.c_uint8),
        ("Status_YawRate", ctypes.c_uint8),
        ("Status_SteeringAngle", ctypes.c_uint8),
        ("Status_DrivingDirection", ctypes.c_uint8),
        ("Status_CharacteristicSpeed", ctypes.c_uint8),
        ("Status_RadarStatus", ctypes.c_uint8),
        ("Status_VoltageStatus", ctypes.c_uint8),
        ("Status_TemperatureStatus", ctypes.c_uint8),
        ("Status_BlockageStatus", ctypes.c_uint8),
    ]

    def to_ros(self) -> Status:
        msg = Status()
        for name, _ in self._fields_:
            attr = name.lower()
            if hasattr(msg, attr):
                setattr(msg, attr, getattr(self, name))
        return msg

    def is_valid(self) -> bool:
        return self.MethodID == STATUS_MESSAGE_METHOD_ID and self.PayloadLength == STATUS_MESSAGE_PDU_LENGTH

class Detection(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("f_AzimuthAngle", ctypes.c_float),
        ("f_AzimuthAngleSTD", ctypes.c_float),
        ("u_InvalidFlags", ctypes.c_uint8),
        ("f_ElevationAngle", ctypes.c_float),
        ("f_ElevationAngleSTD", ctypes.c_float),
        ("f_Range", ctypes.c_float),
        ("f_RangeSTD", ctypes.c_float),
        ("f_RangeRate", ctypes.c_float),
        ("f_RangeRateSTD", ctypes.c_float),
        ("s_RCS", ctypes.c_int8),
        ("u_MeasurementID", ctypes.c_uint16),
        ("u_PositivePredictiveValue", ctypes.c_uint8),
        ("u_Classification", ctypes.c_uint8),
        ("u_MultiTargetProbabilityM", ctypes.c_uint8),
        ("u_ObjectID", ctypes.c_uint16),
        ("u_AmbiguityFlag", ctypes.c_uint8),
        ("u_SortIndex", ctypes.c_uint16),
    ]

    def to_ros(self) -> Detection:
        msg = Detection()
        for name, _ in self._fields_:
            setattr(msg, name.lower(), getattr(self, name))
        return msg

class DetectionListHeader(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("ServiceID", ctypes.c_uint16),
        ("MethodID", ctypes.c_uint16),
        ("PayloadLength", ctypes.c_uint32),
        ("empty1", ctypes.c_int64),
        ("CRC", ctypes.c_uint64),
        ("Length", ctypes.c_uint32),
        ("SQC", ctypes.c_uint32),
        ("DataID", ctypes.c_uint32),
        ("Timestamp_Nanoseconds", ctypes.c_uint32),
        ("Timestamp_Seconds", ctypes.c_uint32),
        ("Timestamp_SyncStatus", ctypes.c_uint8),
        ("EventDataQualifier", ctypes.c_uint32),
        ("ExtendedQualifier", ctypes.c_uint8),
        ("Origin_InvalidFlags", ctypes.c_uint16),
        ("Origin_Xpos", ctypes.c_float),
        ("Origin_Xstd", ctypes.c_float),
        ("Origin_Ypos", ctypes.c_float),
        ("Origin_Ystd", ctypes.c_float),
        ("Origin_Zpos", ctypes.c_float),
        ("Origin_Zstd", ctypes.c_float),
        ("Origin_Roll", ctypes.c_float),
        ("Origin_Rollstd", ctypes.c_float),
        ("Origin_Pitch", ctypes.c_float),
        ("Origin_Pitchstd", ctypes.c_float),
        ("Origin_Yaw", ctypes.c_float),
        ("Origin_Yawstd", ctypes.c_float),
        ("List_InvalidFlags", ctypes.c_uint8),
    ]

class DetectionList(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("hdr", DetectionListHeader),
        ("List_Detections", Detection * ARS548_MAX_DETECTIONS),
        ("List_RadVelDomain_Min", ctypes.c_float),
        ("List_RadVelDomain_Max", ctypes.c_float),
        ("List_NumOfDetections", ctypes.c_uint32),
        ("Aln_AzimuthCorrection", ctypes.c_float),
        ("Aln_ElevationCorrection", ctypes.c_float),
        ("Aln_Status", ctypes.c_uint8),
    ]

    def to_ros(self, frame_id: str, override: bool, clock) -> DetectionList:
        msg = DetectionList()
        msg.header.frame_id = frame_id
        if override:
            msg.header.stamp = clock.now().to_msg()
        else:
            msg.header.stamp.sec = self.hdr.Timestamp_Seconds
            msg.header.stamp.nanosec = self.hdr.Timestamp_Nanoseconds
        msg.crc = self.hdr.CRC
        msg.length = self.hdr.Length
        msg.sqc = self.hdr.SQC
        msg.dataid = self.hdr.DataID
        msg.timestamp_nanoseconds = self.hdr.Timestamp_Nanoseconds
        msg.timestamp_seconds = self.hdr.Timestamp_Seconds
        msg.timestamp_syncstatus = self.hdr.Timestamp_SyncStatus
        msg.eventdataqualifier = self.hdr.EventDataQualifier
        msg.extendedqualifier = self.hdr.ExtendedQualifier
        msg.origin_invalidflags = self.hdr.Origin_InvalidFlags
        msg.origin_xpos = self.hdr.Origin_Xpos
        msg.origin_xstd = self.hdr.Origin_Xstd
        msg.origin_ypos = self.hdr.Origin_Ypos
        msg.origin_ystd = self.hdr.Origin_Ystd
        msg.origin_zpos = self.hdr.Origin_Zpos
        msg.origin_zstd = self.hdr.Origin_Zstd
        msg.origin_roll = self.hdr.Origin_Roll
        msg.origin_rollstd = self.hdr.Origin_Rollstd
        msg.origin_pitch = self.hdr.Origin_Pitch
        msg.origin_pitchstd = self.hdr.Origin_Pitchstd
        msg.origin_yaw = self.hdr.Origin_Yaw
        msg.origin_yawstd = self.hdr.Origin_Yawstd
        count = min(self.List_NumOfDetections, ARS548_MAX_DETECTIONS)
        msg.list_numofdetections = count
        for i in range(count):
            msg.list_detections[i] = self.List_Detections[i].to_ros()
        msg.list_radveldomain_min = self.List_RadVelDomain_Min
        msg.list_radveldomain_max = self.List_RadVelDomain_Max
        msg.aln_azimuthcorrection = self.Aln_AzimuthCorrection
        msg.aln_elevationcorrection = self.Aln_ElevationCorrection
        msg.aln_status = self.Aln_Status
        return msg

    def is_valid(self) -> bool:
        return self.hdr.MethodID == DETECTION_MESSAGE_METHOD_ID and self.hdr.PayloadLength == DETECTION_MESSAGE_PDU_LENGTH

class Object(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('u_StatusSensor', ctypes.c_uint16),
        ('u_ID', ctypes.c_uint32),
        ('u_Age', ctypes.c_uint16),
        ('u_StatusMeasurement', ctypes.c_uint8),
        ('u_StatusMovement', ctypes.c_uint8),
        ('u_Position_InvalidFlags', ctypes.c_uint16),
        ('u_Position_Reference', ctypes.c_uint8),
        ('u_Position_X', ctypes.c_float),
        ('u_Position_X_STD', ctypes.c_float),
        ('u_Position_Y', ctypes.c_float),
        ('u_Position_Y_STD', ctypes.c_float),
        ('u_Position_Z', ctypes.c_float),
        ('u_Position_Z_STD', ctypes.c_float),
        ('u_Position_CovarianceXY', ctypes.c_float),
        ('u_Position_Orientation', ctypes.c_float),
        ('u_Position_Orientation_STD', ctypes.c_float),
        ('u_Existence_InvalidFlags', ctypes.c_uint8),
        ('u_Existence_Probability', ctypes.c_float),
        ('u_Existence_PPV', ctypes.c_float),
        ('u_Classification_Car', ctypes.c_uint8),
        ('u_Classification_Truck', ctypes.c_uint8),
        ('u_Classification_Motorcycle', ctypes.c_uint8),
        ('u_Classification_Bicycle', ctypes.c_uint8),
        ('u_Classification_Pedestrian', ctypes.c_uint8),
        ('u_Classification_Animal', ctypes.c_uint8),
        ('u_Classification_Hazard', ctypes.c_uint8),
        ('u_Classification_Unknown', ctypes.c_uint8),
        ('u_Classification_Overdrivable', ctypes.c_uint8),
        ('u_Classification_Underdrivable', ctypes.c_uint8),
        ('u_Dynamics_AbsVel_InvalidFlags', ctypes.c_uint8),
        ('f_Dynamics_AbsVel_X', ctypes.c_float),
        ('f_Dynamics_AbsVel_X_STD', ctypes.c_float),
        ('f_Dynamics_AbsVel_Y', ctypes.c_float),
        ('f_Dynamics_AbsVel_Y_STD', ctypes.c_float),
        ('f_Dynamics_AbsVel_CovarianceXY', ctypes.c_float),
        ('u_Dynamics_RelVel_InvalidFlags', ctypes.c_uint8),
        ('f_Dynamics_RelVel_X', ctypes.c_float),
        ('f_Dynamics_RelVel_X_STD', ctypes.c_float),
        ('f_Dynamics_RelVel_Y', ctypes.c_float),
        ('f_Dynamics_RelVel_Y_STD', ctypes.c_float),
        ('f_Dynamics_RelVel_CovarianceXY', ctypes.c_float),
        ('u_Dynamics_AbsAccel_InvalidFlags', ctypes.c_uint8),
        ('f_Dynamics_AbsAccel_X', ctypes.c_float),
        ('f_Dynamics_AbsAccel_X_STD', ctypes.c_float),
        ('f_Dynamics_AbsAccel_Y', ctypes.c_float),
        ('f_Dynamics_AbsAccel_Y_STD', ctypes.c_float),
        ('f_Dynamics_AbsAccel_CovarianceXY', ctypes.c_float),
        ('u_Dynamics_RelAccel_InvalidFlags', ctypes.c_uint8),
        ('f_Dynamics_RelAccel_X', ctypes.c_float),
        ('f_Dynamics_RelAccel_X_STD', ctypes.c_float),
        ('f_Dynamics_RelAccel_Y', ctypes.c_float),
        ('f_Dynamics_RelAccel_Y_STD', ctypes.c_float),
        ('f_Dynamics_RelAccel_CovarianceXY', ctypes.c_float),
        ('u_Dynamics_Orientation_InvalidFlags', ctypes.c_uint8),
        ('u_Dynamics_Orientation_Rate_Mean', ctypes.c_float),
        ('u_Dynamics_Orientation_Rate_STD', ctypes.c_float),
        ('u_Shape_Length_Status', ctypes.c_uint32),
        ('u_Shape_Length_Edge_InvalidFlags', ctypes.c_uint8),
        ('u_Shape_Length_Edge_Mean', ctypes.c_float),
        ('u_Shape_Length_Edge_STD', ctypes.c_float),
        ('u_Shape_Width_Status', ctypes.c_uint32),
        ('u_Shape_Width_Edge_InvalidFlags', ctypes.c_uint8),
        ('u_Shape_Width_Edge_Mean', ctypes.c_float),
        ('u_Shape_Width_Edge_STD', ctypes.c_float),
    ]

    def to_ros(self) -> Object:
        msg = Object()
        for name, _ in self._fields_:
            setattr(msg, name.lower(), getattr(self, name))
        return msg

class ObjectListHeader(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('ServiceID', ctypes.c_uint16),
        ('MethodID', ctypes.c_uint16),
        ('PayloadLength', ctypes.c_uint32),
        ('empty1', ctypes.c_uint64),
        ('CRC', ctypes.c_uint64),
        ('Length', ctypes.c_uint32),
        ('SQC', ctypes.c_uint32),
        ('DataID', ctypes.c_uint32),
        ('Timestamp_Nanoseconds', ctypes.c_uint32),
        ('Timestamp_Seconds', ctypes.c_uint32),
        ('Timestamp_SyncStatus', ctypes.c_uint8),
        ('EventDataQualifier', ctypes.c_uint32),
        ('ExtendedQualifier', ctypes.c_uint8),
        ('ObjectList_NumOfObjects', ctypes.c_uint8),
    ]

class ObjectList(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('hdr', ObjectListHeader),
        ('ObjectList_Objects', Object * ARS548_MAX_OBJECTS),
    ]

    def to_ros(self, frame_id: str, override: bool, clock) -> ObjectList:
        msg = ObjectList()
        msg.header.frame_id = frame_id
        if override:
            msg.header.stamp = clock.now().to_msg()
        else:
            msg.header.stamp.sec = self.hdr.Timestamp_Seconds
            msg.header.stamp.nanosec = self.hdr.Timestamp_Nanoseconds
        msg.crc = self.hdr.CRC
        msg.length = self.hdr.Length
        msg.sqc = self.hdr.SQC
        msg.dataid = self.hdr.DataID
        msg.timestamp_nanoseconds = self.hdr.Timestamp_Nanoseconds
        msg.timestamp_seconds = self.hdr.Timestamp_Seconds
        msg.timestamp_syncstatus = self.hdr.Timestamp_SyncStatus
        msg.eventdataqualifier = self.hdr.EventDataQualifier
        msg.extendedqualifier = self.hdr.ExtendedQualifier
        count = min(self.hdr.ObjectList_NumOfObjects, ARS548_MAX_OBJECTS)
        msg.objectlist_numofobjects = count
        for i in range(count):
            msg.objectlist_objects[i] = self.ObjectList_Objects[i].to_ros()
        return msg

    def is_valid(self) -> bool:
        return self.hdr.MethodID == OBJECT_MESSAGE_METHOD_ID and self.hdr.PayloadLength == OBJECT_MESSAGE_PDU_LENGTH
