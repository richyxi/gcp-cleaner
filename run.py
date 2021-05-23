import pandas as pd
import numpy as np
import json
import os
import re

try:
  from dotenv import load_dotenv
  load_dotenv(dotenv_path='/home/ricardo/Documentos/cleaner/.env')
except ImportError:
  pass

is_header = lambda x: x.lower() in ['true']


# FIND SQUEMA
with open('./schema/' + os.environ['SCHEMA']) as f:
  schema = json.load(f)


#STORE COLUMNS PER DATA TYPE
float_cols = list()
int_cols = list()
tmstmp_cols = list()
int_regex = r"[^-0-9]+|[0-9]+(?=-)|^-$|-{2,}"
date_regex = r"[0-9]{4}[/|-](0[1-9]|1[0-2])[/|-](0[1-9]|[1-2][0-9]|3[0-1])*$"
tmstmp_regex = r"^((?![0-9]{4}[/|-](0[1-9]|1[0-2])[/|-](0[1-9]|[1-2][0-9]|3[0-1])[-| ](2[0-3]|[01][0-9])[.|:][0-5][0-9][.|:][0-5][0-9][.|:]{0,1}[0-9]{0,6}).)*$"
for element in schema:
    if element["type"].upper() == "NUMERIC":
        float_cols.append(element["name"].upper())
    elif element["type"].upper() == "INTEGER":
        int_cols.append(element["name"].upper())
    elif element["type"].upper() == "TIMESTAMP":
        tmstmp_cols.append(element["name"].upper())


# ANALYSIS 
print("Reading file..")
df = pd.read_csv('./in/'+ os.environ['FILENAME'], sep=os.environ['DELIMITER'], engine='python', chunksize=int(os.environ['SPLIT_ROWS']))
print("Done, the cleaner will start")
counter = 1
for chunk in df:
  print(f"Chunk {counter} on-going..")
  chunk[float_cols] = chunk[float_cols].apply(pd.to_numeric, errors='coerce', axis=1)
  chunk[tmstmp_cols] = chunk[tmstmp_cols].astype(str).applymap(lambda date: re.sub(date_regex, date + " 00:00:00:000000", date))
  chunk[tmstmp_cols] = chunk[tmstmp_cols].astype(str).replace(tmstmp_regex, np.nan, regex=True)
  chunk[int_cols] = chunk[int_cols].astype(str).replace(int_regex, np.nan, regex=True)

  if counter == 1:
      chunk.to_csv('./out/' + os.environ['FILENAME'], index=False, sep=',', header=is_header(os.environ['HEADER']))
  else:
      chunk.to_csv('./out/' + os.environ['FILENAME'], index=False, sep=',', header=is_header(os.environ['HEADER']), mode='a')
  counter += 1

        

#DELETE IN
os.remove('./in/'+ os.environ['FILENAME'])
