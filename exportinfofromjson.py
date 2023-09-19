import json
import csv
import pandas
exported_json_file = input("Enter Exported JSON File Path:")
input_file = open(exported_json_file)
json_array = json.load(input_file)

# Pulls Content, Timestamp, and Author from exported Discord Data
store_list = [[item['content'], item['timestamp'], item['author']] for item in json_array]
contentvar = [[item['content']] for item in json_array]
timevar = [[item['timestamp']] for item in json_array]

# Pulls specific Username Data from the Author Field
author = [v[2] for v in store_list]
json_array2 = json.dumps(author)
json_array3 = json.loads(json_array2)
store_list2 = [[item['username']] for item in json_array3]

# Prepare List for CSV Export
zipped = list(zip(contentvar, timevar, store_list2))
df = pandas.DataFrame(zipped, columns=['Message', 'Timestamp', 'Username'])
csvname = input("What would you like to call the csv file? (Format: filename.csv): ")
df.to_csv(f"{csvname}", sep=',',index=False)
print("CSV Export Complete")