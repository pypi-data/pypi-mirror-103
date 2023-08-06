import os
import pandas as pd
import numpy as np

print()
print()
print(f"BOT: Hello User! So how many files do you want to see? (use 'all' to see all files)")
HEAD = input("YOU: ")


def main():
    
    dirName = os.getcwd()


    
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):    
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]    
        file_list = []

    for file_name in listOfFiles:

        file_stats = os.stat(file_name)
        file_storage = file_stats.st_size / (1024 * 1024)    

        file_list += [(file_name, file_storage)] 
    

    SIZE_COLUMN_NAME = 'size (mb)'

    df = pd.DataFrame(file_list, columns=['file path', SIZE_COLUMN_NAME]).round()
    df.reset_index(drop=True, inplace=True)

    # df[SIZE_COLUMN_NAME].apply(np.ceil)

    df[SIZE_COLUMN_NAME] = df[SIZE_COLUMN_NAME].round(decimals=3)

    print()
    if str(HEAD) == "all":
        print(df.sort_values(by=SIZE_COLUMN_NAME, ascending=False).to_string())
    else:
        print(df.sort_values(by=SIZE_COLUMN_NAME, ascending=False).head(int(HEAD)).to_string())

    print()
    print()

    
    print(f"BOT: Ok, I have printed out the first {HEAD} largest files in this directory, now do you also want to save this in a csv file? (Y/n)")
    is_csv = input("YOU: ")

    if is_csv == 'Y':
        print("BOT: Ok so you have answered yes! So what should you name it, (like storage.csv) ")
        file_name = input('YOU: ')
        if str(HEAD) == "all":
            df.sort_values(by=SIZE_COLUMN_NAME, ascending=False).to_csv(file_name, index=False)
        else:
            df.sort_values(by=SIZE_COLUMN_NAME, ascending=False).head(int(HEAD)).to_csv(file_name, index=False)
    else:
        print(f"BOT: Ok,Bye!")
        exit()  
    
    print(f'BOT: Ok,  I have saved the data into {file_name}, Bye!')

main()

print()
print()
