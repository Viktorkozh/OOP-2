#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime


class FileInfo:
    def __init__(self, name, extension, creation_date,
                 read_only, hidden, system, size):
        self.name = name
        self.extension = extension
        self.creation_date = creation_date
        self.read_only = read_only
        self.hidden = hidden
        self.system = system
        self.size = size
        self.last_modified = datetime.now()
        self.selected = False
        self.deleted = False


class Directory:
    MAX_FILES = 1000  # Максимально возможный размер списка задан константой.

    def __init__(self, parent_dir, size=MAX_FILES):
        self.parent_dir = parent_dir
        self.size = size
        self.count = 0
        self.files = []

    def add_file(self, file_info):  # Добавление файлов в каталог
        if self.count < self.size:
            self.files.append(file_info)
            self.count += 1
        else:
            print("Directory is full")

    def remove_file(self, file_name):  # Удаления файлов из каталога
        self.files = [f for f in self.files if f.name != file_name]
        self.count = len(self.files)

    def find_file(self, **kwargs):  # Поиск файла
        return [f for f in self.files if all(
            getattr(f, k) == v for k, v in kwargs.items())]

    def total_size(self):  # метод вычисления полного объема каталога
        return sum(f.size for f in self.files)

    def __add__(self, other):  # операция объединения каталогов
        new_dir = Directory(self.parent_dir, self.size + other.size)
        new_dir.files = self.files + other.files
        new_dir.count = len(new_dir.files)
        return new_dir

    def __and__(self, other):
        new_dir = Directory(self.parent_dir)
        new_dir.files = [f for f in self.files if any(
            f.name == of.name and
            f.extension == of.extension for of in other.files)]
        new_dir.count = len(new_dir.files)
        return new_dir

    def generate_group(self, **kwargs):
        return Group([f for f in self.files if all(
            (callable(v) and v(getattr(f, k))) or (getattr(f, k) == v)
            for k, v in kwargs.items())])

    def __getitem__(self, index):
        return self.files[index]

    def __len__(self):
        return self.count

    def size(self):
        return self.size


class Group:
    def __init__(self, files):
        self.files = files


if __name__ == "__main__":
    dir1 = Directory("C:/Users/viktor/Desktop/ncfu/OOP/trash")
    dir1.add_file(FileInfo("file1", "txt", datetime.now(), False,
                  False, False, 100))  # read_only, hidden, system, size
    dir1.add_file(FileInfo("file2", "doc", datetime.now(),
                  True, False, False, 200))

    found_files = dir1.find_file(name="file1")
    print(f"Found files: {[f.name for f in found_files]}")

    total_size = dir1.total_size()
    print(f"Total size: {total_size}")

    group = dir1.generate_group(extension="txt")
    print(f"Group files: {[f.name for f in group.files]}")

    first_file = dir1[0]
    print(f"First file: {first_file.name}")

    last_file = dir1[-1]
    print(f"Last file: {last_file.name}")

    print(f"Directory size: {dir1.size}")
    print(f"Number of files: {len(dir1)}")

    # Объединение каталогов
    dir2 = Directory("C:/Users/viktor/Desktop/ncfu/OOP/trash2")
    dir2.add_file(FileInfo("file3", "pdf", datetime.now(),
                  False, False, False, 300))
    combined_dir = dir1 + dir2
    print(f"Combined directory files: {[f.name for f in combined_dir.files]}")

    # Пересечение каталогов
    dir3 = Directory("C:/Users/viktor/Desktop/ncfu/OOP/trash3")
    dir3.add_file(FileInfo("file1", "txt", datetime.now(),
                  False, False, False, 100))
    intersected_dir = dir1 & dir3
    print(
        "Intersected directory files:"
        f"{[f.name for f in intersected_dir.files]}")

    # Генерация группы по различным критериям
    group_by_extension = dir1.generate_group(extension="txt")
    print(f"Group by extension: {[f.name for f in group_by_extension.files]}")

    group_by_size = dir1.generate_group(size=lambda x: x > 150)
    print(f"Group by size > 150: {[f.name for f in group_by_size.files]}")

    group_by_date = dir1.generate_group(
        creation_date=lambda x: x >= datetime(2024, 10, 10))
    print("Group by date >= 2024.10.10:"
          f"{[f.name for f in group_by_date.files]}")

    group_by_attribute = dir1.generate_group(read_only=True)
    print(
        "Group by read_only attribute:"
        f"{[f.name for f in group_by_attribute.files]}")
