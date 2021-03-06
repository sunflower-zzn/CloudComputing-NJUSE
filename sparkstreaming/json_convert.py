import json

filename='word.txt'
with open(filename, 'r',encoding='UTF-8') as fp:
    lines = fp.readlines()
    dict_all={}
    day='2020-01-20'
    dict_day={}
    key=[]
    value=[]
    for line in lines:
        list=[]
        line=line.replace('(','').replace(')','').replace('\n','').replace('\'','').replace('）','')
        list=line.split(',')
        for i in range(len(list)):
            list[i]=list[i].strip()
        key.append(list[0])
        value.append(list[1])
    for i in range(len(key)):
        dict_day[str(key[i])]=int(value[i])
    dict_all[day]=dict_day
    str_json=json.dumps(dict_all)
    with open("result.json", "w") as fp:
        fp.write(json.dumps(dict_all,indent=4))
