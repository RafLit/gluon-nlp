import json
import random
from copy import deepcopy

datafile = 'dev-v2.0.json'
cal_samples = 64
val_samples = 128

ids = []
with open(datafile, 'r') as f:
    data = json.load(f)
    examples = []
    for entry in data['data']:
        title = entry['title']
        for paragraph in entry['paragraphs']:
            context_text = paragraph['context']
            for qa in paragraph['qas']:
                qas_id = qa['id']
                ids.append(qas_id)
    random.seed(8)
    random.shuffle(ids)
    cal = ids[0:cal_samples]
    print('cal len: ',len(cal))
    val = ids[cal_samples:val_samples+cal_samples]
    print('val len: ',len(val))
    cal_data = deepcopy(data)
    val_data = deepcopy(data)
    for entry in cal_data['data']:
        for paragraph in entry['paragraphs']:
            paragraph['qas'] = list(filter(lambda x:x['id'] in cal, paragraph['qas']))
    for entry in val_data['data']:
        for paragraph in entry['paragraphs']:
            paragraph['qas'] = list(filter(lambda x:x['id'] in val, paragraph['qas']))
    with open('cal-v2.0.json','w') as of:
        json.dump(cal_data, of)
    with open('val-v2.0.json','w') as of:
        json.dump(val_data, of)


