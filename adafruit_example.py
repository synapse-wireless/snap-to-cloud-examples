from adafruitio.adafruit_connector import AdafruitConnector
from snap_to_cloud import SNAPToCloudExample

if __name__ == "__main__":
    cloud_connector = AdafruitConnector()
    SNAPToCloudExample(cloud_connector.publish)
