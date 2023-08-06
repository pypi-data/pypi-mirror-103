
"""

                888   888b     d888                      
                888   8888b   d8888                      
                888   88888b.d88888                      
.d88b.  .d88b. 888888888Y88888P888 .d88b. 88888b.d88b.  
d88P"88bd8P  Y8b888   888 Y888P 888d8P  Y8b888 "888 "88b 
888  88888888888888   888  Y8P  88888888888888  888  888 
Y88b 888Y8b.    Y88b. 888   "   888Y8b.    888  888  888 
"Y88888 "Y8888  "Y888888       888 "Y8888 888  888  888 
    888                                                 
Y8b d88P                                                 
"Y88P"                  

Getmem by Shaurya Pratap Singh
MIT LICENCE © SHAURYA PRATAP SINGH 2-0-2-1

"""

import os
import pandas as pd
import numpy as np

print()
print()
print(f"BOT: Hello User! So how many large files do you want to see? (use 'all' to see all files)")
HEAD = input("YOU: ")

def main():
    
    dirName = os.getcwd()

    listOfFiles = list()

    try:
        for (absPath, dirnames, filenames) in os.walk(dirName): 

            dirpath = os.path.relpath(absPath)

            listOfFiles += [os.path.join(dirpath, file) for file in filenames]    
            file_list = []

    except FileNotFoundError:
        pass

    try:
        for file_name in listOfFiles:

            file_stats = os.stat(file_name)
            file_storage = file_stats.st_size / (1024 * 1024)    
            # relative_paths = [os.path.relpath(path, common_prefix) for path in paths]
            head, tail = os.path.split(file_name)

            file_list += [(tail, head, file_storage)] 
    except FileNotFoundError:
        pass

    SIZE_COLUMN_NAME = 'size (mb)'

    df = pd.DataFrame(file_list, columns=['Name', 'File Directory',  SIZE_COLUMN_NAME])
    df.reset_index(drop=True, inplace=True)

    # df[SIZE_COLUMN_NAME].apply(np.ceil)

    # df[SIZE_COLUMN_NAME] = df[SIZE_COLUMN_NAME].round(decimals=3)

    print()
    if str(HEAD) == "all":
        print(df.sort_values(by=SIZE_COLUMN_NAME, ascending=False).to_string(index=False))
    else:
        print(df.sort_values(by=SIZE_COLUMN_NAME, ascending=False).head(int(HEAD)).to_string(index=False))

    print()
    print()

    
    # if HEAD == "all":
    #     print(f"BOT: Ok, I have printed out the all files in this directory, now do you also want to save this in a csv file? (Y/n)")
    # else:
    #     print(f"BOT: Ok, I have printed out the first {HEAD} largest files in this directory, now do you also want to save this in a csv file? (Y/n)")
    
    # is_csv = input("YOU: ")

    # if is_csv == 'Y' or is_csv == 'y':
    #     print("BOT: Ok so you have answered yes! So what should you name it, (like storage.csv) ")
    #     file_name = input('YOU: ')
    #     if str(HEAD) == "all":
    #         df.sort_values(by=SIZE_COLUMN_NAME, ascending=False).to_csv(file_name, index=False)
    #     else:
    #         df.sort_values(by=SIZE_COLUMN_NAME, ascending=False).head(int(HEAD)).to_csv(file_name, index=False)
    # else:
    #     print(f"BOT: Ok,Bye!")
    #     exit()  
    

main()

print(f'BOT: Ok,  I have accomplished your task, now Bye!')

print()
print()
