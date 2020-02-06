import pandas as pd
from os import listdir
from os.path import isfile, join

#file_dir= '/Users/bibekshrestha/Documents/lab/revamp/data/experiments/base/cnc-host/re/cnc-300/logs'
file_dir='/Users/bibekshrestha/Documents/lab/revamp/data/experiments/base/cnc-host/cnc-100/logs'




def get_individual_log_files(_dir):
     return [f for f in listdir(_dir) if (isfile(join(_dir, f)) and not f.startswith('log.csv'))]


def filter_data(df, threshold=80):
    df[len(df.columns)] = df[1]-df[2]
    df[len(df.columns)] = df[3]/df[4]
    
    total_len = len(df)
    
    median_rtt = df[4].median()
    
    for i in range(1,101):
        med_l = (median_rtt-i/100*median_rtt)
        med_h = (median_rtt+i/100*median_rtt)
        l,h = df[4]>=med_l, df[4]<= med_h
        
        fdf = df.where(l&h).dropna()
        
        if len(fdf)*100/total_len >= threshold:
            return fdf
            break
        

files = get_individual_log_files(file_dir)

_files,_rtt,_throughput = [],[],[]

for f in files:
    df = pd.read_csv('{}/{}'.format(file_dir,f), header=None)
    _f = filter_data(df)
    if _f is None:
        print("check {}".format(f))
    
    _rtt_m = _f[4].mean()
    _throughput_m = _f[5].mean()
    
    _files.append(f)
    _rtt.append(_rtt_m)
    _throughput.append(_throughput_m)
    
    print('{}, rtt: {}, throughput: {}'.format(f,_rtt_m, _throughput_m))

_analysis = {'file':_files, 'rtt':_rtt, 'throughput':_throughput}
df_analysis = pd.DataFrame(_analysis, columns=['file', 'rtt', 'throughput'])

med_rtt = df_analysis['rtt'].median()
total_analytics_length = len(df_analysis)

filtered_analytics = None

for i in range(1,101):
    med_l = (med_rtt-i/100*med_rtt)
    med_h = (med_rtt+i/100*med_rtt)
    l,h = df_analysis['rtt']>=med_l, df_analysis['rtt']<= med_h
    f_analytics = df_analysis.where(l&h).dropna()
    
    if len(f_analytics)*100/total_analytics_length >= 90:
        print(med_l,med_h, len(f_analytics)*100/total_analytics_length)
        filtered_analytics = f_analytics
        break
    

final_mean_rtt = filtered_analytics['rtt'].mean()
final_mean_throughput = filtered_analytics['throughput'].mean()
predicted_mean_throughput = 14/final_mean_rtt

print("mean rtt {} ms".format(filtered_analytics['rtt'].mean()*1000))
print("mean throughput {} byte/s".format(final_mean_throughput))
print("mean throughput (predicted) {} byte/s".format(predicted_mean_throughput))
print("mean rtt deviation from predicted {}%".format((predicted_mean_throughput-final_mean_throughput)/predicted_mean_throughput*100))
    


    

