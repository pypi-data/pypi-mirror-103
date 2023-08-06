#!/usr/bin/env python3
#
#
#   Windlib (Useful Functions Library)
#
#
#   Copyright (C) 2021 SNWCreations. All rights reserved.
#
#


# import libraries for functions
from clint.textui import progress
from pathlib import Path
import rarfile
import tarfile
import gzip
import requests
import urllib
import platform
import zipfile
import sys
import os
import shutil


# some variables for functions.
disklst = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
           'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
found_letters = []
saved_path = '.'


# The library description...

"""
Windlib by SNWCreations

If you will use this library, I suggest importing the functions in this library through the "from" statement.

A useful function library for me!

I'm so lazy...

(C) 2021 SNWCreations. All rights reserved.
"""

# the copyright message
print('Windlib by SNWCreations')
print('Copyright (C) 2021 SNWCreations. All rights reserved.')


def typeof(variate):
    """
    Detect the type of a variable.
    """
    var_type = None
    if isinstance(variate, int):
        var_type = 'int'
    elif isinstance(variate, str):
        var_type = 'str'
    elif isinstance(variate, float):
        var_type = 'float'
    elif isinstance(variate, list):
        var_type = 'list'
    elif isinstance(variate, tuple):
        var_type = 'tuple'
    elif isinstance(variate, dict):
        var_type = 'dict'
    elif isinstance(variate, set):
        var_type = 'set'
    return var_type


def check_os(wantedOSName, slient=True, auto_exit=False):
    """
    Through the "platform" module, the system label (the first parameter) provided in the call parameter is compared with the current system label.

    The function "platform.system()" may return a string, which is a system label that can be used for comparison.

    If your python works support multiple systems, then you can combine the supported system types into a list, and then call this function.

    For example, if a work supports Windows, Mac OS, Jython (Python in Java Virtual Machine) and Linux, then the labels of these three systems can be defined as support_list: ['win32','darwin','linux','Java']

    Then, call it through the following method:

    check_os(support_list)

    * Default parameters:

    * slient - executes without generating any information.

    The default value is True. The valid values are True or False.

    * auto_exit - If the obtained system type is not what you want, it will decide whether to terminate the process according to this variable.

    If the process is terminated, an error value of "1" will be returned.

    The default value is False. The valid values are True or False.
    """

    wantedOSNameType = typeof(wantedOSName)
    if wantedOSNameType == 'list':
        if 'Java' in wantedOSName:
            if not platform.system() == 'Java':
                if not slient == True:
                    print('Not the desired operating system.')
                if not auto_exit == False:
                    sys.exit(1)
            else:
                if not slient == True:
                    print('It\'s desired opearting system.')
        if not sys.platform in wantedOSName:
            if not slient == True:
                print('Not the desired operating system.')
            if not auto_exit == False:
                sys.exit(1)
        else:
            if not slient == True:
                print('It\'s desired opearting system.')
    elif wantedOSNameType == 'str':
        if wantedOSName == 'Java':
            if not platform.system() == wantedOSName:
                if not slient == True:
                    print('Not the desired operating system.')
                if not auto_exit == False:
                    sys.exit(1)
            else:
                if not slient == True:
                    print('It\'s desired opearting system.')
        elif not platform.system() == wantedOSName:
            if not slient == True:
                print('Not the desired operating system.')
            if not auto_exit == False:
                sys.exit(1)
        else:
            if not slient == True:
                print('It\'s desired opearting system.')


def os_info(slient=True):
    """
    Get detailed information about the system, excluding information about computer accessories.

    If the "slient" parameter is False, a prompt will be generated when the function starts and finishes.
    """

    if not slient == True:
        print('Getting operating system version...')
    if sys.platform == 'win32':
        os_version_tmp = platform.platform()
        os_vers = os_version_tmp.split('-')
        os_edition = str(platform.win32_edition())
        os_arch = platform.architecture()
        os_version = 'Microsoft' + \
            os_vers[0] + ' ' + os_vers[1] + ' ' + \
            os_edition + ' ' + os_vers[2] + ' ' + os_arch[0]
    elif sys.platform == 'darwin':
        os_version_tmp = platform.platform()
        os_version = os_version_tmp.replace('-', ' ')
    elif sys.platform == 'linux':
        os_version_tmp = platform.platform()
        os_version = os_version_tmp.replace('-', ' ')
    elif platform.system() == 'Java':
        os_version = 'Java virtual machine (you may be using Jython to call this function)'
    else:
        if not slient == True:
            print('Encountered a return value that could not be processed.')
    if not slient == True:
        print(os_version)


def extract(filename, slient=True):
    """
    Unzip the compressed files.

    The "rarfile" library is required for support the rar files.

    You can download the "rarfile" library at https://sourceforge.net/projects/rarfile.berlios/files/latest/download .

    If the "slient" parameter is False, a prompt will be generated when the function starts and finishes.
    """
    if filename.endswith('.zip'):
        zip_file = zipfile.ZipFile(filename)
        if os.path.isdir(filename + "_files"):
            pass
        else:
            os.mkdir(filename + "_files")
        for names in zip_file.namelist():
            zip_file.extract(names, filename + "_files/")
        zip_file.close()
    elif filename.endswith('.gz'):
        f_name = filename.replace(".gz", "")
        # 获取文件的名称，去掉
        g_file = gzip.GzipFile(filename)
        # 创建gzip对象
        open(f_name, "w+").write(g_file.read())
        # gzip对象用read()打开后，写入open()建立的文件里。
        g_file.close()
        # 关闭gzip对象
    elif filename.endswith('.tar'):
        tar = tarfile.open(filename)
        names = tar.getnames()
        if os.path.isdir(filename + "_files"):
            pass
        else:
            os.mkdir(filename + "_files")
        # 因为解压后是很多文件，预先建立同名目录
        for name in names:
            tar.extract(name, filename + "_files/")
        tar.close()
    elif filename.endswith('.rar'):
        rar = rarfile.RarFile(filename)
        if os.path.isdir(filename + "_files"):
            pass
        else:
            os.mkdir(filename + "_files")
        os.chdir(filename + "_files")
        rar.extractall()
        rar.close()
    elif filename.endswith("tar.gz"):
        tar = tarfile.open(filename, "r:gz")
        tar.extractall()
        tar.close()
    else:
        if not slient == False:
            print('Error! Invaild file.')
    if not slient == False:
        print('Done!')


def get_file(url, save_path='.', show_progress=False, slient=True):
    """
    Download a file from the Internet.

    If the "show_progress" parameter is True, progress will be displayed when downloading. The default value of this parameter is False.

    If the "slient" parameter is False, a prompt will be generated when the function starts and finishes.
    """
    if show_progress == False:
        filename = os.path.basename(url)
        save_name = save_path + '/' + filename
        if not slient == True:
            print('Downloading', save_name)
        r = requests.get(url, stream=True)
        f = open(save_name, "wb")
        # chunk是指定每次写入的大小，每次只写了1024byte
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
        if not slient == True:
            print('Completed.')
    else:
        res = requests.get(url, stream=True)
        total_length = int(res.headers.get('content-length'))
        filename = os.path.basename(url)
        with open(filename, "wb") as pypkg:
            for chunk in progress.bar(res.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1, width=100):
                if chunk:
                    pypkg.write(chunk)


def find_file_on_all_partitions(filename, slient=True):
    """
    Find files on all hard disk partitions.

    For example, if you want to find a file called "example.txt" on all hard disk partitions, then you should call it like this:

    find_file_on_all_partitions('example.txt')

    This function will search for this file in the order of "A:\\example.txt", "B:\\example.txt", etc.

    For another example, if you want to find a file called "example.txt" in the "example" folder on all hard disk partitions, then you should call:

    find_file_on_all_partitions('example/example.txt')

    This function will find this file in the order of "A:\\example\\example.txt", "B:\\example\\example.txt", etc.

    If found, the drive letter of the partition where the target file can be found will be placed in the "found_letters" list.

    If the "slient" parameter is False, a prompt will be generated when the function starts and finishes.
    """

    now = disklst[0]
    now_file = now + ':' + os.sep + filename
    os.path.isfile(now_file)
    if now_file.isfile():
        found_letters.insert(0, now)
    del disklst[0]
    if not disklst == []:
        if not slient == True:
            find_file_on_all_partitions(filename)
        else:
            find_file_on_all_partitions(filename, slient=False)
    else:
        if not found_letters == []:
            if not slient == True:
                print('Done!')
                print(
                    'The target file was found in the partition with these drive letters:', found_letters)
        else:
            if not slient == True:
                print('Done!')
                print('The target file was not found!')
    del now
    del now_file


def get_os_partition():
    """
    Get the drive letter of the partition where the system is located.

    Will return a variable "os_partition".
    """

    os_partition_tmp = os.getenv("SystemDrive")
    os_partition = os_partition_tmp.replace(':', '')
    del os_partition_tmp
    return os_partition


def file_or_dir_exists(target):
    """
    Check if the file or directory exists.

    When the target is a file, 'IS_FILE' is returned.

    When the target is a directory, 'IS_DIR' is returned.

    When the function cannot find the target, it returns 'NOT_FOUND'.

    """
    try:
        file = Path(target)
    except:
        return 'TARGET_INVAILD'
    if file.is_file():
        return 'IS_FILE'
    elif file.is_dir():
        return 'IS_DIR'
    else:
        return False



def find_files_with_the_specified_extension(file_type, folder='.', slient=True):
    """
    Find the file with the specified extension name in targeted folder, and add the file name to the "file_list" list.

    The default value of parameter "folder" is '.' (Current dir).

    The "file_type" variable must be an extension, and does not need to carry ".".

    For example "txt" "jar" "md" "class"

    Cannot be ".txt" ".jar" ".md" ".class"

    If the "slient" parameter is False, a prompt will be generated when the function starts and finishes.
    """
    if not file_type[0] == '.':
        f_type = '.' + file_type
    items = os.listdir(folder)
    file_list = []
    for names in items:
        if names.endswith(f_type):
            file_list.append(names)
    del items


def find_str_in_file(string, filename, slient=True):
    """
    Find target string in a file.

    "filename" parameter must be a valid file name (can be absolute or relative path).

    If the "slient" parameter is False, a prompt will be generated when the function starts and finishes.
    """
    with open(filename, 'r') as f:
        counts = 0
        for line in f.readlines():
            time = line.count(string)
            counts += time
        if not slient == False:
            print("%sNumber of occurrences：%d" % (str, counts))



def copy_file(src, dst):
    """
    Copy the file (or folder) to the specified directory.
    
    You can copy multiple files to the specified directory by listing.
    """
    src_type = typeof(src)
    dst_type = typeof(dst)
    if not src_type == 'str' or 'list':
        return 'SRC_INVAILD'
    if not dst_type == 'str':
        return 'DST_INVAILD'
    try:
        dst_tmp = Path(dst)
    except:
        return 'DST_INVAILD'
    if not os.path.exists(dst):
        os.mkdir(dst)
    if src_type == 'list':
        for tmp in src:
            try:
                filename_tmp = Path(tmp)
            except:
                print(tmp, 'is invaild.')
            if filename_tmp.is_file():
                shutil.copyfile(tmp, dst_tmp)
            elif filename_tmp.is_dir():
                shutil.copytree(tmp, dst_tmp)
            else:
                print(tmp, 'is not exists.')
                continue
    elif src_type == 'str':
        try:
            filename_tmp = Path(tmp)
        except:
            print(tmp, 'is invaild.')
        if filename_tmp.is_file():
            shutil.copyfile(tmp, dst_tmp)
        elif filename_tmp.is_dir():
            shutil.copytree(tmp, dst_tmp)
        else:
            print(tmp, 'is not exists.')



def is_it_broken(path):
    """
    Check a file or directory for corruption.

    Allow a large number of directories and files to be checked through the list when called once.
    """
    if typeof(path) == 'list':
        broken_files = []
        not_found = []
        for tmp in path:
            if os.path.lexists(tmp) == True:
                if os.path.exists(path) == False:
                    broken_files.append(tmp)
            else:
                not_found.append(tmp)
    elif typeof(path) == 'str':
        if os.path.lexists(path) == True:
            if os.path.exists(path):
                return 'IS_BROKEN'
            else:
                return 'NOT_BROKEN'
        else:
            return 'NOT_FOUND'



def pushd(pushd_path='ORGIN'):
    """
    Temporarily switch to a directory and save the current path before switching for return on the next call.

    If this function is called with no arguments, the location saved in the last call is returned.
    """
    if not pushd_path == 'ORGIN':
        saved_path = os.getcwd()
        try:
            os.chdir(pushd_path)
        except:
            print('Invaild path.')
    else:
        os.chdir(saved_path)
        del saved_path



def get_zip_file(input_path, result):
    """
    Depth first traversal of the directory, with "compress_to_zip_file" function, no other purpose.
    :param input_path:
    :param result:
    :return:
    """
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path + '/' + file):
            get_zip_file(input_path + '/' + file, result)
        else:
            result.append(input_path + '/' + file)


 
def compress_to_zip_file(input_path, output_path, output_name):
    """
    Compress all files in a path to a zip file.
    :param input_path: 压缩的文件夹路径
    :param output_path: 解压（输出）的路径
    :param output_name: 压缩包名称
    :return:
    """
    f = zipfile.ZipFile(output_path + '/' + output_name, 'w', zipfile.ZIP_DEFLATED)
    filelists = []
    get_zip_file(input_path, filelists)
    for file in filelists:
        f.write(file)
    f.close()


