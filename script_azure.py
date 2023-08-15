import os
import shutil
import datetime
import argparse
import pandas as pd
from azure.storage.blob import BlobServiceClient


parser = argparse.ArgumentParser(description='set parameters')
parser.add_argument('--default_endpoints_protocol', required=True)
parser.add_argument('--account_name', required=True)
parser.add_argument('--account_key', required=True)
parser.add_argument('--endpoint_suffix', required=True)
parser.add_argument('--original_file_url', required=True)


def main(args):
    connection_string = f"DefaultEndpointsProtocol={args.default_endpoints_protocol};" \
                        f"AccountName={args.account_name};" \
                        f"AccountKey={args.account_key};" \
                        f"EndpointSuffix={args.endpoint_suffix}"
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=connection_string)
    local_path = '.'
    str_date = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    new_file_name = f'data_{str_date}.csv'

    base_data = pd.read_csv(args.original_file_url)
    base_data.sample(frac=0.6).to_csv(os.path.join(local_path, new_file_name), index=False)

    blob_client = blob_service_client.get_blob_client(
        container='datasets',
        blob=os.path.join(local_path, new_file_name))

    with open(file=os.path.join(local_path, new_file_name), mode="rb") as data:
        blob_client.upload_blob(data=data, overwrite=True)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
