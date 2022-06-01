import csv, os

class file_utils(object):
    
    @staticmethod
    def saveFile(keys, values, name):
        print('Saving file: ' + name)
        
        os.makedirs(os.path.dirname(name), exist_ok=True)
        
        with open(name, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(values)