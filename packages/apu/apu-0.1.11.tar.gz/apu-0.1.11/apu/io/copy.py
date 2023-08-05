""" make recursive cpy easy"""
import os
import shutil
from multiprocessing import Pool, Lock

from pathlib import Path
from tqdm import tqdm

from apu.mp.parallel_for import parallel_for
from apu.io.fileformat import compair

MUTEX = Lock()


def copy_(file_):
    """simple copy for one file"""
    src_file = file_[0]
    dst_file = file_[1]

    with MUTEX:
        print(f"{src_file} -> {dst_file}")

    shutil.copy(src_file, dst_file)


class Copy:
    """Copy data"""
    def __init__(self,
                 origin: str,
                 dest: str,
                 number: int = None,
                 sort: bool = True,
                 verbose: bool = False):
        """copy from origin to destination. copy only a given
           number of objects of each subfolder to the destination.
           If you want you can sort the data in each subfolder. this
           makes it easy to make it more possible that the objects
           in the folder are arranged.
        """
        self.origin = Path(origin)
        self.destination = Path(dest)
        self.pool = Pool(os.cpu_count())
        self.verbose = verbose
        self.count = 1 if number is None or number <= 0 else number

        self.files = self.__files(sort=sort)

    def __files(self, sort):
        """create the file list. pleae keep in mind, that it can
           take longer if you tr to check if the
           files allready exists."""
        files_ = set()
        for src_dir, _, files in os.walk(self.origin):

            dst_dir = Path(
                src_dir.replace(str(self.origin), str(self.destination), 1))

            if not dst_dir.exists():
                if self.verbose:
                    print(f"{dst_dir} not exists")
                dst_dir.mkdir(parents=True, exist_ok=True)

            if sort:
                file_list = sorted(
                    files[:self.count] if len(files) >= self.count else files,
                    key=lambda path: path)
            else:
                file_list = files

            if len(file_list) == 0:
                print(f"{src_dir} is empty?")
                continue

            for file_ in file_list:
                src_file = Path(src_dir) / file_
                dst_file = dst_dir / file_

                if dst_file.exists() and not compair(
                        src_file, dst_file, method="md5"):
                    print(f"{src_file} already copied")
                else:
                    files_.add(tuple((src_file, dst_file)))
        return files_

    def __call__(self, parallel: bool = False):
        """ call the copy in parallel or serial"""
        if self.files is None or len(self.files) == 0:
            return

        if parallel:
            parallel_for(copy_, self.files)
        else:
            for file_ in tqdm(self.files):
                copy_(file_)
