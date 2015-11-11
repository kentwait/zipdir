import subprocess as proc
import datetime
import os
import tarfile as tar
# import shutil
import re


# 7zip based backup functions

def run_7za(cmd_str: str, bin_path='7za'):
    """Calls 7za using the passed string of arguments

    Parameters
    ----------
    cmd_str : str
    bin_path : path

    Returns
    -------
    process
    """
    return proc.check_output('{bin} {cmd_str}'.format(bin=bin_path, cmd_str=cmd_str), shell=True)


def full_7z_dir(abs_dir_path, save_path='.', strftime='%Y%m%d-%H%M%S', compression_level=3):
    """Creates a full compressed backup of a folder using 7zip.
    Ideally should be used when backing up a folder for the first time

    Parameters
    ----------
    abs_dir_path : str
        Absolute path to the folder to be compressed
    save_path : path
        Save path of the base archive
    strftime : str
        Date and time string formatting rules
    compression_level : 0, 1, 3, 5, 7, 9
        Level of 7zip compression. 0 is no compression while 9 gives the highest compression ratio
        (most compact archive size). Note that high levels means longer compression times.

    Returns
    -------
    int
    """
    folder_name = os.path.split(abs_dir_path)[-1]
    timestamp = datetime.datetime.now().strftime(strftime)
    cmd_str = 'a -mx={level} -t7z {save_path}/{folder_name}.{timestamp}.base.7z {abs_dir_path}'.format(
        level=compression_level, save_path=save_path, folder_name=folder_name, timestamp=timestamp,
        abs_dir_path=abs_dir_path)
    return run_7za(cmd_str)


def diff_7z_dir(abs_dir_path, base_archive_filepath, save_path='.', strftime='%Y%m%d-%H%M%S', compression_level=3):
    """Creates a differential compressed backup of a folder using 7zip.
    Must have a full backup in place already before a diff backup can be created.

    Parameters
    ----------
    abs_dir_path : str
        Absolute path of the folder being differentially backed-up
    base_archive_filepath : filename
        File path of the 7zip base (full) archive
    save_path : str
        Save path of the base archive
    strftime : str
        Date and time string formatting rules
    compression_level : 0, 1, 3, 5, 7, 9
        Level of 7zip compression. 0 is no compression while 9 gives the highest compression ratio
        (most compact archive size). Note that high levels means longer compression times.

    Returns
    -------
    int
    """
    folder_name = os.path.split(abs_dir_path)[-1]
    timestamp = str(datetime.datetime.now().strftime(strftime))
    cmd_str = 'u {base_archive_filepath} -ms=off -mx={level} -t7z -u- ' \
              '-up0q3r2x2y2z0w2\!{save_path}/{folder_name}.{timestamp}.diff.7z {abs_dir_path}' \
        .format(base_archive_filepath=base_archive_filepath, level=compression_level, save_path=save_path,
                folder_name=folder_name, timestamp=timestamp, abs_dir_path=abs_dir_path)
    return run_7za(cmd_str)


# gnu-tar based backup functions

def run_gnu_tar(cmd_str: str, bin_path='gtar'):
    """

    Parameters
    ----------
    cmd_str
    bin_path

    Returns
    -------

    """
    return proc.check_output('{bin} {cmd_str}'.format(bin=bin_path, cmd_str=cmd_str), shell=True)


def full_tar_dir(abs_dir_path, save_path='.', strftime='%Y%m%d-%H%M%S', compression_level=0):
    """

    Parameters
    ----------
    abs_dir_path
    save_path
    strftime
    compression_level

    Returns
    -------

    """
    base_path, folder_name = os.path.split(abs_dir_path)
    timestamp = str(datetime.datetime.now().strftime(strftime))
    cmd_str = '-c{compress}vf {save_path}/{folder_name}.{timestamp}.base.tar{compress_ext} ' \
              '-g {save_path}/{folder_name}.{timestamp}.base.snar -C {base_path} {folder_name}' \
        .format(compress='z' if compression_level > 0 else '', compress_ext='.gz' if compression_level > 0 else '',
                save_path=save_path, folder_name=folder_name, timestamp=timestamp, base_path=base_path)
    print(cmd_str)
    # return run_gnu_tar(cmd_str)


def diff_tar_dir(abs_dir_path, base_archive_filepath, save_path='.', strftime='%Y%m%d-%H%M%S', compression_level=0,
                 deleted_files_list='.deleted_list'):
    """

    gnu-tar can detect new files or changes but not remove deleted files
    create anti-file list to instruct deletion of files compared to the original

    Parameters
    ----------
    abs_dir_path
    base_archive_filepath
    save_path
    strftime
    compression_level
    deleted_files_list

    Returns
    -------

    """
    start_wd = os.getcwd()
    base_path, folder_name = os.path.split(abs_dir_path)
    timestamp = str(datetime.datetime.now().strftime(strftime))

    # copy base.snar to {timestamp}.snar
    archive_base_path, archive_name = os.path.split(base_archive_filepath)
    base_snar_path = os.path.join(archive_base_path, '{}.base.snar'.format(re.search('(^.+)\.base\.tar', archive_name)))
    diff_snar_path = os.path.join(archive_base_path, '{name}.{timestamp}.diff.snar'.format(
        name=re.search('(^.+)\.[0-9\-]+\.base\.tar', archive_name), timestamp=timestamp))
    print(base_snar_path, diff_snar_path)
    # shutil.copy(base_snar_path, diff_snar_path)

    # list files currently present in the directory
    os.chdir(base_path)
    current_filelist = list()
    for path, dirs, files in os.walk(folder_name):
        current_filelist.append(path)
        for f in files:
            current_filelist.append(os.path.join(path, f))

    # list files in base backup
    base_filelist = list()
    with tar.open(base_archive_filepath, 'r') as f:
        for path in f.getnames():
            str_match = re.search('^.*({0}.*?)/*$'.format(folder_name), path).group(1)  # matches the folder name first
            print(str_match)
            base_filelist.append(str_match)

    # list files in base backup and find files not present anymore
    # save files to delete as .deleted_list
    with open(os.path.join(abs_dir_path, deleted_files_list), 'w') as f:
        for path in [x for x in base_filelist if x not in set(current_filelist)]:
            print(path, file=f)

    # perform level-1 backup (differential)
    pass

    os.chdir(start_wd)


def batch_full_backup(abs_paths, function=full_7z_dir, save_path='.', strftime='%Y%m%d-%H%M%S', log=True):
    """Run batch backup for the first time

    Parameters
    ----------
    abs_paths : str
    function : function
    save_path : str
    strftime : str
    log : bool

    """
    timestamp = datetime.datetime.now().strftime(strftime)
    with open(os.path.join(save_path, 'full_backup_log.{timestamp}.txt'.format(timestamp=timestamp)), 'a') as f:
        for path in abs_paths:
            print(function(path, save_path=save_path, strftime=strftime), file=f)
            print('Compressed {}'.format(path))


def batch_diff_backup(abs_paths, base_archive_abs_paths, function=diff_7z_dir, save_path='.', strftime='%Y%m%d-%H%M%S',
                      log=True):
    """Run differential batch backup

    Parameters
    ----------
    abs_paths : str
    base_archive_abs_paths : str
    function : function
    save_path : str
    strftime : str
    log : bool

    """
    timestamp = datetime.datetime.now().strftime(strftime)
    with open(os.path.join(save_path, 'diff_backup_log.{timestamp}.txt'.format(timestamp=timestamp)), 'a') as f:
        for path, archive_path in zip(abs_paths, base_archive_abs_paths):
            print(function(path, archive_path, save_path=save_path, strftime=strftime), file=f)
            print('Differential of {}'.format(path))
