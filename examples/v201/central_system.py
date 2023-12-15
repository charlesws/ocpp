import asyncio
import logging
import threading
from datetime import datetime
import ui

import json
import jsonschema

import sys
import os

sys.path.append('C:\\OCPP201\\ocpp')

print("sys.path \n")
print(sys.path)

from charleswsf.mod1 import *
from moduletest.moddd import *

from ocpp2.routing import on
from ocpp2.v201 import ChargePoint as cp
from ocpp2.v201 import call_result
from ocpp2.v201 import call


try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    # import sys
    sys.exit(1)

logging.basicConfig(level=logging.INFO)

global_send = ""
global_cp = ""
global_request_id = 0


class ChargePoint1(cp):
    @on('Authorize')
    def on_authorize(self, id_token):
        print('Got a Authorize! {}'.format(id_token))
        id_token_info = {"status": "Accepted"}
        return call_result.AuthorizePayload(id_token_info=id_token_info)

    @on("BootNotification")
    def on_boot_notification(self, charging_station, reason, **kwargs):
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(), interval=10, status="Accepted"
        )

    @on('CancelReservation')
    def on_cancel_reservation(self, reservation_id):
        print('Got a CancelReservation! {}'.format(reservation_id))
        # print(reservation_id)
        return call_result.CancelReservationPayload(status='Accepted')

    @on('CertificateSigned')
    def on_certificate_signed(self, certificate_chain, **kwargs):
        print('Got a CertificateSigned!')
        print(certificate_chain)
        return call_result.CertificateSignedPayload(status='Accepted')

    @on("ChangeAvailability")
    def on_change_availability(self, operational_status, **kwargs):
        print("ChangeAvailability!")
        print(operational_status)
        return call_result.ChangeAvailabilityPayload(status="Accepted")

    @on("ClearCache")
    def on_clear_cache(self, **kwargs):
        print("ClearCache!")
        return call_result.ClearCachePayload(status="Accepted")

    @on("ClearChargingProfile")
    def on_clear_charging_profile(self, **kwargs):
        print(" ClearChargingProfile!")
        return call_result.ClearChargingProfilePayload(status="Accepted")

    @on("ClearDisplayMessage")
    def on_clear_display_message(self, id, **kwargs):
        print(' ClearDisplayMessage!{}'.format(id))
        return call_result.ClearDisplayMessagePayload(status="Accepted")

    @on("ClearedChargingLimit")
    def on_cleared_charging_limit(self, charging_limit_source, **kwargs):
        print(' ClearedChargingLimit! {}'.format(charging_limit_source))
        return call_result.ClearedChargingLimitPayload()

    @on("ClearVariableMonitoring")
    def on_clear_variable_monitoring(self, id, **kwargs):
        print(' ClearVariableMonitoring! {}'.format(id))
        result = {}
        result['status'] = 'Accepted'
        result['id'] = id[0]
        return call_result.ClearVariableMonitoringPayload(clear_monitoring_result=[result])

    @on("CostUpdated")
    def on_cost_updated(self, total_cost, transaction_id, **kwargs):
        print(' CostUpdated! {}'.format(total_cost))
        print(transaction_id)
        return call_result.CostUpdatedPayload()

    @on("CustomerInformation")
    def on_customer_information(self, request_id, report, clear, **kwargs):
        print(' CustomerInformation! {}'.format(request_id))
        print(report)
        print(clear)
        return call_result.CustomerInformationPayload(status="Accepted")

    @on("DataTransfer")
    def on_data_transfer(self, vendor_id, **kwargs):
        print(' DataTransfer! {}'.format(vendor_id))
        return call_result.CustomerInformationPayload(status="Accepted")

    @on("FirmwareStatusNotification")
    def on_firmware_status_notification(self, status, **kwargs):
        print(' FirmwareStatusNotification! {}'.format(status))
        return call_result.FirmwareStatusNotificationPayload()

    @on("GetBaseReport")
    def on_get_base_report(self, request_id, report_base, **kwargs):
        print(' GetBaseReport! {}'.format(request_id))
        print(report_base)
        return call_result.GetBaseReportPayload(status="Accepted")

    @on("GetCertificateStatus")
    def on_get_certificate_status(self, ocsp_request_data, **kwargs):
        print(' GetCertificateStatus!')
        print(ocsp_request_data)
        return call_result.GetCertificateStatusPayload(status="Accepted")

    @on("GetChargingProfiles")
    def on_get_charging_profiles(self, request_id, charging_profile, **kwargs):
        print(' GetChargingProfiles! {}'.format(request_id))
        print(charging_profile)
        return call_result.GetChargingProfilesPayload(status="Accepted")

    @on("GetCompositeSchedule")
    def on_get_composite_schedule(self, duration, evse_id, **kwargs):
        print(' GetCompositeSchedule! {}'.format(duration))
        print(evse_id)
        return call_result.GetCompositeSchedulePayload(status="Accepted")

    @on('GetDisplayMessages')
    def on_get_display_messages(self, request_id, **kwargs):
        print('Got a GetDisplayMessages!')
        print(request_id)
        return call_result.GetDisplayMessagesPayload(status='Accepted')

    @on('GetLocalListVersion')
    def on_get_local_list_version(self):
        print('Got a GetLocalListVersion!')
        return call_result.GetLocalListVersionPayload(version_number=456)

    @on('GetLog')
    def on_get_log(self, log, log_type, request_id, **kwargs):
        print('Got a GetLog!')
        print(log)
        print(log_type)
        print(request_id)
        return call_result.GetLogPayload(status='Accepted')

    @on("GetMonitoringReport")
    def on_get_monitoring_report(self, request_id, **kwargs):
        print("GetMonitoringReport!")
        print(request_id)
        # global global_send
        # global global_cp
        # global global_request_id
        # global_cp = self
        # global_send = "NotifyMonitoringReportRequest"
        # global_request_id = request_id
        # print(global_send)
        return call_result.GetMonitoringReportPayload(status="Accepted")

    @on('GetReport')
    def on_get_report(self, request_id, **kwargs):
        print('Got a GetReport!')
        print(request_id)
        return call_result.GetReportPayload(status='Accepted')

    @on('GetTransactionStatus')
    def on_get_transaction_status(self, **kwargs):
        print('Got a GetTransactionStatus!')
        return call_result.GetTransactionStatusPayload(messages_in_queue=True)

    @on("GetVariables")
    def on_get_variables(self, get_variable_data, **kwargs):
        print("Got a GetVariables!")
        print(get_variable_data)
        getresult = {}
        getresult['attributeStatus'] = 'Accepted'
        getresult['component'] = get_variable_data[0]['component']
        getresult['variable'] = get_variable_data[0]['variable']
        getresult['attributeValue'] = "testdata"
        return call_result.GetVariablesPayload([getresult])

    @on("Heartbeat")
    def on_heartbeat(self):
        print("Got a Heartbeat!")
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S") + "Z"
        )

    @on('LogStatusNotification')
    def on_log_status_notification(self, status, **kwargs):
        print('Got a LogStatusNotification!')
        print(status)
        return call_result.LogStatusNotificationPayload()

    @on('MeterValues')
    def on_meter_values(self, evse_id, meter_value, **kwargs):
        print('Got a MeterValues!')
        print(evse_id)
        print(meter_value)
        return call_result.MeterValuesPayload()

    @on('NotifyChargingLimit')
    def on_notify_charging_limit(self, charging_limit, **kwargs):
        print('Got a NotifyChargingLimit!')
        print(charging_limit)
        return call_result.NotifyChargingLimitPayload()

    @on('NotifyCustomerInformation')
    def on_notify_customer_information(self, data, seq_no, generated_at, request_id, **kwargs):
        print('Got a NotifyCustomerInformation!')
        print(data)
        print(seq_no)
        print(generated_at)
        print(request_id)
        return call_result.NotifyCustomerInformationPayload()

    @on('NotifyDisplayMessages')
    def on_notify_display_messages(self, request_id, **kwargs):
        print('Got a NotifyDisplayMessages!')
        print(request_id)
        return call_result.NotifyDisplayMessagesPayload()

    @on('NotifyEVChargingNeeds')
    def on_notify_ev_charging_needs(self, charging_needs, evse_id, **kwargs):
        print('Got a NotifyEVChargingNeeds!')
        print(charging_needs)
        print(evse_id)
        return call_result.NotifyEVChargingNeedsPayload(status='Accepted')

    @on('NotifyEVChargingSchedule')
    def on_notify_ev_charging_schedule(self, time_base, charging_schedule, evse_id, **kwargs):
        print('Got a NotifyEVChargingSchedule!')
        print(time_base)
        print(charging_schedule)
        print(evse_id)
        return call_result.NotifyEVChargingNeedsPayload(status='Accepted')

    @on('NotifyEvent')
    def on_notify_event(self, generated_at, seq_no, event_data, **kwargs):
        print('Got a NotifyEvent!')
        print(generated_at)
        print(seq_no)
        print(event_data)
        return call_result.NotifyEventPayload()

    @on('NotifyMonitoringReport')
    def on_notify_monitoring_report(self, request_id, seq_no, generated_at, **kwargs):
        print('Got a NotifyMonitoringReport!')
        print(request_id)
        print(seq_no)
        print(generated_at)
        return call_result.NotifyMonitoringReportPayload()

    @on('NotifyReport')
    def on_notify_report(self, request_id, generated_at, seq_no, **kwargs):
        print('Got a NotifyReport!')
        print(request_id)
        print(generated_at)
        print(seq_no)
        return call_result.NotifyReportPayload()

    @on('PublishFirmware')
    def on_publish_firmware(self, location, checksum, request_id, **kwargs):
        print('Got a PublishFirmware!')
        print(location)
        print(checksum)
        print(request_id)
        return call_result.PublishFirmwarePayload(status='Accepted')

    @on('PublishFirmwareStatusNotification')
    def on_publish_firmware_status_notification(self, status,  **kwargs):
        print('Got a PublishFirmwareStatusNotification!')
        print(status)
        return call_result.PublishFirmwareStatusNotificationPayload()

    @on('ReportChargingProfiles')
    def on_report_charging_profiles(self, request_id, charging_limit_source, charging_profile, evse_id, **kwargs):
        print('Got a ReportChargingProfiles!')
        print(request_id)
        print(charging_limit_source)
        print(charging_profile)
        print(evse_id)
        return call_result.ReportChargingProfilesPayload()

    @on('RequestStartTransaction')
    def on_request_start_transaction(self, id_token, remote_start_id,  **kwargs):
        print('Got a RequestStartTransaction!')
        print(id_token)
        print(remote_start_id)
        return call_result.RequestStartTransactionPayload(status='Accepted')

    @on('RequestStopTransaction')
    def on_request_stop_transaction(self, transaction_id,  **kwargs):
        print('Got a RequestStopTransaction!')
        print(transaction_id)
        return call_result.RequestStopTransactionPayload(status='Accepted')

    @on('ReservationStatusUpdate')
    def on_reservation_status_update(self, reservation_id, reservation_update_status, **kwargs):
        print('Got a ReservationStatusUpdate!')
        print(reservation_id)
        print(reservation_update_status)
        return call_result.ReservationStatusUpdatePayload()

    @on('ReserveNow')
    def on_reserve_now(self, id, expiry_date_time, id_token, **kwargs):
        print('Got a ReserveNow!')
        print(id)
        print(expiry_date_time)
        print(id_token)
        return call_result.ReserveNowPayload(status='Accepted')

    @on('Reset')
    def on_reset(self, type, **kwargs):
        print('Got a Reset!' + type)
        return call_result.ResetPayload(status='Accepted')

    @on('SecurityEventNotification')
    def on_security_event_notification(self, type, timestamp, **kwargs):
        print('Got a SecurityEventNotification!')
        print(type)
        print(timestamp)
        return call_result.SecurityEventNotificationPayload()

    @on('SendLocalList')
    def on_send_local_list(self, version_number, update_type, **kwargs):
        print('Got a SendLocalList!')
        print(version_number)
        print(update_type)
        return call_result.SendLocalListPayload(status='Accepted')

    @on('SetChargingProfile')
    def on_set_charging_profile(self, evse_id, charging_profile, **kwargs):
        print('Got a SetChargingProfile!')
        print(evse_id)
        print(charging_profile)
        return call_result.SetChargingProfilePayload(status='Accepted')

    @on('SetDisplayMessage')
    def on_set_display_message(self, message, **kwargs):
        print('Got a SetDisplayMessage!')
        print(message)
        return call_result.SetDisplayMessagePayload(status='Accepted')

    @on('SetMonitoringBase')
    def on_set_monitoring_base(self, monitoring_base, **kwargs):
        print('Got a SetMonitoringBase!')
        print(monitoring_base)
        return call_result.SetMonitoringBasePayload(status='Accepted')

    @on('SetMonitoringLevel')
    def on_set_monitoring_level(self, severity, **kwargs):
        print('Got a SetMonitoringLevel!')
        print(severity)
        return call_result.SetMonitoringBasePayload(status='Accepted')

    @on('SetNetworkProfile')
    def on_set_network_profile(self, configuration_slot, connection_data, **kwargs):
        print('Got a SetNetworkProfile!')
        print(configuration_slot)
        print(connection_data)
        return call_result.SetMonitoringBasePayload(status='Accepted')

    @on('SetVariableMonitoring')
    def on_set_variable_monitoring(self, set_monitoring_data, **kwargs):
        print('Got a SetVariableMonitoring!')
        print(set_monitoring_data)
        result1 = {}
        result1['status'] = 'Accepted'
        result1['type'] = set_monitoring_data[0]['type']
        result1['severity'] = set_monitoring_data[0]['severity']
        result1['component'] = set_monitoring_data[0]['component']
        result1['variable'] = set_monitoring_data[0]['variable']
        return call_result.SetVariableMonitoringPayload([result1])

    @on('SetVariables')
    def on_set_variables(self, set_variable_data):
        print('Got a SetVariables!')
        print(set_variable_data)
        result = {}
        result['attributeStatus'] = 'Accepted'
        result['component'] = set_variable_data[0]['component']
        result['variable'] = set_variable_data[0]['variable']
        return call_result.SetVariablesPayload([result])

    @on('StatusNotification')
    def on_status_notification(self, timestamp, connector_status, evse_id, connector_id, **kwargs):
        print('Got a StatusNotification!')
        print(timestamp)
        print(connector_status)
        print(evse_id)
        print(connector_id)
        return call_result.StatusNotificationPayload()

    @on('TransactionEvent')
    def on_transaction_event(self, event_type, timestamp, trigger_reason, seq_no,transaction_info, **kwargs):
        print('Got a TransactionEvent!')
        print(event_type)
        print(timestamp)
        print(trigger_reason)
        print(seq_no)
        print(transaction_info)
        return call_result.TransactionEventPayload()

    @on('TriggerMessage')
    def on_trigger_message(self, requested_message, **kwargs):
        print('Got a TriggerMessage!')
        print(requested_message)
        return call_result.TriggerMessagePayload(status='Accepted')

    @on('UnlockConnector')
    def on_unlock_connector(self, evse_id, connector_id, **kwargs):
        print('Got a UnlockConnector!')
        print(evse_id)
        print(connector_id)
        return call_result.UnlockConnectorPayload(status='Unlocked')

    @on('UnpublishFirmware')
    def on_unpublish_firmware(self, checksum, **kwargs):
        print('Got a UnpublishFirmware!')
        print(checksum)
        return call_result.UnpublishFirmwarePayload(status='Unpublished')

    @on('UpdateFirmware')
    def on_update_firmware(self, request_id, firmware, **kwargs):
        print('Got a UpdateFirmware!')
        print(request_id)
        print(firmware)
        return call_result.UpdateFirmwarePayload(status='InvalidCertificate')


async def on_connect(websocket, path):
    """For every new charge point that connects, create a ChargePoint
    instance and start listening for messages.
    """
    try:
        requested_protocols = websocket.request_headers["Sec-WebSocket-Protocol"]
    except KeyError:
        logging.info("Client hasn't requested any Subprotocol. " "Closing Connection")
        return await websocket.close()
        logging.error("Client hasn't requested any Subprotocol. Closing Connection")
        return await websocket.close()
    if websocket.subprotocol:
        logging.info("Protocols Matched: %s", websocket.subprotocol)
    else:
        # In the websockets lib if no subprotocols are supported by the
        # client and the server, it proceeds without a subprotocol,
        # so we have to manually close the connection.
        logging.warning(
            "Protocols Mismatched | Expected Subprotocols: %s,"
            " but client supports %s | Closing connection",
            websocket.available_subprotocols,
            requested_protocols,
        )
        return await websocket.close()

    charge_point_id = path.strip("/")
    charge_point = ChargePoint1(charge_point_id, websocket)

    await charge_point.start()
    await charge_point.on_heartbeat()

async def task_server_ocpp():
    #  deepcode ignore BindToAllNetworkInterfaces: <Example Purposes>
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9001,
        subprotocols=['ocpp2.0.1']
    )

    logging.info("Server Started listening to new connections...")
    await server.wait_closed()


async def work_timer():
    global global_send
    global global_cp
    while True:
        if global_send == "NotifyMonitoringReportRequest":
            print('NotifyMonitoringReportRequest send')
            request_notify_monitoring_report = call.NotifyMonitoringReportPayload(request_id=global_request_id,
                                                                                    seq_no=1,
                                                                                    generated_at="2023-12-11T17:28:12Z")
            await global_cp.call(request_notify_monitoring_report)

        if global_send == "NotifyDisplayMessagesRequest":
            print('NotifyDisplayMessagesRequest send')
            request_notify_display_messages = call.NotifyDisplayMessagesPayload(request_id=global_request_id)
            await global_cp.call(request_notify_display_messages)
        # print('work_timer on loop:')
        await asyncio.sleep(1)


def thread_loop_task(loop):
    # 为子线程设置自己的事件循环
    asyncio.set_event_loop(loop)
    future = asyncio.gather(task_server_ocpp(), work_timer())
    loop.run_until_complete(future)


if __name__ == '__main__':
    mod1fun()
    mod12fun()
    # 创建一个事件循环thread_loop
    thread_loop = asyncio.new_event_loop()
    t = threading.Thread(target=thread_loop_task, args=(thread_loop,))
    t.daemon = True
    t.start()

    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(ui.task_ui())

    # asyncio.run() is used when running this example with Python >= 3.7v
    # asyncio.run(main())
