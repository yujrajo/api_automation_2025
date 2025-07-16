import influxdb_client
import time
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from config.config import  influxdb_token
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
