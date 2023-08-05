"""Utils function for .rawls file
"""
#main imports
from os import listdir, name, makedirs, chdir, remove, rmdir, getcwd
from os.path import isfile, join,exists
import csv
import glob
from posix import POSIX_FADV_WILLNEED
import pandas as pd
import shutil

#modules imports
from .rawls import Rawls
# utils functions
def create_CSV(filepath, x, y, out_filepath, nb_samples = -1):
    """create a CSV file with all the samples
    for a pixel specified by x an y coordinates

    Arguments:
        filepath : {str} -- repertory of the rawls samples
        x : {int} -- horizontal coordinate of the pixel
        y : {int} -- vertical coordinate of the pixel
        out_filepath : {str} -- path where we want to save the CSV file
        nb_samples : {int} -- number of the samples we use for create CSV file

    Raises:
        Exception: Invalid input filepath, need at least one image rawls

    >>> from rawls.rawls import Rawls
    >>> from rawls.utils import create_CSV
    >>> path = 'images/'
    >>> out = 'images/'
    >>> create_CSV(path,0,0,out)
    images//images_0_0.csv recorded
    >>> import pandas as pd
    >>> df = pd.read_csv('images//images_0_0.csv',sep=',',header=0)
    >>> print(len(df.columns))
    3
    >>> data = df[["0_0_R"]].to_numpy()
    >>> print(data.mean())
    0.0048503875
    """
    files = []
    for f in listdir(filepath):
        if '.rawls' in f:
            files.append(filepath + "/" + f)
    if(len(files)==0):
        raise Exception('Unvalid input filepath images, need .rawls image')
    samplesPixel = []
    if(nb_samples == -1):
        for file in files:
            if file.endswith(".rawls"):
                samplesPixel.append(Rawls.load_pix(file,x,y))
    else:
        range = 0
        for i in range(nb_samples):
            finish = False
            while(finish == False):
                file = files[range]
                if file.endswith(".rawls"):
                    samplesPixel.append(Rawls.load_pix(file,x,y))
                    finish = True
                range += 1
    if filepath.endswith("/"):
        filepath = filepath[:-1]
    file_name_CSV = filepath.split('/')[-1] + "_" + str(x) + "_" + str(y)
    if not exists(out_filepath):
        makedirs(out_filepath)
    out_filepath += "/" + file_name_CSV + ".csv"
    with open(out_filepath, 'w', newline='') as file:
        writer = csv.writer(file,delimiter=',')
        row_title = [str(x) + "_" + str(y) + "_" + "R" , str(x) + "_" + str(y) + "_" + "G" , str(x) + "_" + str(y) + "_" + "B"]
        writer.writerow(row_title)
        writer.writerows(samplesPixel)
    print(out_filepath,"recorded")

def create_CSV_zone(filepath, x1, y1, x2, y2, out_filepath, nb_samples = -1):
    """create a CSV file with all the samples
    for an area specified by x1 an y1 coordinates (top left corner pixel) and x2 an y2 coordinates (bottom right corner pixel)

    Arguments:
        filepath : {str} -- repertory of the rawls samples
        x1 : {int} -- horizontal coordinate of the top left corner pixel
        y1 : {int} -- vertical coordinate of the top left corner pixel
        x2 : {int} -- horizontal coordinate of the bottom right corner pixel
        y2 : {int} -- vertical coordinate of the bottom right corner pixel
        out_filepath : {str} -- path where we want to save the CSV file
        nb_samples : {int} -- number of the samples we use for create CSV file

    Raises:
        Exception: Invalid coodinates
        Exception: Invalid input filepath, need at least one image rawls

    """

    if (x1>x2) or (y1>y2):
        raise Exception('Invalid coordinates')
    if filepath.endswith("/"):
        filepath = filepath[:-1]
    if out_filepath.endswith("/"):
        out_filepath = out_filepath[:-1]
    if out_filepath.startswith("/home") == False:
        if out_filepath.startswith("/") == False:
            out_filepath = "/" + out_filepath
        cwd = getcwd()
        out_filepath = cwd + out_filepath
        print(out_filepath)
    #create a temp repertory
    temp_out_filepath = "/tmp/" + filepath.split('/')[-1]
    for j in range(y2-y1+1):
        for i in range(x2-x1+1):
            create_CSV(filepath,x1+i,y1+j,temp_out_filepath,nb_samples)
    chdir(temp_out_filepath)
    file_extension = '.csv'
    all_filenames = [i for i in glob.glob(f"*{file_extension}")]
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    file_name_CSV = filepath.split('/')[-1] + "_" + str(x1) + "_" + str(y1) + "_to_" + str(x2) + "_" + str(y2) + ".csv"
    combined_csv.to_csv( file_name_CSV , index=False, encoding='utf-8-sig')
    shutil.move(file_name_CSV, out_filepath + "/" + file_name_CSV)
    shutil.rmtree(temp_out_filepath)
def check_file_paths(filepaths):
    """check filepaths input extension
    
    Arguments:
        filepaths: {[str]} -- image filepaths list
    
    Raises:
        Exception: Invalid input filepaths extension
    """

    if isinstance(filepaths, list):
        for p in filepaths:
            check_file_paths(p)
    else:
        if not '.rawls' in filepaths:
            raise Exception('Unvalid input filepath images, need .rawls image')