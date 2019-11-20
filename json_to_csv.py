import json
import os

def save_single_json(file_name, csv_table):
    with open(file_name) as json_file:
        data = json.load(json_file)
        annotations = data['ant']['annotations']
        video_id = data['ant']['title']
        for annotation in annotations:
            subject = annotation['annotation']['subject']
            seconds = int(annotation['annotation']['seconds'])
            lable = 1 if subject == 'Happy' else 0
            csv_table.append([video_id, seconds, lable, subject])
        

if __name__ == "__main__":
    csv_table = []

    files = os.listdir('json/')
    for one_file in files:
        save_single_json('json/' + one_file, csv_table)

    for row in csv_table:
        print(row)

    import csv

    with open('json_to_csv.csv', mode='w') as csv_file:
        fieldnames = ['id', 'time', 'label', 'type']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        # writer.writerow({'emp_name': 'John Smith', 'dept': 'Accounting', 'birth_month': 'November'})
        # writer.writerow({'emp_name': 'Erica Meyers', 'dept': 'IT', 'birth_month': 'March'})
        for row in csv_table:
            writer.writerow(
                {'id':row[0],
                'time':row[1],
                'label':row[2],
                'type':row[3],
                }
            )