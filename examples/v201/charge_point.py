import asyncio
import logging
import threading
import json
from ocpp2.routing import on
from ocpp2.v201 import call_result
try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys
    sys.exit(1)

from ocpp2.v201 import ChargePoint as cp
from ocpp2.v201 import call
logging.basicConfig(level=logging.INFO)

global_send = ""
global_cp = ""
global_request_id = 0


class ChargePoint(cp):
    @on("ChangeAvailability")
    def on_change_availability(self, operational_status, **kwargs):
        print("ChangeAvailability!")
        print(operational_status)
        return call_result.ChangeAvailabilityPayload(status="Accepted")

    @on("ClearCache")
    def on_clear_cache(self):
        print("ClearCache!")
        return call_result.ClearCachePayload(status="Accepted")

    @on("SendLocalList")
    def on_send_loca_list(self, version_number, update_type, **kwargs):
        print("SendLocalList!")
        print(version_number)
        print(update_type)
        return call_result.SendLocalListPayload(status="Accepted")

    @on("GetDisplayMessages")
    def on_get_display_messages(self, request_id, **kwargs):
        print("GetDisplayMessages!")
        print(request_id)
        global global_send
        global global_cp
        global global_request_id
        global_cp = self
        _send1 = "NotifyDisplayMessagesRequest"
        print(_send1)
        global_request_id = request_id
        return call_result.GetDisplayMessagesPayload(status="Accepted")

    @on("ClearChargingProfile")
    def on_clear_charging_profile(self, **kwargs):
        print("ClearChargingProfile!")
        return call_result.ClearChargingProfilePayload(status="Accepted")

    @on("SetMonitoringLevel")
    def on_set_monitoring_level(self, severity, **kwargs):
        print("SetMonitoringLevel!")
        print(severity)
        return call_result.SetMonitoringLevelPayload(status="Accepted")

    @on("GetMonitoringReport")
    def on_set_monitoring_level(self, request_id, **kwargs):
        print("GetMonitoringReport!")
        print(request_id)
        global global_send
        global global_cp
        global global_request_id
        global_cp = self
        global_send = "NotifyMonitoringReportRequest"
        global_request_id = request_id
        print(global_send)
        return call_result.GetMonitoringReportPayload(status="Accepted")

    @on("SetMonitoringLevel")
    def on_set_monitoring_level(self, severity, **kwargs):
        print("SetMonitoringLevel!")
        print(severity)
        return call_result.SetMonitoringLevelPayload(status="Accepted")

    @on("GetVariables")
    def on_get_variables(self, severity, get_variable_data,**kwargs):
        print("Got a GetVariables!")
        print(get_variable_data)
        getresult = {}
        getresult['attributeStatus'] = 'Accepted'
        getresult['component'] = get_variable_data[0]['component']
        getresult['variable'] = get_variable_data[0]['variable']
        # getresult['attributeValue'] = ''
        return call_result.GetVariablesPayload(getresult)

    @on('SetVariables')
    def on_set_variables(self, set_variable_data):
        print('Got a SetVariables!')
        print(set_variable_data)
        result = {}
        result['attributeStatus'] = 'Accepted'
        result['component'] = set_variable_data[0]['component']
        result['variable'] = set_variable_data[0]['variable']
        return call_result.SetVariablesPayload([result])

    async def send_heartbeat(self, interval):
        request = call.HeartbeatPayload()
        # request2 = call.RequestStartTransactionPayload(100,100)
        while True:
            await self.call(request)
            await asyncio.sleep(interval)

    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charging_station={"model": "Wallbox XYZ", "vendor_name": "anewone"},
            reason="PowerUp",
        )
        response = await self.call(request)

        if response.status == "Accepted":
            print("Connected to central system.")
            # await self.send_heartbeat(response.interval)
            # 测试所有命令发送
            request_heartbeat = call.HeartbeatPayload()
            await self.call(request_heartbeat)

            request_authorize = call.AuthorizePayload(id_token={"idToken": "12345", "type": "ISO14443"})
            await self.call(request_authorize)
            request_change_availability = call.ChangeAvailabilityPayload(operational_status="Operative")
            await self.call(request_change_availability)
            request_cancel_reservation = call.CancelReservationPayload(reservation_id=100)
            await self.call(request_cancel_reservation)
            request_certificate_signed = call.CertificateSignedPayload(certificate_chain="RJLYN5E1CkHJbTjqHxORXQwti1BG7RxbfrquUQTm2IN3JVT46MyY52QjqFI08+wGVn4hmOHCHH111h0oIGFonA==m8jmCZIz2ga3rCpel5i8wwrruAlvuK3QwLcDoIeyMpeKwhUF7TkesYCuljPqRuKzd/XegtZ1nAtXSTaC7Lv5Qw==")
            await self.call(request_certificate_signed)
            request_clear_cache = call.ClearCachePayload()
            await self.call(request_clear_cache)
            request_clear_charging_profile = call.ClearChargingProfilePayload()
            await self.call(request_clear_charging_profile)
            request_clear_display_message = call.ClearDisplayMessagePayload(id=1)
            await self.call(request_clear_display_message)
            request_cleared_charging_limit = call.ClearedChargingLimitPayload(charging_limit_source="CSO")
            await self.call(request_cleared_charging_limit)
            request_clear_variable_monitoring = call.ClearVariableMonitoringPayload(id=[1])#(id=[1, 2])
            await self.call(request_clear_variable_monitoring)
            request_cost_updated = call.CostUpdatedPayload(total_cost=11,transaction_id='123')
            await self.call(request_cost_updated)
            request_customer_information = call.CustomerInformationPayload(request_id=11, report=True, clear=True)
            await self.call(request_customer_information)
            request_data_transfer = call.DataTransferPayload(vendor_id='SETEC POWER', message_id='test', data='123')
            await self.call(request_data_transfer)
            request_firmware_status_notification = call.FirmwareStatusNotificationPayload(status="Downloaded")
            await self.call(request_firmware_status_notification)
            request_get_base_report = call.GetBaseReportPayload(
                request_id=123,
                report_base="ConfigurationInventory")
            await self.call(request_get_base_report)
            request_get_certificate_status = call.GetCertificateStatusPayload(
                ocsp_request_data={
                    "hashAlgorithm": "SHA256",
                    "issuerNameHash": "issuerNameHash123",
                    "issuerKeyHash": "issuerKeyHash123 ",
                    "serialNumber": "setec123456",
                    "responderURL": "www.setec-power.com"
                 })
            await self.call(request_get_certificate_status)
            request_get_charging_profiles = call.GetChargingProfilesPayload(request_id=123, charging_profile={})
            await self.call(request_get_charging_profiles)
            request_get_composite_schedule = call.GetCompositeSchedulePayload(duration=123, evse_id=123)
            await self.call(request_get_composite_schedule)
            request_get_display_messages = call.GetDisplayMessagesPayload(request_id=123)
            await self.call(request_get_display_messages)
            request_get_local_list_version = call.GetLocalListVersionPayload()
            await self.call(request_get_local_list_version)
            request_get_log = call.GetLogPayload(log={"remoteLocation": "ftp://user:password@host:port/path"}, log_type="DiagnosticsLog", request_id=123)
            await self.call(request_get_log)
            request_get_monitoring_report = call.GetMonitoringReportPayload(request_id=123)
            await self.call(request_get_monitoring_report)
            request_get_report = call.GetReportPayload(request_id=123)
            await self.call(request_get_report)
            request_get_transaction_status = call.GetTransactionStatusPayload(transaction_id="123")
            await self.call(request_get_transaction_status)
            request_get_variables = call.GetVariablesPayload(get_variable_data=[
              {
                "component": {
                  "name": "AuthCtrlr"
                },
                "variable": {
                  "name": "LocalPreAuthorize"
                }
              }
            ])
            await self.call(request_get_variables)
            request_log_status_notification = call.LogStatusNotificationPayload(status="Uploaded")
            await self.call(request_log_status_notification)
            request_meter_values = call.MeterValuesPayload(evse_id=123, meter_value=[
              {
                "timestamp": "2023-12-11T17:28:12Z",
                "sampledValue": [{
                        "context": "Transaction.End",
                        "measurand": "Energy.Active.Import.Register",
                        "value": 12
                    },
                    {
                        "context": "Transaction.End",
                        "measurand": "Energy.Active.Import.Register",
                        "value": 13.4
                    }]
              }
            ])
            await self.call(request_meter_values)
            request_notify_charging_limit = call.NotifyChargingLimitPayload(charging_limit={
                "chargingLimitSource": "EMS"
            })
            await self.call(request_notify_charging_limit)
            request_notify_customer_information = call.NotifyCustomerInformationPayload(data="data123", seq_no=123,
                                                                                        generated_at= '2023-12-11T17:28:12Z',
                                                                                        request_id=456)
            await self.call(request_notify_customer_information)
            request_notify_display_messages = call.NotifyDisplayMessagesPayload(request_id=456)
            await self.call(request_notify_display_messages)
            request_notify_ev_charging_needs = call.NotifyEVChargingNeedsPayload(charging_needs=
                                                                                 {"requestedEnergyTransfer": "DC"},
                                                                                 evse_id=123)
            await self.call(request_notify_ev_charging_needs)
            request_notify_ev_charging_schedule = call.NotifyEVChargingSchedulePayload(time_base='2023-12-11T17:28:12Z', evse_id=123,
                charging_schedule ={
                    "id": 123,
                    "startSchedule": "2020-05-15T02:37:26.944Z",
                    "chargingRateUnit": "A",
                    "chargingSchedulePeriod": [{
                            "limit": 20.0,
                            "startPeriod": 0
                        }]
                })
            await self.call(request_notify_ev_charging_schedule)
            request_notify_event = call.NotifyEventPayload(
                generated_at='2023-12-11T17:28:12Z',
                seq_no=123,
                event_data=[{
                    "eventId": 123,
                    "timestamp": "2020-05-15T02:37:26.944Z",
                    "trigger": "Periodic",
                    "actualValue": "test",
                    "eventNotificationType": "HardWiredMonitor",
                    "component": {
                          "name": "AuthCtrlr"
                        },
                    "variable": {
                          "name": "LocalPreAuthorize"
                        }
                }]
            )
            await self.call(request_notify_event)
            request_notify_monitoring_report = call.NotifyMonitoringReportPayload(request_id=123, seq_no=456,
                                                                                  generated_at="2020-05-15T02:37:26.944Z")
            await self.call(request_notify_monitoring_report)
            request_notify_report = call.NotifyReportPayload(request_id=444, seq_no=333,
                                                                                  generated_at="2020-06-15T02:37:26.944Z")
            await self.call(request_notify_report)
            request_publish_firmware = call.PublishFirmwarePayload(location="ftp://user:password@host:port/path",
                                                                   checksum="78BC78BC78BC78BC78BC78BC78BC78BC",request_id=444)
            await self.call(request_publish_firmware)
            request_publish_firmware_status_notification = call.PublishFirmwareStatusNotificationPayload(status="Published")
            await self.call(request_publish_firmware_status_notification)
            request_report_charging_profiles = call.ReportChargingProfilesPayload(
                request_id=444,
                charging_limit_source="EMS",
                charging_profile=[{
                    "id": 1234,
                    "stackLevel": 1,
                    "chargingProfilePurpose": "ChargingStationMaxProfile",
                    "chargingProfileKind": "Absolute",
                    "chargingSchedule": [{
                            "id": 123,
                            "startSchedule": "2020-05-15T02:37:26.944Z",
                            "chargingRateUnit": "A",
                            "chargingSchedulePeriod": [{
                                    "limit": 20.0,
                                    "startPeriod": 0
                                }]
                        }]

                }],
                evse_id = 444)
            await self.call(request_report_charging_profiles)
            request_request_start_transaction = call.RequestStartTransactionPayload(id_token={"idToken": "12345", "type": "ISO14443"},
                                                                 remote_start_id=11)
            await self.call(request_request_start_transaction)
            request_request_stop_transaction = call.RequestStopTransactionPayload(transaction_id='11')
            await self.call(request_request_stop_transaction)
            request_reservation_status_update = call.ReservationStatusUpdatePayload(reservation_id=123, reservation_update_status="Expired")
            await self.call(request_reservation_status_update)
            request_reserve_now = call.ReserveNowPayload(id=123,expiry_date_time ="2020-05-15T02:37:26.944Z",
                                                         id_token={"idToken": "12345", "type": "ISO14443"})
            await self.call(request_reserve_now)
            request_reset = call.ResetPayload(type="Immediate")
            await self.call(request_reset)
            request_security_event_notification = call.SecurityEventNotificationPayload(type="TamperDetectionActivated",timestamp="2020-05-15T02:37:26.944Z")
            await self.call(request_security_event_notification)
            request_send_local_list = call.SendLocalListPayload(version_number=123,update_type="Differential")
            await self.call(request_send_local_list)
            request_set_charging_profile = call.SetChargingProfilePayload(evse_id=123,
                                                                          charging_profile={
                                                                              "id": 1234,
                                                                              "stackLevel": 1,
                                                                              "chargingProfilePurpose": "ChargingStationMaxProfile",
                                                                              "chargingProfileKind": "Absolute",
                                                                              "chargingSchedule": [{
                                                                                  "id": 123,
                                                                                  "startSchedule": "2020-05-15T02:37:26.944Z",
                                                                                  "chargingRateUnit": "A",
                                                                                  "chargingSchedulePeriod": [{
                                                                                      "limit": 20.0,
                                                                                      "startPeriod": 0
                                                                                  }]
                                                                              }]
                                                                          })
            await self.call(request_set_charging_profile)
            request_set_display_message = call.SetDisplayMessagePayload(
                message={
                    "id": 12345,
                    "priority": "AlwaysFront",
                    "message": {
                          "format": "ASCII",
                          "content": "test message",
                         }
                })
            await self.call(request_set_display_message)
            request_set_monitoring_base = call.SetMonitoringBasePayload(monitoring_base="HardWiredOnly")
            await self.call(request_set_monitoring_base)
            request_set_monitoring_level = call.SetMonitoringLevelPayload(severity=123)
            await self.call(request_set_monitoring_level)
            request_set_network_profile = call.SetNetworkProfilePayload(configuration_slot=123,
                connection_data={
                    "ocppVersion": "OCPP20",
                    "ocppTransport": "JSON",
                    "ocppCsmsUrl": "ws://localhost:9001/CP_1",
                    "messageTimeout": 60,
                    "securityProfile": 12,
                    "ocppInterface": "Wireless0"
                })
            await self.call(request_set_network_profile)
            request_set_variable_monitoring = call.SetVariableMonitoringPayload(set_monitoring_data=[{
                    "id": 1234,
                    "transaction": True,
                    "value": 12,
                    "type": "LowerThreshold",
                    "severity": 3,
                    "component": {
                        "name": "AuthCtrlr"
                    },
                    "variable": {
                        "name": "LocalPreAuthorize"
                    }
                }])
            await self.call(request_set_variable_monitoring)
            request_set_variables = call.SetVariablesPayload(set_variable_data=[
                {
                    "attributeValue": "false",
                    "component": {
                        "name": "AuthCtrlr"
                    },
                    "variable": {
                        "name": "LocalPreAuthorize"
                    }
                }
            ])
            await self.call(request_set_variables)
            request_status_notification = call.StatusNotificationPayload(timestamp="2020-05-15T02:37:26.944Z",
                                                                         connector_status="Available",
                                                                         evse_id=1,
                                                                         connector_id=1)
            await self.call(request_status_notification)
            request_transaction_event = call.TransactionEventPayload(event_type="Started",
                                                                    timestamp="2020-05-15T02:37:26.944Z",
                                                                    trigger_reason="CablePluggedIn",
                                                                    seq_no=1,
                                                                    transaction_info=
                                                                     {
                                                                        "transactionId": "123",
                                                                    })
            await self.call(request_transaction_event)
            request_trigger_message = call.TriggerMessagePayload(requested_message="LogStatusNotification")
            await self.call(request_trigger_message)
            request_unlock_connector = call.UnlockConnectorPayload(evse_id=1, connector_id=1)
            await self.call(request_unlock_connector)
            request_unpublish_firmware = call.UnpublishFirmwarePayload(checksum="12BC78BC78BC78BC78BC78BC78BC78BC")
            await self.call(request_unpublish_firmware)
            request_update_firmware = call.UpdateFirmwarePayload(request_id=123,
                                                                 firmware ={
                                                                    "location": "ftp://user:password@host:port/path",
                                                                    "retrieveDateTime": "2020-05-15T02:37:26.944Z"
                                                                  })
            await self.call(request_update_firmware)

async def work_timer():
    global global_send
    global global_cp
    while True:
        # print('work_timer on loop:')
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

        await asyncio.sleep(1)


async def main():
    async with websockets.connect(
            "ws://localhost:9001/CP_1", subprotocols=["ocpp2.0.1"]
        # "ws://d58417a972efd308.octt.openchargealliance.org:14601/Vector", subprotocols=["ocpp2.0.1"]
    ) as ws:

        charge_point = ChargePoint("CP_1", ws)
        await asyncio.gather(
            charge_point.start(), charge_point.send_boot_notification()
        )


def thread_loop_task(loop):
    # 为子线程设置自己的事件循环
    asyncio.set_event_loop(loop)
    future = asyncio.gather(work_timer())
    loop.run_until_complete(future)


if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    # 创建一个事件循环thread_loop
    thread_loop = asyncio.new_event_loop()
    t = threading.Thread(target=thread_loop_task, args=(thread_loop,))
    t.daemon = True
    t.start()

    asyncio.run(main())
