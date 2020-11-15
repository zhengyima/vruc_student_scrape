import json
from tqdm import tqdm
f = open("classes.txt")

cdict = {}
for line in tqdm(f):
    data = json.loads(line)
    classes = data['classes']
    for c in classes:
        cdict[c['id']] = 1

print(len(cdict))