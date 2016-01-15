from exosite.exosite_connector import ExositeConnector
from snap_to_cloud import SNAPToCloudExample

if __name__ == "__main__":
    cloud_connector = ExositeConnector()
    SNAPToCloudExample(cloud_connector.publish)
