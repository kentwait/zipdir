import subprocess as proc
import datetime
import os

def run_7za(cmd_str: str):
    """Calls 7za using the passed string of arguments
    """
    return proc.check_output('7za {cmd_str}'.format(cmd_str=cmd_str), shell=True)


def full_backup_dir(abs_dir_path, save_path='.', strftime='%Y%m%d-%H%M%S'):
    """Creates a full compressed backup of a folder using 7zip and tar.
    Ideally should be used when backing up a folder for the first time

    Parameters
    ----------
    abs_dir_path : path
        Absolute path to the folder to be compressed
    save_path : path
        Save path of the base archive
    strftime : str
        Date and time string formatting rules

    Returns
    -------
    int
    """
    folder_name = os.path.split(abs_dir_path)[-1]
    timestamp = datetime.datetime.now().strftime(strftime)
    cmd_str = 'a {save_path}/{folder_name}.{timestamp}.base.7z {abs_dir_path}'.format(
        save_path=save_path, folder_name=folder_name, timestamp=timestamp, abs_dir_path=abs_dir_path)
    return run_7za(cmd_str)


def diff_backup_dir(abs_dir_path, base_archive_filepath, save_path='.', strftime='%Y%m%d-%H%M%S'):
    """Creates a differetial compressed backup of a folder using 7zip and tar.
    Must have a full backup in place already before a diff backup can be created.

    Parameters
    ----------
    abs_dir_path : path
        Absolute path of the folder being differentially backed-up
    base_archive_path : filename
        File path of the 7zip base (full) archive
    save_path : path
        Save path of the base archive
    strftime : str
        Date and time string formatting rules

    Returns
    -------
    int
    """
    folder_name = os.path.split(abs_dir_path)[-1]
    timestamp = datetime.datetime.now().strftime(strftime)
    cmd_str = 'u {base_archive_filepath} -ms=off -mx=9 -t7z -u- ' \
              '-up0q3r2x2y2z0w2\!{save_path}/{folder_name}.{timestamp}.diff.7z {abs_dir_path}'.format(
        base_archive_filepath=base_archive_filepath, save_path=save_path, folder_name=folder_name, timestamp=timestamp,
        abs_dir_path=abs_dir_path)
    return run_7za(cmd_str)