from os import path, remove, rename, walk
from pprint import pprint

from utils.config import BASE_DIR, LOG_FILE_PATH
from utils.enums import Operation


class FileOperator:
    def __init__(
        self, dir_path: str, file_to_find: str, operation: Operation,
        dirs_to_skip: list = None, updated_file_name: str = None,
        include_parent_folder_name: bool = False, seperator: str = '.'
    ):
        self.dir_path = dir_path
        self.file_to_find = file_to_find
        self.operation = operation
        self.dirs_to_skip = dirs_to_skip
        self.updated_file_name = updated_file_name
        self.include_parent_folder_name = include_parent_folder_name
        self.seperator = seperator

    @staticmethod
    def create_log_file(operation: str, file_paths: list):
        with open(LOG_FILE_PATH, "w") as log_file:
            log_file.write(f'File Paths of {operation} files:\n\n')
            log_file.write("\n".join(str(_path) for _path in file_paths))

    def get_file_paths(self):
        for root, dirs, files in walk(self.dir_path):
            if self.dirs_to_skip and len(self.dirs_to_skip) > 0:
                [
                    dirs.remove(dir_) for dir_ in
                    self.dirs_to_skip if dir_ in dirs
                ]
            for file in files:
                # File is compared with file extension
                if file == self.file_to_find:
                    file_path = path.join(root, file)
                    yield file_path

    def delete_files(self):
        file_paths = list(self.get_file_paths())
        [remove(file_path) for file_path in file_paths]
        self.create_log_file('deleted', file_paths)
        return (
            f'Total {len(file_paths)} files deleted.\n'
            f'For more info please check log file.'
        )

    def rename_files(self):
        file_paths = list(self.get_file_paths())
        for file_path in file_paths:
            new_path = file_path.split('/')
            new_path[-1] = self.updated_file_name
            if self.include_parent_folder_name:
                parent_folder = new_path[-2]
                new_path[-1] = (
                    f'{parent_folder}{self.seperator}{self.updated_file_name}'
                )
            new_path = '/'.join(new_path)
            if path.exists(new_path):
                return (f"The file with name {self.updated_file_name} "
                        f"already exists in the folder.")
            rename(file_path, new_path)
            self.create_log_file('renamed', file_paths)
        return (
            f'Total {len(file_paths)} files renamed.\n'
            f'For more info please check log file.'
        )

    def execute_file_operation(self):
        if self.operation == Operation.FIND:
            file_paths = list(self.get_file_paths())
            self.create_log_file('found', file_paths)
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
        dir_path=directory_path, file_to_find='tempenum4.py',
        operation=Operation.RENAME, dirs_to_skip=['venv'],
        updated_file_name='tempenum5.py'
    )
    pprint(obj1.execute_file_operation())
