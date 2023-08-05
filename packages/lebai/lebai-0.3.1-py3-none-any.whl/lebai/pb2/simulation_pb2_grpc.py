# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import messages_pb2 as messages__pb2
import simulation_pb2 as simulation__pb2


class SimulationControllerStub(object):
    """仿真-离线编程模拟服务
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SetPos = channel.unary_unary(
                '/robotc.SimulationController/SetPos',
                request_serializer=messages__pb2.JPose.SerializeToString,
                response_deserializer=simulation__pb2.SimRes.FromString,
                )
        self.EStop = channel.unary_unary(
                '/robotc.SimulationController/EStop',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=simulation__pb2.SimRes.FromString,
                )
        self.EStopRelease = channel.unary_unary(
                '/robotc.SimulationController/EStopRelease',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=simulation__pb2.SimRes.FromString,
                )
        self.Button = channel.unary_unary(
                '/robotc.SimulationController/Button',
                request_serializer=simulation__pb2.ButtonReq.SerializeToString,
                response_deserializer=simulation__pb2.SimRes.FromString,
                )
        self.SetDialgage = channel.unary_unary(
                '/robotc.SimulationController/SetDialgage',
                request_serializer=simulation__pb2.DialgageReq.SerializeToString,
                response_deserializer=simulation__pb2.SimRes.FromString,
                )
        self.SetRobotAI = channel.unary_unary(
                '/robotc.SimulationController/SetRobotAI',
                request_serializer=messages__pb2.AIO.SerializeToString,
                response_deserializer=simulation__pb2.SimRes.FromString,
                )
        self.SetRobotDI = channel.unary_unary(
                '/robotc.SimulationController/SetRobotDI',
                request_serializer=messages__pb2.DIO.SerializeToString,
                response_deserializer=simulation__pb2.SimRes.FromString,
                )
        self.SetFlangeDI = channel.unary_unary(
                '/robotc.SimulationController/SetFlangeDI',
                request_serializer=messages__pb2.DIO.SerializeToString,
                response_deserializer=simulation__pb2.SimRes.FromString,
                )
        self.ChangeRobotSpeed = channel.unary_unary(
                '/robotc.SimulationController/ChangeRobotSpeed',
                request_serializer=simulation__pb2.RobotSpeed.SerializeToString,
                response_deserializer=simulation__pb2.SimRes.FromString,
                )


class SimulationControllerServicer(object):
    """仿真-离线编程模拟服务
    """

    def SetPos(self, request, context):
        """设置仿真机器人关节角
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EStop(self, request, context):
        """硬件急停
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EStopRelease(self, request, context):
        """释放硬件急停开关
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Button(self, request, context):
        """按下按钮
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetDialgage(self, request, context):
        """设置百分表值
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetRobotAI(self, request, context):
        """设置模拟输入
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetRobotDI(self, request, context):
        """设置数字输入
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetFlangeDI(self, request, context):
        """设置法兰数字输入
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ChangeRobotSpeed(self, request, context):
        """设置仿真机器人运行速度
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SimulationControllerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SetPos': grpc.unary_unary_rpc_method_handler(
                    servicer.SetPos,
                    request_deserializer=messages__pb2.JPose.FromString,
                    response_serializer=simulation__pb2.SimRes.SerializeToString,
            ),
            'EStop': grpc.unary_unary_rpc_method_handler(
                    servicer.EStop,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=simulation__pb2.SimRes.SerializeToString,
            ),
            'EStopRelease': grpc.unary_unary_rpc_method_handler(
                    servicer.EStopRelease,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=simulation__pb2.SimRes.SerializeToString,
            ),
            'Button': grpc.unary_unary_rpc_method_handler(
                    servicer.Button,
                    request_deserializer=simulation__pb2.ButtonReq.FromString,
                    response_serializer=simulation__pb2.SimRes.SerializeToString,
            ),
            'SetDialgage': grpc.unary_unary_rpc_method_handler(
                    servicer.SetDialgage,
                    request_deserializer=simulation__pb2.DialgageReq.FromString,
                    response_serializer=simulation__pb2.SimRes.SerializeToString,
            ),
            'SetRobotAI': grpc.unary_unary_rpc_method_handler(
                    servicer.SetRobotAI,
                    request_deserializer=messages__pb2.AIO.FromString,
                    response_serializer=simulation__pb2.SimRes.SerializeToString,
            ),
            'SetRobotDI': grpc.unary_unary_rpc_method_handler(
                    servicer.SetRobotDI,
                    request_deserializer=messages__pb2.DIO.FromString,
                    response_serializer=simulation__pb2.SimRes.SerializeToString,
            ),
            'SetFlangeDI': grpc.unary_unary_rpc_method_handler(
                    servicer.SetFlangeDI,
                    request_deserializer=messages__pb2.DIO.FromString,
                    response_serializer=simulation__pb2.SimRes.SerializeToString,
            ),
            'ChangeRobotSpeed': grpc.unary_unary_rpc_method_handler(
                    servicer.ChangeRobotSpeed,
                    request_deserializer=simulation__pb2.RobotSpeed.FromString,
                    response_serializer=simulation__pb2.SimRes.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'robotc.SimulationController', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SimulationController(object):
    """仿真-离线编程模拟服务
    """

    @staticmethod
    def SetPos(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/robotc.SimulationController/SetPos',
            messages__pb2.JPose.SerializeToString,
            simulation__pb2.SimRes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EStop(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/robotc.SimulationController/EStop',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            simulation__pb2.SimRes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EStopRelease(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/robotc.SimulationController/EStopRelease',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            simulation__pb2.SimRes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Button(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/robotc.SimulationController/Button',
            simulation__pb2.ButtonReq.SerializeToString,
            simulation__pb2.SimRes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetDialgage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/robotc.SimulationController/SetDialgage',
            simulation__pb2.DialgageReq.SerializeToString,
            simulation__pb2.SimRes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetRobotAI(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/robotc.SimulationController/SetRobotAI',
            messages__pb2.AIO.SerializeToString,
            simulation__pb2.SimRes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetRobotDI(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/robotc.SimulationController/SetRobotDI',
            messages__pb2.DIO.SerializeToString,
            simulation__pb2.SimRes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetFlangeDI(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/robotc.SimulationController/SetFlangeDI',
            messages__pb2.DIO.SerializeToString,
            simulation__pb2.SimRes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ChangeRobotSpeed(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/robotc.SimulationController/ChangeRobotSpeed',
            simulation__pb2.RobotSpeed.SerializeToString,
            simulation__pb2.SimRes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
