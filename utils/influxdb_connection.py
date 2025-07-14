import influxdb_client, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from helper.rest_client import RestClient
from config.config import url_base, headers, influxdb_token
from utils.logger import get_logger


LOGGER = get_logger(__name__, "DEBUG")

class InfluxDBConnection:
    def __init__(self) -> None:
        token = influxdb_token
        org = "api-course"
        url = "http://localhost:8086"

        self.write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        self.bucket = "api-automation"
        self.write_api = self.write_client.write_api(write_options=SYNCHRONOUS)

    def store_data_influxdb(self,response, endpoint):
        # response = RestClient().send_request("GET", url=f"{url_base}projects", headers=headers)
        LOGGER.debug(f"Data stored in DB: {endpoint}, {response["request"]["url"]}, {response["request"]["method"]}, {response["status_code"]} ")
        point = (
            Point("response_time")
            .tag("url", response["request"]["url"])
            .tag("method", response["request"]["method"])
            .tag("status", response["status_code"])
            .tag("endpoint", endpoint)
            .field("value", response["time"])
        )
        self.write_api.write(bucket=self.bucket, org="api-course", record=point)
        time.sleep(1)  # separate points by 1 second

    def close(self):
        self.write_client.close()
        # query_api = write_client.query_api()

        # query = """from(bucket: "api-automation")
        # |> range(start: -10m)
        # |> filter(fn: (r) => r._measurement == "response_time")"""
        # tables = query_api.query(query, org="api-course")

        # for table in tables:
        #     for record in table.records:
        #         print(record)

        # query_api = write_client.query_api()

        # query = """from(bucket: "api-automation")
        #   |> range(start: -10m)
        #   |> filter(fn: (r) => r._measurement == "measurement1")
        #   |> mean()"""
        # tables = query_api.query(query, org="api-course")

        # for table in tables:
        #     for record in table.records:
        #         print(record)
