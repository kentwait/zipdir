import subprocess as proc
import datetime


def get_marked_dir_path(dirpath):
    """Get the absolute path of a marked directory
    """
    pass


def run_7za(cmd_str: str):
    """Calls 7za using the passed string of arguments
    """
    return proc.check_output('7za {cmd_str}'.format(cmd_str=cmd_str), shell=True)


def full_backup_dir(folder_name):
    """Creates a full compressed backup of a folder using 7zip and tar.
    Ideally should be used when backing up a folder for the first time

    Parameters
    ----------
    folder_name : path
        Relative path to the folder to be compressed

    Returns
    -------
    int
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    cmd_str = '7za a {folder_name}.{timestamp}.base.7z {folder_name}'.format(
        folder_name=folder_name, timestamp=timestamp)
    return run_7za(cmd_str)


def diff_backup_dir(folder_name, sevenz_name):
    """Creates a differetial compressed backup of a folder using 7zip and tar.
    Must have a full backup in place already before a diff backup can be created.

    Parameters
    ----------
    folder_name : path
        Relative path of the folder being differentially backed-up
    sevenz_name : filename
        Filename of the 7zip base (full) archive

    Returns
    -------
    int
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    cmd_str = '7za u {sevenz_name} -ms=off -mx=9 -t7z -u- -up0q3r2x2y2z0w2\!{folder_name}.{timestamp}.diff.7z ' \
              '{folder_name}'.format(sevenz_name=sevenz_name, folder_name=folder_name, timestamp=timestamp)
    return run_7za(cmd_str)