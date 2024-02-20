import os
import tkinter as tk
from tkinter import filedialog, ttk

from utils.config import LOG_FILE_PATH
from utils.helpers import FileOperator, Operation


class FileOperatorGui:
    # region INITIALIZE GUI
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("File Operator App")

        self.dir_path_label = ttk.Label(self.root, text="Directory path:")
        self.dir_path_label.grid(row=0, column=0, padx=5, pady=5)
        self.dir_path_entry = ttk.Entry(self.root, width=40)
        self.dir_path_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_button = ttk.Button(
            self.root, text="Browse", command=self.browse_directory
        )
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        self.file_to_find_label = ttk.Label(self.root, text="File to find:")
        self.file_to_find_label.grid(row=1, column=0, padx=5, pady=5)
        self.file_to_find_entry = ttk.Entry(self.root, width=40)
        self.file_to_find_entry.grid(row=1, column=1, padx=5, pady=5)
        self.file_to_find_entry.insert(
            0, "Please enter the name without file extension."
        )

        self.dir_to_skip_label = ttk.Label(
            self.root, text="Directories to Skip:"
        )
        self.dir_to_skip_label.grid(row=2, column=0, padx=5, pady=5)
        self.dirs_to_skip_entry = ttk.Entry(self.root, width=40)
        self.dirs_to_skip_entry.grid(row=2, column=1, padx=5, pady=5)

        self.updated_name = ttk.Label(self.root, text="Updated name:")
        self.updated_name.grid(row=3, column=0, padx=5, pady=5)
        self.updated_name_entry = ttk.Entry(self.root, width=40)
        self.updated_name_entry.insert(
            0, "Please enter the name without file extension."
        )
        self.updated_name_entry.grid(row=3, column=1, padx=5, pady=5)

        self.operation_label = ttk.Label(self.root, text="Operation:")
        self.operation_label.grid(row=4, column=0, padx=5, pady=5)
        self.operation_var = tk.StringVar()
        self.operation_combobox = ttk.Combobox(
            self.root, textvariable=self.operation_var,
            values=[
                Operation.FIND.value, Operation.RENAME.value,
                Operation.DELETE.value
            ]
        )
        self.operation_combobox.grid(row=4, column=1, padx=5, pady=5)

        self.execute_button = ttk.Button(
            self.root, text="Execute", command=self.execute_operation,
            state=tk.DISABLED
        )
        self.execute_button.grid(row=5, column=1, padx=5, pady=5)

        self.result_label = ttk.Label(self.root, text="Result:")
        self.result_label.grid(row=6, column=0, padx=5, pady=5)
        self.result_text = tk.Text(self.root, height=2, width=40)
        self.result_text.grid(row=6, column=1, padx=5, pady=5)

        self.log_button = ttk.Button(
            self.root, text="Open Log File", command=self.open_log_file,
            state=tk.DISABLED
        )
        self.log_button.grid(row=7, column=1, padx=5, pady=5)

        self.dir_path_entry.bind(
            "<KeyRelease>", lambda event: self.check_button_state()
        )
        self.file_to_find_entry.bind(
            "<KeyRelease>", lambda event: self.check_button_state()
        )
        self.operation_combobox.bind(
            "<KeyRelease>", lambda event: self.check_button_state()
        )
        self.updated_name.bind(
            "<KeyRelease>", lambda event: self.check_button_state()
        )

        self.root.mainloop()

    def browse_directory(self):
        dir_path = filedialog.askdirectory()
        self.dir_path_entry.delete(0, tk.END)
        self.dir_path_entry.insert(0, dir_path)

    # endregion

    def check_button_state(self):
        if (
                self.operation_var.get() and self.dir_path_entry.get() and
                self.operation_var.get() == Operation.RENAME.value and
                self.file_to_find_entry.get() and self.updated_name_entry.get()
        ):
            self.execute_button.config(state=tk.NORMAL)

        elif (
                self.operation_var.get() and
                self.operation_var.get() != Operation.RENAME.value and
                self.file_to_find_entry.get() and self.dir_path_entry.get()
        ):
            self.execute_button.config(state=tk.NORMAL)
        else:
            self.execute_button.config(state=tk.DISABLED)

        self.root.after(200, self.check_button_state)

    def validate_input_entries(self):
        if (
                self.file_to_find_entry.get() == ' ' or
                (self.operation_var.get() and
                 self.updated_name_entry.get() == ' ')
        ):
            raise Exception(
                'File to find and updated name must not be empty.'
            )

    def execute_operation(self):
        try:
            self.validate_input_entries()
            dirs_to_skip = [
                _dir.strip() for _dir in self.dirs_to_skip_entry.get().split()
            ]
            obj = FileOperator(
                dir_path=self.dir_path_entry.get(),
                file_to_find=self.file_to_find_entry.get(),
                operation=getattr(Operation, self.operation_var.get()),
                dirs_to_skip=dirs_to_skip,
                updated_file_name=self.updated_name_entry.get()
            )
            result = obj.execute_file_operation()
            self.log_button.config(state=tk.NORMAL)
        except Exception as error:
            result = error

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)

    @staticmethod
    def open_log_file():
        os.system(f'start {LOG_FILE_PATH}')


if __name__ == '__main__':
    FileOperatorGui()
