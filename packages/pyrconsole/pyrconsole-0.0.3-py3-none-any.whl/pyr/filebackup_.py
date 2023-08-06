import ustring         as s
from   ulog            import log

import cons            as cons
import env             as env
import filecopy        as filecopy
import filedelete      as filedelete
import fileio          as fileio
import filelistfind    as filelistfind
import ulog            as ulog

backup_dir = cons.alogs_dir + s.sep(cons.alogs_dir) + "DirBackup"
files_dir = backup_dir + s.sep(backup_dir) + "files"
paths_dir = backup_dir + s.sep(backup_dir) + "paths"


def translate(m):
    m00 = m
    m = tr_restore(m)
    ulog.log_trans(m00, m)
    return m


def tr_restore(m):
    if (m == "rv"):
        do_restore()
        m = cons.ignore_cmd
    return m


def do_restore():
    path_files = filelistfind.list_dir_(paths_dir)
    if (not path_files == None and len(path_files) > 0):
        for path_file in path_files:
            file = fileio.l(path_file)[0]
            file_backup = files_dir + s.sep(files_dir) + fileio.get_file_name(file)
            filecopy.do_copy_file(file_backup, file, overwrite=True)
        try:
            ulog.tmp_silent()
            do_cleanup()
        finally:
            ulog.no_tmp_silent()


def do_cleanup():
    filedelete.do_del_file(backup_dir)


def backup(file):
    if (fileio.exists(file)):
        # backup changed files
        if (not s.st(file, cons.alogs_dir)):
            try:
                ulog.tmp_silent()
                do_cleanup()
                do_backup__(file)
            finally:
                ulog.no_tmp_silent()


def backup_files(files):
    # backup changed files
    if (not is_all_st(files, cons.alogs_dir)):
        try:
            ulog.tmp_silent()
            do_cleanup()
            for file in files:
                if (not s.st(file, cons.alogs_dir)):
                    do_backup__(file)
        finally:
            ulog.no_tmp_silent()


def do_backup__(file):
    if (fileio.exists(file)):
        files_path = files_dir + s.sep(files_dir) + fileio.get_file_name(file)
        paths_path = paths_dir + s.sep(paths_dir) + fileio.get_file_name(file)
        filecopy.do_copy_file(file, files_path)
        fileio.mkdir(fileio.get_parent(paths_path))
        fileio.w__(paths_path, [file])


def is_all_st(files, alogs_dir):
    files = s._filter_(files, s.nst, alogs_dir)
    return len(files) == 0

