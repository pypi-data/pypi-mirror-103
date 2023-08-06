import logging
from typing import List

from cabin.domain.messages.summary_request import *
from cabin.domain.messages.timer_request import TimerRequest
from cabin.domain.tables.device import Device
from cabin.domain.tables.device_telemetry import DeviceTelemetry
from cabin.domain.tables.summary import Summary
from cabin.utils.time import *


def device_summary_req_msgs(
    timerJson: str, devicesJson: str, timespan: SummaryTimespan
) -> str:
    """Generates a list of serialised DeviceSummaryRequests.
    This function can be used to fan out a single SummaryRequest.

    Args:
    - timerJson: Serialised TimerRequest which triggered the SummaryRequest
    - devicesJson: Serialised list of Devices which DeviceSummaryRequests should
        be created for
    - timespan: The timespan to bin data in before summarising

    Returns: A list of serialised DeviceSummaryRequests.
    """
    timer: TimerRequest = TimerRequest.Schema().loads(timerJson)
    devices: List[Device] = Device.Schema(many=True).loads(devicesJson)

    if timer.IsPastDue:
        logging.warn(f"{timespan.name} timer is past due!")

    request = SummaryRequest(
        timespan=timespan,
        startTime=as_utc(timer.ScheduleStatus.Last),
        endTime=as_utc(datetime.utcnow()),
    )

    schema = DeviceSummaryRequest.Schema(many=True)
    return schema.dumps(
        [device_summmary_request(request, d) for d in devices], sort_keys=True
    )


def device_summmary_request(
    request: SummaryRequest, device: Device
) -> DeviceSummaryRequest:
    timezone = tz.gettz(device.timezone)
    start_time = start_of(request.timespan, request.startTime.astimezone(timezone))
    end_time = start_of(request.timespan, request.endTime.astimezone(timezone))
    return DeviceSummaryRequest(
        timespan=request.timespan,
        startTimestamp=timestamp(start_time),
        endTimestamp=timestamp(end_time),
        readPartition=DeviceTelemetry.partition_key(device.customerID, device.deviceID),
        writePartition=Summary.partition_key(
            device.customerID, device.deviceID, request.timespan
        ),
        device=device,
    )
