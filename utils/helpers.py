from os import makedirs, walk, path, remove, rename
from pprint import pprint

from utils.config import LOG_FILE_PATH, BASE_DIR
from utils.enums import Operation


class FileOperator:
    def __init__(
            self, dir_path: str, file_to_find: str, operation: Operation,
            dirs_to_skip: list = None, updated_file_name: str = None
    ):
        self.dir_path = dir_path
        self.file_to_find = file_to_find
        self.operation = operation
        self.dirs_to_skip = dirs_to_skip
        self.updated_file_name = updated_file_name
        makedirs(LOG_FILE_PATH, exist_ok=True)

    def get_file_paths(self):
        for root, dirs, files in walk(self.dir_path):
            if self.dirs_to_skip and len(self.dirs_to_skip) > 0:
                [
                    dirs.remove(dir_) for dir_ in
                    self.dirs_to_skip if dir_ in dirs
                ]
            for file in files:
                if file == self.file_to_find:
                    file_path = path.join(root, file)
                    yield file_path

    def delete_files(self):
        file_paths = list(self.get_file_paths())
        [remove(file_path) for file_path in file_paths]
        with open(LOG_FILE_PATH, "w") as log_file:
            log_file.write('File Paths of deleted files:\n\n')
            log_file.write("\n".join(str(_path) for _path in file_paths))
        return (
            f'Total {len(file_paths)} files deleted.\n'
            f'For more info please check log file.'
        )

    def rename_files(self):
        file_paths = list(self.get_file_paths())
        for file_path in file_paths:
            new_path = file_path.split('/')
            new_path[-1] = self.updated_file_name.split('.')[0]
            new_path = '/'.join(new_path)
            rename(file_path, new_path)
        return (
            f'Total {len(file_paths)} files renamed.\n'
            f'For more info please check log file.'
        )

    def execute_file_operation(self):
        if self.operation == Operation.FIND:
            file_paths = list(self.get_file_paths())
            with open(LOG_FILE_PATH, "w") as log_file:
                log_file.write('File Paths of found files:\n\n')
                log_file.write("\n".join(str(_path) for _path in file_paths))
            return (
                f'Total {len(file_paths)} files found.\n'
                f'For more info please check log file.'
            )
        if self.operation == Operation.RENAME:
            return self.rename_files()
        if self.operation == Operation.DELETE:
            return self.delete_files()


if __name__ == '__main__':
    directory_path = BASE_DIR
    obj1 = FileOperator(
        dir_path=directory_path, file_to_find='add.dd',
        operation=Operation.RENAME, dirs_to_skip=['venv'],
        updated_file_name='aa.aa'
    )
    pprint(obj1.execute_file_operation())
