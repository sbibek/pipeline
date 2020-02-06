import pandas as pd
from os import listdir
from os.path import isfile, join

file_dir= '/Users/bibekshrestha/Documents/lab/revamp/data/experiments/base/cnc-host/cnc-200/logs'




def get_individual_log_files(_dir):
     return [f for f in listdir(_dir) if (isfile(join(_dir, f)) and not f.startswith('log.csv'))]


def filter_data(df, threshold=80):
    df[len(df.columns)] = df[1]-df[2]
    df[len(df.columns)] = df[3]/df[4]
    
    total_len = len(df)
    
    median_rtt = df[4].median()
    
    for i in range(1,1001):
        med_l = (median_rtt-i/100*median_rtt)
        med_h = (median_rtt+i/100*median_rtt)
        l,h = df[4]>=med_l, df[4]<= med_h
        
        fdf = df.where(l&h).dropna()
        
        if len(fdf)*100/total_len >= threshold:
            return fdf
            break
        

files = get_individual_log_files(file_dir)

for f in files:
    df = pd.read_csv('{}/{}'.format(file_dir,f), header=None)
    _f = filter_data(df)
    if _f is None:
        print("check {}".format(f))
    print('{}, rtt: {}, throughput: {}'.format(f,_f[4].mean(), _f[5].mean()))
