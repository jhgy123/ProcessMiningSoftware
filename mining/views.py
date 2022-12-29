import base64
import os

from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
import pm4py
os.environ["PATH"] += os.pathsep + r'D:\Program Files (x86)\Graphviz\bin'
from pm4py.objects.log.importer.xes import importer as xes_importer
# Create your views here.
#加载csv文件
def load_csv(path):
    dataframe = pd.read_csv(path, sep=';')
    dataframe = dataframe.rename(columns={'dd-MM-yyyy:HH.mm': 'time'})
    dataframe['time:timestamp'] = pd.to_datetime(dataframe['time'], format='%d-%m-%Y:%H.%M')
    # dataframe['time:timestamp']=dataframe['time'].apply(lambda x:time.mktime(time.strptime(x,'%d-%m-%Y:%H.%M')))
    # print(dataframe)
    # print(dataframe['time:timestamp'].dtype)
    dataframe = pm4py.format_dataframe(dataframe, case_id='Case ID', activity_key='Activity', timestamp_key='time:timestamp')
    return dataframe

#加载xes文件
def load_xes(path):
    dataframe = pm4py.read_xes(path)
    # pm4py.read_xes()
    # dataframe=xes_importer.apply(path)
    return dataframe

#图片base64编码
def encode_base64(file):
    with open(file,'rb') as f:
        img_data = f.read()
        base64_data = base64.b64encode(img_data)
        print(type(base64_data))
        #print(base64_data)
        # 如果想要在浏览器上访问base64格式图片，需要在前面加上：data:image/jpeg;base64,
        base64_str = str(base64_data, 'utf-8')
        print(base64_str)
        return "data:image/png;base64,"+base64_str

#首页
def index(request):
    return render(request, 'index.html')

#alpha算法挖掘
def alpha(request):
    myfile = request.FILES.get('logfile', None)
    print(myfile.name.split('.'))
    print(type(myfile))
    if myfile.name.split('.')[-1]=='csv':#文件为csv文件
        logdata=load_csv(myfile)
        petri_net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(logdata)
        pm4py.save_vis_petri_net(petri_net, initial_marking, final_marking,
                                 file_path='./temfiles/resultfiles/alpha_csv.png')
        base64data=encode_base64('./temfiles/resultfiles/alpha_csv.png')
        print(base64data)
        return render(request, 'result.html',{"algorithm":"alpha","base64img":base64data})
    if myfile.name.split('.')[-1]=='xes':#文件为xes文件
        destination = open("./temfiles/tem.xes", "wb")
        destination.writelines(myfile)
        destination.close()
        logdata=load_xes("./temfiles/tem.xes")
        petri_net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(logdata)
        pm4py.save_vis_petri_net(petri_net, initial_marking, final_marking,
                                 file_path='./temfiles/resultfiles/alpha_xes.png')
        base64data = encode_base64('./temfiles/resultfiles/alpha_xes.png')
        print(base64data)
        return render(request, 'result.html',{"algorithm":"alpha","base64img":base64data})

#heuristics算法挖掘
def heuristics(request):
    myfile = request.FILES.get('logfile', None)
    print(myfile.name.split('.'))
    print(type(myfile))
    if myfile.name.split('.')[-1]=='csv':#文件为csv文件
        logdata=load_csv(myfile)
        petri_net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(logdata)
        pm4py.save_vis_petri_net(petri_net, initial_marking, final_marking,
                                 file_path='./temfiles/resultfiles/heuristics_csv.png')
        base64data=encode_base64('./temfiles/resultfiles/heuristics_csv.png')
        print(base64data)
        return render(request, 'result.html',{"algorithm":"heuristics","base64img":base64data})
    if myfile.name.split('.')[-1]=='xes':#文件为xes文件
        destination = open("./temfiles/tem.xes", "wb")
        destination.writelines(myfile)
        destination.close()
        logdata=load_xes("./temfiles/tem.xes")
        petri_net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(logdata)
        pm4py.save_vis_petri_net(petri_net, initial_marking, final_marking,
                                 file_path='./temfiles/resultfiles/heuristics_xes.png')
        base64data = encode_base64('./temfiles/resultfiles/heuristics_xes.png')
        print(base64data)
        return render(request, 'result.html',{"algorithm":"heuristics","base64img":base64data})

#inductive算法挖掘
def inductive(request):
    myfile = request.FILES.get('logfile', None)
    print(myfile.name.split('.'))
    print(type(myfile))
    if myfile.name.split('.')[-1]=='csv':#文件为csv文件
        logdata=load_csv(myfile)
        petri_net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(logdata)
        pm4py.save_vis_petri_net(petri_net, initial_marking, final_marking,
                                 file_path='./temfiles/resultfiles/inductive_csv.png')
        base64data=encode_base64('./temfiles/resultfiles/inductive_csv.png')
        print(base64data)
        return render(request, 'result.html',{"algorithm":"inductive","base64img":base64data})
    if myfile.name.split('.')[-1]=='xes':#文件为xes文件
        destination = open("./temfiles/tem.xes", "wb")
        destination.writelines(myfile)
        destination.close()
        logdata=load_xes("./temfiles/tem.xes")
        petri_net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(logdata)
        pm4py.save_vis_petri_net(petri_net, initial_marking, final_marking,
                                 file_path='./temfiles/resultfiles/inductive_xes.png')
        base64data = encode_base64('./temfiles/resultfiles/inductive_xes.png')
        print(base64data)
        return render(request, 'result.html',{"algorithm":"inductive","base64img":base64data})





