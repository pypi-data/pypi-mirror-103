#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--
# wine-ctl, manage Wine prefixes
# Copyright (C) 2019-2020  Marc Dequènes (Duck)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#++
# You can find the code here: https://projects.duckcorp.org/projects/wine-ctl

VERSION = "2.1.0"


# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse
from argcomplete.completers import ChoicesCompleter, FilesCompleter, SuppressCompleter
import yaml
import jsonschema
import os
from pathlib import Path
import subprocess
import fnmatch
import re
import shutil
import shlex
import tempfile



class WinePrefix():
    def __init__(self, config, name, bin_path_scheme):
        self.name = name
        self.config = config
        self.bin_path_scheme = bin_path_scheme

        self.path = Path(config['install_path']).joinpath(self.name)

    def exists(self):
        return self.path.exists()

    def find_exe(self, exe_name, exe_list):
        bin_path_scheme = self.bin_path_scheme
        if not bin_path_scheme and 'default_bin_path_scheme' in config:
            bin_path_scheme = config['default_bin_path_scheme']

        if bin_path_scheme:
            if 'bin_path_schemes' not in config or bin_path_scheme not in config['bin_path_schemes']:
                print(f"Binary scheme '{bin_path_scheme}' not defined")
                return False
            if exe_name not in config['bin_path_schemes'][bin_path_scheme]:
                print(f"Binary scheme '{bin_path_scheme}' does not contain path for '{exe_name}'")
                return False
            # if set to None (Null in YAML), then skip the  override and lookup in the PATH
            if config['bin_path_schemes'][bin_path_scheme][exe_name]:
                if not Path(config['bin_path_schemes'][bin_path_scheme][exe_name]).exists():
                    print(f"Path for '{exe_name}' in binary scheme '{bin_path_scheme}' does not exist")
                    return False
                return config['bin_path_schemes'][bin_path_scheme][exe_name]

        for exe in exe_list:
            path = shutil.which(exe)
            if path:
                return path

        print("{} executable not found".format(exe_name))

    def run(self, command, check_prefix=True):
        if check_prefix and not prefix.exists():
            print("This wine prefix does not exist")
            return False

        exe_path = self.find_exe("wine", ['wine-development', 'wine'])
        if not exe_path:
            return False

        os.environ['WINEPREFIX'] = str(self.path)
        if isinstance(command, str):
            if re.match(r'[\'"]?/', command):
                return subprocess.run([exe_path, 'start', '/unix'] + shlex.split(command))
            else:
                return subprocess.run([exe_path] + shlex.split(command))
        else:
            return subprocess.run(command)

    def create(self, update=False):
        exe_path = self.find_exe('wineboot', ['wineboot-development', 'wineboot'])
        if not exe_path:
            return False

        if not self.exists():
            self.path.mkdir(parents=True)
            r = self.run([exe_path, '-i'], check_prefix=False)
        elif update:
            r = self.run([exe_path, '-u'], check_prefix=False)
        else:
            return True
        return r.returncode == 0

    def configure(self):
        exe_path = self.find_exe('winecfg', ['winecfg-development', 'winecfg'])
        if not exe_path:
            return False

        if not self.exists():
           return False

        return self.run([exe_path])

    def shutdown(self):
        exe_path = self.find_exe("wineserver", ['wineserver-development', 'wineserver'])
        if not exe_path:
            return False

        os.environ['WINEPREFIX'] = str(self.path)

        return subprocess.run([exe_path, '--kill', '--wait'])

    def debug(self):
        exe_path = self.find_exe("winedbg", ['winedbg-development', 'winedbg'])
        if not exe_path:
            return False

        os.environ['WINEPREFIX'] = str(self.path)

        r = subprocess.run([exe_path, '--command', 'info process'])
        if not r:
            return False

        return subprocess.run([exe_path])



# errors deferred for completion, returning None instead
def load_config():
    config_path = '~/.config/wine-ctl.yml'
    try:
        stream = open(Path(config_path).expanduser(), 'r')
    except Exception as e:
        print("Unable to open configuration file ({})".format(config_path))
        return None
    try:
        config = yaml.safe_load(stream)
    except Exception as e:
        print("configuration file could not be parsed (not a valid YAML file)")
        return None

    config_schema = """
    type: object
    properties:
      app_lib_path:
        type: string
      install_path:
        type: string
      home_skel:
        type: string
      env:
        type: object
        additionalProperties:
          type: [string, 'null']
      bin_path_schemes:
        type: object
        additionalProperties:
          type: object
          properties:
            wine:
              type: string
            wineboot:
              type: string
            winecfg:
              type: string
            winedbg:
              type: string
            wineserver:
              type: string
            winetricks:
              type: [string, 'null']
            'dxvk-setup':
              type: [string, 'null']
          additionalProperties: False
      default_bin_path_scheme:
        type: string
    required: ['install_path']
    additionalProperties: False
    """
    try:
        jsonschema.validate(config, yaml.safe_load(config_schema))
    except jsonschema.exceptions.ValidationError as e:
        print("configuration error: {}".format(e.message))
        return None

    return config


def find_and_launch(path, lnk=False):
    path = path.resolve()

    if lnk:
        orig_path = path
        path = orig_path.joinpath('drive_c', 'users', 'Public', 'Start Menu', 'Programs')
        if not path.exists():
            path = orig_path.joinpath('drive_c', 'users', 'Public', 'Desktop')
        file_pattern = "*.lnk"
        exe_ignore_re = re.compile(r"(Uninstall)", flags=re.IGNORECASE)
        classic_path_parts = ['drive_c', 'users', 'Public', 'Start Menu', 'Programs', 'Desktop']
    else:
        file_pattern = "*.exe"
        exe_ignore_re = re.compile(r"(/(windows|Windows NT|Internet Explorer|Windows Media Player|Temp|Application Data|InstallShield Installation Information|Common Files|Unity)/|unins\d+.exe|vc_?redist)", flags=re.IGNORECASE)
        classic_path_parts = ['drive_c', 'Program Files', 'Program Files (x86)', 'GOG Games']

    l = {}
    for root, dirs, files in os.walk(path):
        for name in files:
            item = Path(root).joinpath(name)
            if fnmatch.fnmatch(name, file_pattern) and not exe_ignore_re.search(str(item)):
                item_path_parts = item.relative_to(path).parts
                item_useful_parts = [i for i in item_path_parts if i not in classic_path_parts]
                item_name = str(Path(*item_useful_parts))
                if lnk:
                    item_name = item_name[0:-4]
                l[item_name] = item

    if len(l) == 0:
        print("-- no selection available --")
        return False

    l_names = sorted(l)

    for idx, item_name in enumerate(l_names):
        print("  {}: {}".format(idx, item_name))
    c = input("Selection (enter to exit): ")
    if c and c.isdigit() and int(c) < len(l):
        return prefix.run('"{}"'.format(l[l_names[int(c)]]))
    return False


def find_prefixes(config):
    l = []
    with os.scandir(config['install_path']) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_dir():
                if Path(config['install_path']).joinpath(entry.name, 'dosdevices').is_dir():
                    l.append(entry.name)
    return l


def action_list(config, args):
    print("List of Wine prefixes:")

    l_prefixes = find_prefixes(config)

    l = {}
    for item in l_prefixes:
        in_lib = Path(config['app_lib_path']).joinpath(item).exists() if 'app_lib_path' in config else False
        l[item] = in_lib

    for app in sorted(l):
        lib_flag = 'L' if l[app] else ' '
        print("{}  {}".format(lib_flag, app))


def action_create(config, prefix, args):
    if args.lib:
        if 'app_lib_path' not in config:
            print("library path (app_lib_path) not defined in configuration")
            exit(1)

        app_path = Path(config['app_lib_path']).joinpath(prefix.name)
        if not app_path.exists():
            print("application '{}' is not in library".format(prefix.name))
            exit(1)

    if not prefix.create(update=args.update):
        print("prefix preparation failed")
        exit(2)

    if 'home_skel' in config:
        user_win_home = prefix.path.joinpath('drive_c', 'users', os.environ['USER'])
        user_win_home.mkdir(parents=True, exist_ok=True)
        # distutils.dir_util.copy_tree fails to update symlinks with "File exists"
        #copy_tree(config['home_skel'], str(user_win_home), preserve_symlinks=True, update=True)
        r = subprocess.run(['cp', '-a', config['home_skel'], str(user_win_home)])
        if r.returncode != 0:
            print("could not update the user home with the skeleton")
            exit(2)

    if not args.lib:
        return

    print("Available Installers:")
    r = find_and_launch(app_path)
    if r and r.returncode != 0:
        print("Installation failed")
        exit(2)


def action_config(config, prefix, args):
    r = prefix.configure()
    if r and r.returncode != 0:
        print("Execution failed")
        exit(2)


def action_run(config, prefix, args):
    if args.executable:
        r = prefix.run(args.executable)
    else:
        launch_type = "Executables" if args.exe else "Shortcuts"
        print("Available {}:".format(launch_type))
        r = find_and_launch(prefix.path, lnk=(not args.exe))
    if r and r.returncode != 0:
        print("Execution failed")
        exit(2)


def action_dxvk(config, prefix, args):
    if not args.action:
        test_lib = prefix.path.joinpath('dosdevices', 'c:', 'windows', 'system32', 'dxgi.dll')
        status = "installed" if 'dxvk' in str(test_lib.resolve()) else "not installed"
        print("DXVK is {}".format(status))
        exit(0)

    exe_path = prefix.find_exe('dxvk-setup', ['dxvk-setup'])
    if not exe_path:
        exit(2)

    r = prefix.run([exe_path, args.action, '-d'])
    if r and r.returncode != 0:
        print("Execution failed")
        exit(2)


def action_trick(config, prefix, args):
    exe_path = prefix.find_exe('winetricks', ['winetricks'])
    if not exe_path:
        exit(2)

    r = prefix.run([exe_path, args.trick])
    if r and r.returncode != 0:
        print("Execution failed")
        exit(2)


def dosbox_conf_unix_convert(path):
    cfile = tempfile.NamedTemporaryFile()

    print(path)
    with open(path, "r", encoding='iso-8859-1') as f:
        # TODO: use := when Python 3.8 is commonplace
        #while l := f.readline():
        for l in f:
            if re.match(r'(img)?mount', l, re.IGNORECASE):
                l = l.replace("\\", "/")
            cfile.write(bytes(l, 'iso-8859-1'))
    cfile.flush()

    return cfile


def action_dosbox(config, prefix, args):
    search_path = prefix.path.joinpath('drive_c', 'GOG Games')

    # GOG layout
    games = {}
    for root, dirs, files in os.walk(search_path):
        for f in files:
            r = re.match(r'(?P<confprefix>dosbox_?[^_]+)\.conf$', f)
            if r:
                game_path = Path(root)
                game_name = game_path.name
                game_confprefix = r.group('confprefix')

                # usual path when single game
                game_workdir = game_path.joinpath('DOSBOX')
                if not game_workdir.is_dir():
                    # shared DOSBOX files when game pack
                    game_workdir = game_path.joinpath('..', 'DOSBOX')
                    if not game_workdir.is_dir():
                        continue

                game_base_config = game_path.joinpath(game_confprefix + '.conf')
                game_launcher_config = game_path.joinpath(game_confprefix + '_single.conf')
                game_settings_config = game_path.joinpath(game_confprefix + '_settings.conf')

                if not game_workdir.joinpath(game_launcher_config).exists():
                    continue
                games[game_name] = {
                    'workdir': game_workdir,
                    'conffiles': [game_base_config, game_launcher_config]
                }

                if game_workdir.joinpath(game_settings_config).exists():
                    games[game_name + ' (settings)'] = {
                        'workdir': game_workdir,
                        'conffiles': [game_base_config, game_settings_config]
                    }

    if len(games) == 0:
        print("-- no selection available --")
        exit(0)

    custom_config = Path('~/.config/wine-ctl_dosbox.conf').expanduser()
    has_custom_config = custom_config.exists()

    gamelist = sorted(games)
    for idx, game_name in enumerate(gamelist):
        print("  {}: {}".format(idx, game_name))
    c = input("Selection (enter to exit): ")
    if c and c.isdigit() and int(c) < len(gamelist):
        game = games[gamelist[int(c)]]
        os.chdir(game['workdir'])
        command = ['dosbox']
        game['fixedconfig'] = []
        for f in game['conffiles']:
            cf = dosbox_conf_unix_convert(f)
            # temporary files need to survive during wine-ctl run
            game['fixedconfig'].append(cf)
            command += ['-conf', str(cf.name)]
        if has_custom_config:
            command += ['-conf', str(custom_config)]
        r = prefix.run(command)
        if r and r.returncode != 0:
            print("Execution failed")
            exit(2)


def action_scummvm(config, prefix, args):
    games = {}
    parse_game = re.compile(r'(?P<id>\w+:\w+) +(?P<name>[\w :()/]+?) +(?P<path>/[\w /_-]+)')
    # limit path because scanning the whole prefix take too long
    for subpath in ['Program Files', 'Program Files (x86)', 'GOG Games']:
        search_path = prefix.path.joinpath('drive_c', subpath)
        if not search_path.exists():
            continue
        r = subprocess.run(['scummvm', '--detect', '--recursive', '-p', search_path], capture_output=True)
        if r.returncode != 0:
            print("Scanning for scummvm games failed: {}".format(r.stderr.decode("utf-8")))
            exit(2)
        for line in r.stdout.decode("utf-8").splitlines():
            m = parse_game.match(line)
            if m:
                games[m.group('name')] = m.groupdict()

    if len(games) == 0:
        print("-- no selection available --")
        exit(0)

    gamelist = sorted(games)
    for idx, game_name in enumerate(gamelist):
        print("  {}: {}".format(idx, game_name))
    c = input("Selection (enter to exit): ")
    if c and c.isdigit() and int(c) < len(gamelist):
        game = games[gamelist[int(c)]]
        os.chdir(game['path'])
        r = prefix.run(['scummvm', '--fullscreen', game['id']])
        if r and r.returncode != 0:
            print("Execution failed")
            exit(2)


def find_library_programs(config):
    l = []
    with os.scandir(config['app_lib_path']) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_dir():
                l.append(entry.name)
    return l

def action_library(config, args):
    if 'app_lib_path' not in config:
        print("library path (app_lib_path) not defined in configuration")
        exit(1)

    print("List of Library Programs:")

    l_progs = find_library_programs(config)

    l = {}
    for item in l_progs:
        in_prefix = Path(config['install_path'], item).exists()
        app_path = Path(config['app_lib_path'], item)
        has_win_inst = bool(list(app_path.glob('**/*.exe')))
        has_lin_inst = bool(list(app_path.glob('**/*.sh')))
        l[item] = {
            'in_prefix': in_prefix,
            'has_win_inst': has_win_inst,
            'has_lin_inst': has_lin_inst,
        }

    for app in sorted(l):
        inst_flag = 'I' if l[app]['in_prefix'] else ' '
        has_win_inst_flag = 'w' if l[app]['has_win_inst'] else ' '
        has_lin_inst_flag = 'l' if l[app]['has_lin_inst'] else ' '
        print("{}  {}{}  {}".format(inst_flag, has_win_inst_flag, has_lin_inst_flag, app))


def action_shutdown(config, prefix, args):
    prefix.shutdown()


def action_debug(config, prefix, args):
    prefix.debug()



if __name__ == "__main__":

    config = load_config()

    if config:
        PrefixesCompleter = ChoicesCompleter(find_prefixes(config))
        if 'app_lib_path' in config:
            LibraryPrograms = ChoicesCompleter(find_library_programs(config))
        else:
            LibraryPrograms = SuppressCompleter()
    else:
        PrefixesCompleter = SuppressCompleter()
        LibraryPrograms = SuppressCompleter()

    # declare available subcommands and options
    parser = argparse.ArgumentParser(description='Manage Wine Prefixes')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s {}'.format(VERSION))
    parser.add_argument('--quiet', '-q', action='store_true', help='less verbose display')
    parser.add_argument('--bin-path-scheme', '-s', help="Binaries Path Scheme")
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_list = subparsers.add_parser('list', help='list Wine prefixes')
    parser_list.set_defaults(func=action_list)

    parser_create = subparsers.add_parser('create', help='create a new Wine prefix')
    parser_create.set_defaults(func=action_create)
    parser_create.add_argument('--lib', '-l', action='store_true', help='search installer in library')
    parser_create.add_argument('--update', '-u', action='store_true', help='rerun wineboot even if the prefix already exist')
    parser_create.add_argument('name', help='Wine prefix name').completer = LibraryPrograms

    parser_config = subparsers.add_parser('config', help='configure a Wine prefix (shorthand for running winecfg)')
    parser_config.set_defaults(func=action_config)
    parser_config.add_argument('name', help='Wine prefix name').completer = PrefixesCompleter

    parser_run = subparsers.add_parser('run', help='run application in the Wine prefix')
    parser_run.set_defaults(func=action_run)
    parser_run.add_argument('name', help='Wine prefix name').completer = PrefixesCompleter
    parser_run.add_argument('executable', nargs='?', help='optional path of the executable to run (or choice of available exe in the prefix)').completer = FilesCompleter(directories=False)
    parser_run.add_argument('--exe', '-e', action='store_true', help='look for executables instead of shorcuts')

    parser_dxvk = subparsers.add_parser('dxvk', help='setup DXVK support')
    parser_dxvk.set_defaults(func=action_dxvk)
    parser_dxvk.add_argument('name', help='Wine prefix name').completer = PrefixesCompleter
    parser_dxvk.add_argument('action', nargs='?', choices=('i', 'u'), help='install or uninstall DXVK (the default is to inform if installed)')

    parser_trick = subparsers.add_parser('trick', help='install winetrick component')
    parser_trick.set_defaults(func=action_trick)
    parser_trick.add_argument('name', help='Wine prefix name').completer = PrefixesCompleter
    parser_trick.add_argument('trick', help='winetricks component to install').completer = SuppressCompleter

    parser_dosbox = subparsers.add_parser('dosbox', help='search and run dosbox games')
    parser_dosbox.set_defaults(func=action_dosbox)
    parser_dosbox.add_argument('name', help='Wine prefix name').completer = PrefixesCompleter

    parser_scummvm = subparsers.add_parser('scummvm', help='search and run scummvm games')
    parser_scummvm.set_defaults(func=action_scummvm)
    parser_scummvm.add_argument('name', help='Wine prefix name').completer = PrefixesCompleter

    parser_library = subparsers.add_parser('library', help='list programs in library')
    parser_library.set_defaults(func=action_library)

    parser_shutdown = subparsers.add_parser('shutdown', help='Shutdown Wine prefix')
    parser_shutdown.set_defaults(func=action_shutdown)
    parser_shutdown.add_argument('name', help='Wine prefix name').completer = PrefixesCompleter

    parser_debug = subparsers.add_parser('debug', help='Run Wine debugger')
    parser_debug.set_defaults(func=action_debug)
    parser_debug.add_argument('name', help='Wine prefix name').completer = PrefixesCompleter

    # autocompletion
    argcomplete.autocomplete(parser)

    # deferred for completion
    if not config:
        exit(1)

    # let's parse
    args = parser.parse_args()



    # set environment
    if 'env' in config:
        for e_var, e_val in config['env'].items():
            if e_val:
                os.environ[e_var] = str(e_val)
            elif e_var in os.environ:
                os.environ.pop(e_var)

    # action!
    if hasattr(args, 'func'):
        if hasattr(args, 'name'):
            prefix = WinePrefix(config, args.name, args.bin_path_scheme)
            exit(args.func(config, prefix, args))
        else:
            exit(args.func(config, args))
    else:
        parser.print_help()

