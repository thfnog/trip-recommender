import csv
import os
import sys

sys.path.insert(0, ".")
from WebApp.storage.storage_management import storage_management


class file_utils(object):

    @staticmethod
    def saveFile(keys, values, path_name, file_name, file_storage_name):
        print('Saving file: ' + path_name)

        os.makedirs(os.path.dirname(path_name), exist_ok=True)

        with open(path_name, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(values)

        storage_management.upload_to_s3(local_file=path_name, bucket=file_storage_name,
                                        s3_file=file_name)
