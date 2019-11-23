import pandas as pd
import csv

def merge_csv(file_one, file_two, key_col, destination):
    file_a = pd.read_csv(file_one)
    file_b = pd.read_csv(file_two)
    file_b = file_b.dropna(axis=1)
    merged = file_a.merge(file_b, on=key_col)
    merged.to_csv(destination, index=False)


def write_array_to_CSV(arrary, filename):
    with open(filename, mode='w') as csv_file:
        fieldnames = [
            'video_id', 
            'smile', 
            'gender', 
            'anger', 
            'contempt', 
            'disgust', 
            'fear', 
            'happiness', 
            'neutral', 
            'sadness', 
            'surprise', 
            'time', 
            'type', 
            'tag_video_id', 
            'tag_video_time', 
            'tag_video_labe', 
            'tag_video_tyoe', 
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in arrary:
            writer.writerow(
                {
                    'video_id': row[0], 
                    'smile': row[1], 
                    'gender':row[2], 
                    'anger': row[3], 
                    'contempt':row[4], 
                    'disgust':row[5], 
                    'fear':row[6], 
                    'happiness':row[7], 
                    'neutral':row[8], 
                    'sadness':row[9], 
                    'surprise':row[10], 
                    'time':row[11], 
                    'type':row[12], 
                    'tag_video_id':row[13], 
                    'tag_video_time':row[14], 
                    'tag_video_labe':row[15], 
                    'tag_video_tyoe':row[16], 
                }
            )

if __name__ == "__main__":
    # merge_csv('test_1.csv', 'combined.csv', 'video_id', 'merged.csv')
    res = []
    with open('test_1.csv', mode='r') as csv_file:
        csv_reader1 = csv.reader(csv_file)
        line_count1 = 0
        for row1 in csv_reader1:
            if line_count1 == 0:
                line_count1 += 1
                continue
            with open('combined.csv', mode='r') as csv_file:
                csv_reader2 = csv.reader(csv_file)
                line_count2 = 0
                for row2 in csv_reader2:
                    if line_count2 == 0:
                        line_count2 += 1
                        continue
                    if row1[0] == row2[0] and row1[-2] == row2[1]:
                        # print(row1+row2)
                        res.append(row1+row2)

    write_array_to_CSV(res, 'final.csv')
