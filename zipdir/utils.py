import os
import re

def get_marked_dirs(dir_path, mark_filename='.compress_dir'):
    """Get the absolute path of marked directories in a directory tree
    """
    marked_abs_paths = list()
    for root, dirs, files in os.walk(dir_path):
        # path = root.split('/')
        if mark_filename in files:
            marked_abs_paths.append(os.path.abspath(root))
    return marked_abs_paths


def remove_all_marks(dir_path, mark_filename='.compress_dir'):
    """Remove all marks in a directory tree
    """
    for root, dirs, files in os.walk(dir_path):
        # path = root.split('/')
        if mark_filename in files:
            print('Found in {}'.format(root))
            os.remove('{}/{}'.format(root, mark_filename))


def mark_dirs(list_of_abs_paths: list, mark_filename='.compress_dir'):
    """Marks each directory in the list for compression
    """
    for path in list_of_abs_paths:
        print('Marking {}'.format(path))
        open('{}/{}'.format(path, mark_filename), 'a').close()

def parse_dirs_file(fh):
    return [line.replace('\n', '') for line in fh.readlines()]


def mark_all_top_subdirs(root_dir, mark_filename='.compress_dir', exclude='^\.'):
    assert os.path.isabs(root_dir)
    abs_paths = list()
    exclude_path = re.compile(str(exclude))
    for path in os.listdir(root_dir):
        if not exclude_path.search(path):
            path = os.path.join(root_dir, path)
            if os.path.isdir(path):
                abs_paths.append(path)
    mark_dirs(abs_paths, mark_filename=mark_filename)
    return abs_paths


def mark_all_end_subdirs(root_dir, mark_filename='.compress_dir', exclude='^\.'):
    assert os.path.isabs(root_dir)
    abs_paths = list()
    exclude_path = re.compile(str(exclude))
    for root, dirs, files in os.walk(root_dir):
        if len(dirs) == 0:
            if not exclude_path.search(os.path.split(root)[-1]):
                if os.path.isdir(root):
                    abs_paths.append(root)
    mark_dirs(abs_paths, mark_filename=mark_filename)
    return abs_paths


def mark_subdirs_gt(root_dir, maxcount=100, mark_filename='.compress_dir', exclude='^\.'):
    assert os.path.isabs(root_dir)
    abs_paths = list()
    exclude_path = re.compile(str(exclude))
    for root, dirs, files in os.walk(root_dir):
        if len(dirs) + len(files) >= maxcount:
            if not exclude_path.search(os.path.split(root)[-1]):
                if os.path.isdir(root):
                    abs_paths.append(root)
    mark_dirs(abs_paths, mark_filename=mark_filename)