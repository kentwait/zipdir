import os

def get_marked_dir_paths(dirpath, mark_filename='.compress_dir'):
    """Get the absolute path of marked directories in a directory tree
    """
    marked_abs_paths = list()
    for root, dirs, files in os.walk(dirpath):
        # path = root.split('/')
        if mark_filename in files:
            marked_abs_paths.append(os.path.abspath(root))
    return marked_abs_paths


def remove_all_marks(dirpath, mark_filename='.compress_dir'):
    """Remove all marks in a directory tree
    """
    for root, dirs, files in os.walk(dirpath):
        # path = root.split('/')
        if mark_filename in files:
            print('Found in {}'.format(root))
            os.remove('{}/{}'.format(root, mark_filename))


def mark_dirs(list_of_abs_paths: list, mark_filename='.compress_dir'):
    """Places .compress_dir marks on each directory in the list
    """
    for path in list_of_abs_paths:
        print(path)
        open('{}/{}'.format(path, mark_filename), 'a').close()
