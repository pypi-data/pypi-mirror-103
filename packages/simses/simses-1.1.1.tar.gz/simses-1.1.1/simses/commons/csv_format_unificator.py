import os
import pandas as pd

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# rootdir="C:\\Users\\Lenovo\\Desktop\\trying_csv"
rootdir="../../"
list_of_path=[]

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        list_of_path.append(os.path.join(subdir,file))

for i in range(len(list_of_path)):
    if ".csv" in list_of_path[i]:
        if ".csv.gz" in list_of_path[i]:
            pass
        else:
            path = list_of_path[i]
            print(path)
            name = path.partition("\\")[2]

            try :
                file = open(path,"r")
                print("File is open")
                if ";" in file.read() :
                    print(f"{bcolors.WARNING}Here the seperator is ;{bcolors.ENDC}")
                    data = pd.read_csv(path, sep=";")
                    print(data.head(),"\n")

                    for col in data.columns:
                        try :

                            data[col] = [x.replace(',', '.') for x in data[col]]
                            # for x in data[col]:
                                # if isinstance(x,int) :
                                #     pass
                                # else :
                                #     data[col]=x.replace(',', '.')
                        except :
                            pass

                    data.to_csv(path,index=False, decimal=".", sep=",")
                    print(path, f"{bcolors.OKGREEN}is NOW up to standards{bcolors.ENDC}")

                else :
                    print("Here the seperator is ,")
                    data = pd.read_csv(path, sep=",")
                    print(data.head(),"\n")
                    print(path, f"{bcolors.OKCYAN}is already up to standards{bcolors.ENDC} \n")

            except :
                print("Failed to open file")