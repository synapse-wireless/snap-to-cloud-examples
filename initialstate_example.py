from initialstate.initialstate_connector import InitialStateConnector
from snap_to_cloud import SNAPToCloudExample

if __name__ == "__main__":
    cloud_connector = InitialStateConnector()
    SNAPToCloudExample(cloud_connector.publish)