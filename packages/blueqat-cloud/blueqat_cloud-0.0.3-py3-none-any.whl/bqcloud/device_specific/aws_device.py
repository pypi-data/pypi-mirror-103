import json
import typing
from typing import Any, Dict, Optional

from blueqat import Circuit
from bqbraket import convert

from braket.device_schema import GateModelParameters
from braket.device_schema.ionq import IonqDeviceParameters
from braket.device_schema.rigetti import RigettiDeviceParameters
#from braket.device_schema.simulators import GateModelSimulatorDeviceParameters
from braket.tasks import GateModelQuantumTaskResult

from ..data import ExecutionRequest
from ..abstract_result import AbstractResult

if typing.TYPE_CHECKING:
    from ..device import Device


def make_executiondata(c: Circuit, dev: 'Device', shots: int,
                       group: Optional[str],
                       send_email: bool) -> ExecutionRequest:
    action = convert(c).to_ir().json()
    dev_params = make_device_params(c, dev)
    return ExecutionRequest(action, dev.value, dev_params, shots, group,
                            send_email)


def make_device_params(c: Circuit, dev: 'Device') -> str:
    paradigm_params = GateModelParameters(qubitCount=c.n_qubits,
                                          disableQubitRewiring=False)
    if "/rigetti/" in dev.value:
        return RigettiDeviceParameters(
            paradigmParameters=paradigm_params).json()
    if "/ionq/" in dev.value:
        return IonqDeviceParameters(paradigmParameters=paradigm_params).json()
    raise ValueError("Unknown AWS device.")


class BraketResult(AbstractResult):
    def __init__(self, result_obj: Dict[str, Any]) -> None:
        jsonized = json.dumps(result_obj)
        self.result = GateModelQuantumTaskResult.from_string(jsonized)

    def shots(self) -> typing.Counter[str]:
        return self.result.measurement_counts


def make_result(data: Dict[str, Any], _: 'Device') -> Optional[BraketResult]:
    taskmetadata = data.get('taskMetadata')
    if not (taskmetadata and taskmetadata.get('id')):
        return None
    return BraketResult(data)
