from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from enum import Enum
import functools


class NoteConfig(BaseModel):
    directory_name: Optional[str]
    filename_prefix: Optional[List[str]]
    header: Optional[List[str]]


class FileType(Enum):
    csv = "csv"
    excel = "excel"
    pickle = "pickle"


class Result(BaseModel):
    persistent: Optional[Dict[FileType, Dict[str, Any]]]
    result: Optional[Dict[FileType, Dict[str, Any]]]
    note: Optional[Dict[str, Any]]


class Note:
    filepath: Optional[str] = None
    header: Optional[List[str]] = None
    encoding: str = "utf-8"

    @classmethod
    def __check_file(cls):
        from os.path import exists

        if not exists(cls.filepath):
            return False
        return True

    @classmethod
    def __check_header(cls):
        header = ",".join(cls.header)
        with open(cls.filepath, "r", encoding=cls.encoding) as fr:
            same_header = header == fr.readline()
        if not same_header:
            return False
        return True

    @classmethod
    def set_config(cls, note_config: NoteConfig):
        from os.path import join
        from os import getcwd
        from datetime import datetime

        if note_config.filename_prefix and note_config.directory_name:
            file_name = "_".join(
                note_config.filename_prefix
                + [datetime.strftime(datetime.now(), "%Y%m%d%H%M%S") + ".csv",]
            )
            cls.filepath = join(getcwd(), note_config.directory_name, file_name)
            cls.header = note_config.header
            if (not cls.__check_file()) or (not cls.__check_header()):
                header = ",".join(cls.header) + "\n"
                cls.record_line(header)

    @classmethod
    def record_line(cls, line):
        with open(cls.filepath, "a+", encoding=cls.encoding) as fa:
            fa.write(line)

    @classmethod
    def record(cls, note_config: NoteConfig):
        cls.set_config(note_config)

        def wrapper(func):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                result: Result = func(*args, **kwargs)
                line = []
                for column_name in cls.header:
                    line.append(str(result.note[column_name]))
                line = ",".join(line) + "\n"
                cls.record_line(line=line)

            @functools.wraps(func)
            def inner_empty(*args, **kwargs):
                return func(*args, **kwargs)

            if cls.filepath != None and cls.header != None:
                return inner
            else:
                return inner_empty

        return wrapper
