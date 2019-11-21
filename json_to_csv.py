# This scirpt convert json file from tag tool to a signgle CSV file


import json
import os
import csv

def save_single_json(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)
        annotations = data['ant']['annotations']
        video_id = data['ant']['title']

        new_array = []
        length = int(annotations[-1]['annotation']['seconds'])+1 
        for i in range(length):
            new_array.append([video_id, i, 'Neutral', 0.5])

        for annotation in annotations:
            subject = annotation['annotation']['subject']
            seconds = int(annotation['annotation']['seconds'])
            lable = 1 if subject == 'Happy' else 0
            new_array[seconds] = [video_id, seconds, subject, lable]
        return new_array

def padding_row():
    pass
        
def write_array_to_CSV(arrary, filename):
    with open(filename, mode='w') as csv_file:
        fieldnames = ['id', 'time', 'label', 'type']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in arrary:
            writer.writerow(
                {'id':row[0],
                'time':row[1],
                'label':row[2],
                'type':row[3],
                }
            )

if __name__ == "__main__":

    csv_table = []
    files = os.listdir('json/')
    for one_file in files:
        single_json_arrary = save_single_json('json/' + one_file)
        csv_table += single_json_arrary 

    # test = save_single_json('json/' + files[0])
    # print(test)

    for row in csv_table:
        print(row)

    write_array_to_CSV(csv_table, 'json_to_csv.csv')

