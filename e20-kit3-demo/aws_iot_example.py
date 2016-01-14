from aws_iot.aws_connector import AWSConnector
from snap_to_cloud import SNAPToCloudExample

if __name__ == "__main__":
    cloud_connector = AWSConnector()
    SNAPToCloudExample(cloud_connector)
