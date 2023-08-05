# Copyright (C) 2007-2011 Andrea Francia Trivolzio(PV) Italy
from __future__ import absolute_import

version='0.21.4.18'

import os
import logging

logger=logging.getLogger('trashcli.trash')
logger.setLevel(logging.WARNING)
logger.addHandler(logging.StreamHandler())

# Error codes (from os on *nix, hard coded for Windows):
EX_OK    = getattr(os, 'EX_OK'   ,  0)
EX_USAGE = getattr(os, 'EX_USAGE', 64)
EX_IOERR = getattr(os, 'EX_IOERR', 74)

import os

def backup_file_path_from(trashinfo_file_path):
    trashinfo_basename = os.path.basename(trashinfo_file_path)
    backupfile_basename = trashinfo_basename[:-len('.trashinfo')]
    info_dir = os.path.dirname(trashinfo_file_path)
    trash_dir = os.path.dirname(info_dir)
    files_dir = os.path.join(trash_dir, 'files')
    return os.path.join(files_dir, backupfile_basename)

def home_trash_dir_path(environ):
    if 'XDG_DATA_HOME' in environ:
        return ['%(XDG_DATA_HOME)s/Trash' % environ]
    elif 'HOME' in environ:
        return ['%(HOME)s/.local/share/Trash' % environ]
    return []


def home_trash_dir(environ, volume_of):
    paths = home_trash_dir_path(environ)
    for path in paths:
        yield path, volume_of(path)


def volume_trash_dir1(volume, getuid):
    path = os.path.join(volume, '.Trash/%s' % getuid())
    yield path, volume


def volume_trash_dir2(volume, getuid):
    path = os.path.join(volume, ".Trash-%s" % getuid())
    yield path, volume


def do_nothing(*argv, **argvk): pass
class Parser:
    def __init__(self):
        self.default_action = do_nothing
        self.argument_action = do_nothing
        self.short_options = ''
        self.long_options = []
        self.actions = dict()
        self._on_invalid_option = do_nothing

    def __call__(self, argv):
        program_name = argv[0]
        from getopt import getopt, GetoptError

        try:
            options, arguments = getopt(argv[1:],
                                        self.short_options,
                                        self.long_options)
        except GetoptError as e:
            invalid_option = e.opt
            self._on_invalid_option(program_name, invalid_option)
        else:
            for option, value in options:
                if option in ('--help', '-h', '--version'):
                    self.actions[option](program_name)
                    return
                if option in self.actions:
                    self.actions[option](value)
                    return
            for argument in arguments:
                self.argument_action(argument)
            self.default_action()

    def on_invalid_option(self, action):
        self._on_invalid_option = action

    def on_help(self, action):
        self.add_option('help', action, 'h')

    def on_version(self, action):
        self.add_option('version', action)

    def add_option(self, long_option, action, short_aliases=''):
        self.long_options.append(long_option)
        if long_option.endswith('='):
            import re
            long_option = re.sub('=$', '', long_option)
        self.actions['--' + long_option] = action
        for short_alias in short_aliases:
            self.add_short_option(short_alias, action)

    def add_short_option(self, short_option, action):
        self.short_options += short_option
        self.actions['-' + short_option] = action

    def on_argument(self, argument_action):
        self.argument_action = argument_action
    def as_default(self, default_action):
        self.default_action = default_action


class MyEnum:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class TrashDirsScanner:
    Found = MyEnum('TrashDirsScanner.Found')
    SkippedBecauseParentNotSticky = MyEnum('TrashDirsScanner.SkippedBecauseParentNotSticky')
    SkippedBecauseParentIsSymlink = MyEnum('TrashDirsScanner.SkippedBecauseParentIsSymlink')

    def __init__(self, environ, getuid, list_volumes, top_trash_dir_rules):
        self.getuid = getuid
        self.mount_points = list_volumes
        self.top_trash_dir_rules = top_trash_dir_rules
        self.environ = environ

    def scan_trash_dirs(self):
        home_trash_dir_paths = home_trash_dir_path(self.environ)
        for path in home_trash_dir_paths:
            yield TrashDirsScanner.Found, (path, '/')
        for volume in self.mount_points():
            top_trash_dir_path = os.path.join(volume, '.Trash', str(self.getuid()))
            result = self.top_trash_dir_rules.valid_to_be_read(top_trash_dir_path)
            if result == TopTrashDirValidationResult.Valid:
                yield TrashDirsScanner.Found, (top_trash_dir_path, volume)
            elif result == TopTrashDirValidationResult.NotValidBecauseIsNotSticky:
                yield TrashDirsScanner.SkippedBecauseParentNotSticky, (top_trash_dir_path,)
            elif result == TopTrashDirValidationResult.NotValidBecauseParentIsSymlink:
                yield TrashDirsScanner.SkippedBecauseParentIsSymlink, (top_trash_dir_path,)
            alt_top_trash_dir = os.path.join(volume, '.Trash-%s' % self.getuid())
            yield TrashDirsScanner.Found, (alt_top_trash_dir, volume)


class Harvester:
    def __init__(self, file_reader):
        self.file_reader = file_reader

        self.on_orphan_found                               = do_nothing
        self.on_trashinfo_found                            = do_nothing
        self.on_volume                                     = do_nothing
    def analize_trash_directory(self, trash_dir_path, volume_path):
        self.on_volume(volume_path)
        trashdir = TrashDir(self.file_reader)
        trashdir.open(trash_dir_path, volume_path)
        trashdir.each_trashinfo(self.on_trashinfo_found)
        trashdir.each_orphan(self.on_orphan_found)


class HelpPrinter:
    def __init__(self, out):
        self.out = out

    def usage(self, usage):
        self.println(usage)
        self.println('')

    def summary(self, summary):
        self.println(summary)
        self.println('')

    def options(self, *line_describing_option):
        self.println('Options:')
        for line in line_describing_option:
            self.println(line)
        self.println('')

    def bug_reporting(self):
        self.println("Report bugs to https://github.com/andreafrancia/trash-cli/issues")

    def println(self, line):
        println(self.out, line)

def println(out, line):
    out.write(line + '\n')

class PrintHelp:
    def __init__(self, description, out):
        self.description  = description
        self.printer      = HelpPrinter(out)

    def my_print_help(self, program_name):
        self.description(program_name, self.printer)

class PrintVersion:
    def __init__(self, out, version):
        self.out = out
        self.version = version
    def print_version(self, program_name):
        println(self.out, "%s %s" % (program_name, self.version))

class TopTrashDirValidationResult:
    class DoesNotExist:
        pass
    class NotValidBecauseIsNotSticky:
        pass
    class NotValidBecauseParentIsSymlink:
        pass
    class Valid:
        pass

class TopTrashDirRules:
    def __init__(self, fs):
        self.fs = fs

    def valid_to_be_read(self, path):
        parent_trashdir = os.path.dirname(path)
        if not self.fs.exists(path):
            return TopTrashDirValidationResult.DoesNotExist
        if not self.fs.is_sticky_dir(parent_trashdir):
            return TopTrashDirValidationResult.NotValidBecauseIsNotSticky
        if self.fs.is_symlink(parent_trashdir):
            return TopTrashDirValidationResult.NotValidBecauseParentIsSymlink
        else:
            return TopTrashDirValidationResult.Valid

class Dir:
    def __init__(self, path, entries_if_dir_exists):
        self.path                  = path
        self.entries_if_dir_exists = entries_if_dir_exists
    def entries(self):
        return self.entries_if_dir_exists(self.path)
    def full_path(self, entry):
        return os.path.join(self.path, entry)

class TrashDir:
    def __init__(self, file_reader):
        self.file_reader    = file_reader
    def open(self, path, volume_path):
        self.trash_dir_path = path
        self.volume_path    = volume_path
        self.files_dir      = Dir(self._files_dir(),
                                  self.file_reader.entries_if_dir_exists)
    def each_orphan(self, action):
        for entry in self.files_dir.entries():
            trashinfo_path = self._trashinfo_path_from_file(entry)
            file_path = self.files_dir.full_path(entry)
            if not self.file_reader.exists(trashinfo_path): action(file_path)
    def _entries_if_dir_exists(self, path):
        return self.file_reader.entries_if_dir_exists(path)

    def each_trashinfo(self, action):
        for entry in self._trashinfo_entries():
            action(os.path.join(self._info_dir(), entry))
    def _info_dir(self):
        return os.path.join(self.trash_dir_path, 'info')
    def _trashinfo_path_from_file(self, file_entry):
        return os.path.join(self._info_dir(), file_entry + '.trashinfo')
    def _files_dir(self):
        return os.path.join(self.trash_dir_path, 'files')
    def _trashinfo_entries(self, on_non_trashinfo=do_nothing):
        for entry in self._entries_if_dir_exists(self._info_dir()):
            if entry.endswith('.trashinfo'):
                yield entry
            else:
                on_non_trashinfo()

class ParseError(ValueError): pass

def maybe_parse_deletion_date(contents):
    result = Basket(unknown_date())
    ParseTrashInfo(
            on_deletion_date = lambda date: result.collect(date),
            on_invalid_date = lambda: result.collect(unknown_date())
    )(contents)
    return result.collected

def unknown_date():
    return '????-??-?? ??:??:??'

try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

class ParseTrashInfo:
    def __init__(self,
                 on_deletion_date = do_nothing,
                 on_invalid_date = do_nothing,
                 on_path = do_nothing):
        self.found_deletion_date = on_deletion_date
        self.found_invalid_date = on_invalid_date
        self.found_path = on_path
    def __call__(self, contents):
        from datetime import datetime
        for line in contents.split('\n'):
            if line.startswith('DeletionDate='):
                try:
                    date = datetime.strptime(line, "DeletionDate=%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    self.found_invalid_date()
                else:
                    self.found_deletion_date(date)

            if line.startswith('Path='):
                path=unquote(line[len('Path='):])
                self.found_path(path)

class Basket:
    def __init__(self, initial_value = None):
        self.collected = initial_value
    def collect(self, value):
        self.collected = value
def parse_deletion_date(contents):
    result = Basket()
    ParseTrashInfo(on_deletion_date=result.collect)(contents)
    return result.collected

def parse_path(contents):
    for line in contents.split('\n'):
        if line.startswith('Path='):
            return unquote(line[len('Path='):])
    raise ParseError('Unable to parse Path')


