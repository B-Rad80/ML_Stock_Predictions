import numpy as np
import pandas as pd
import time
import os

# Creating & Saving a sample file
def createSample(data,percent):3
    percent=float(percent/100)
    start=int(len(data) * percent)
    print('starting at %i'%start)
    df_sample=data.iloc[start:]
    df_sample.to_csv(r'SampleData.csv',index=False)
    return (df_sample)

# Combining all files together
def combineData(working_dir):
    # Staring Variables
    try:
        file_names=os.listdir(working_dir)
    except:
        print("Directory not found, Do you have the folder ETFs in your working directory?")
    columns=None
    with open(working_dir + ('/%s'%file_names[0])) as f:
        columns=f.readline().strip('\n').split(',')
    df_data=pd.DataFrame(columns=columns)
    i=1
    total_files=len(file_names)

    # Creating the data
    for file in file_names:
        print('%i/%i'%(i,total_files))
        i+=1
        print(file)
        if(".txt" in file):
            with open(working_dir+('/%s'%file)) as f:
                print('staring file: %s'%file)
                df=pd.read_csv(working_dir + ('/%s' % file))
                df['Ticker']=pd.Series(['%s'%file.split('.')[0] for i in range(len(df.index))],index=df.index)
                df_data=df_data.append(df,ignore_index=True)

    # Dropping useless Columns
    for col in columns:
        if len(np.unique(df_data[col].values))==1:
            df_data=df_data.drop([col],axis=1)

    # Saving the data
    df_data.Date = pd.to_datetime(df_data.Date)
    df_data = df_data.sort_values(by="Date")
    df_data.to_csv(r'Complete.csv',index=False)
    return(df_data)

def main():
    working_dir= os.getcwd() + "/ETFs"
    df_complete,df_sample=None,None
    num=0
    while(num!='3'):
        num=input('Choose one \n' + '1: Combine Data \n' + '2: Create Sample\n' + '3: Exit \n')

        if num=='1':
            start_time=time.time()
            df_complete=combineData(working_dir)
            print(df_complete.head())
            print('time:%fs'%(time.time()-start_time))

        elif num=='2':
            df_sample=pd.read_csv("Complete.csv")
            percent=100-int(input('percentage of data to use as samples \n'))
            df_sample=createSample(df_sample,percent)
            df_sample.info(verbose=True)
            print(df_sample.head())git

        elif num=='3':
            print('Exiting')

        else:
            print('%s is not an option'%num)

if __name__=="__main__":
    main()