#organiza as pastas de arquivos, movendo e renomeando
#fonte: https://www.youtube.com/watch?v=qbW6FRbaSl0
from forg import *
import os
import sys
import importlib_resources
import json
import time
import pandas as pd

#name = 'forg'
def forg():
    
    #data_dir = os.path.join(os.path.dirname(__file__), 'tests', 'data')
    
    #data_path = os.path.join(data_dir, 'message.eml')
    ocsv = importlib_resources.files('data').joinpath('filesext.csv')
    with ocsv.open() as fp:
        my_bytes = fp.read()
        #print(my_bytes)

    #print(ocsv)

    df = pd.read_csv(ocsv)
    mime = pd.DataFrame()
    print(df)
    folder_to_track = os.getcwd() # '/Users/rodrigofreitas/Documents' #
    folder_destination = folder_to_track + "/forg"


    #CREATE PASTA FORG IF IT DOESN'T EXISTS
    if not os.path.isdir(folder_to_track + "/forg"):
        os.makedirs(folder_to_track + "/forg")

    i = 1

    for filename in os.listdir(folder_to_track):

        #pega extensao
        lfilext = filename.split('.')
        filext = lfilext[-1]
        componto = "." + filext.lower()

        #checa tipo de midia
        mime = df.loc[df.Extension == componto,'mime']

        if mime.empty:
            print("vazio")
        else:
            #checa se ja existe a pasta, se nao, cria a pasta
            print(mime.values[0])
            destEnd = folder_destination + "/" + mime.values[0]
            if not os.path.isdir(destEnd):
                os.makedirs(destEnd)
                print("created folder : ", destEnd)
                #print(mime.values[0])
            src = folder_to_track + "/" + filename
            new_destination = destEnd + "/" + filename
                #print(new_destination)
            os.rename(src, new_destination)

def main():
    forg()              
#main
if __name__ == '__main__':
    main()