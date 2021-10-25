#!/usr/bin/env python3
"""This file contains the useful functions to handle modelling problem. 
NOTE: it needs to be placed in the services directory to work properly."""
import subprocess, os, json

from bot_interface import service_server_requires_and_gets_file_of_handle


def get_problem_path_from(you_service_file_path):
    """Call this with: get_problem_path_from(__file__)"""
    service_dir_path = os.path.abspath(os.path.dirname(you_service_file_path))
    return os.path.join(service_dir_path, '../')


class ModellingProblemHelper():
    def __init__(self,
                problem_path,                            \
                tmp_dirname       = 'tmp97815',          \
                mod_filename      = 'model.mod',         \
                dat_filename      = 'instance.dat',      \
                sol_filename      = 'solution.txt',      \
                out_filename      = 'output.txt',        \
                err_filename      = 'error.txt',         \
                inputs_dirname    = 'inputs',            \
                gendict_filename  = 'gen_dictionary.json'):
        self.__problem_path = problem_path
        self.__tmp_path     = os.path.join(problem_path, tmp_dirname)
        self.__mod_path     = os.path.join(problem_path, tmp_dirname, mod_filename)
        self.__dat_path     = os.path.join(problem_path, tmp_dirname, dat_filename)
        self.__sol_path     = os.path.join(problem_path, tmp_dirname, sol_filename)
        self.__out_path     = os.path.join(problem_path, tmp_dirname, out_filename)
        self.__err_path     = os.path.join(problem_path, tmp_dirname, err_filename)
        self.__inputs_path  = os.path.join(problem_path, inputs_dirname)
        self.__gendict_path = os.path.join(problem_path, 'gen', gendict_filename)


    # TODO: fix PermissionError:
    def __del__(self):
        """Remove TMP_DIR"""
        # os.remove(self.__tmp_path)


    # MANAGE TMP_DIR FILES ---------------------------
    def __init_tmp_dir(self):
        """Creates a folder where to store the temporary files needed by the service. Our goal is that this should work whether the service is run in local or on a server."""
        if not os.path.exists(self.__tmp_path):
            os.makedirs(self.__tmp_path)


    def receive_mod_file(self):
        """Enable the service to recive the mod file."""
        # Initialize TMP_DIR
        self.__init_tmp_dir()
        # Manage mod file
        mod = service_server_requires_and_gets_file_of_handle('mod').decode()
        try:
            with open(self.__mod_path, 'w') as mod_file:
                mod_file.write(mod)
        except os.error as err:
            raise RuntimeError('write-error', self.__mod_filename, err)


    def receive_dat_file(self):
        """Enable the service to recive the dat file."""
        # Initialize TMP_DIR
        self.__init_tmp_dir()
        # Manage dat file
        dat = service_server_requires_and_gets_file_of_handle('dat').decode()
        try:
            with open(self.__dat_path, 'w') as dat_file:
                dat_file.write(dat)
        except os.error as err:
            raise RuntimeError('write-error', self.__dat_filename, err)


    def receive_input_file(self):
        """Enable the service to recive the input file then return the input in a string form."""
        # Initialize TMP_DIR
        self.__init_tmp_dir()
        # Manage input file
        return service_server_requires_and_gets_file_of_handle('input').decode()


    def run_GLPSOL(self, dat_file_path=None):
        """launches glpsol on the .mod and .dat files contained in TMP_DIR. The stdout, stderr and solution of glpsol are saved in files."""
        # Get file dat path
        if not dat_file_path:
            dat_file_path = self.__dat_path
        
        # Get files for stdoutRun GPLSOL
        try:
            with open(self.__out_path, 'w') as out_file:
                try:
                    with open(self.__err_path, 'w') as err_file:
                        # RUN gplsol
                        subprocess.run([
                            "glpsol", 
                            "-m", self.__mod_path, 
                            "-d", dat_file_path,
                        ], cwd=self.__tmp_path, timeout=30.0, stdout=out_file, stderr=err_file)
                except os.error as err:
                    raise RuntimeError('write-error', self.__err_filename, err)
                except Exception as err:
                    raise RuntimeError('process-exception', err)
                except subprocess.TimeoutExpired as err:
                    raise RuntimeError('process-timeout', err)
                except subprocess.CalledProcessError as err: 
                    raise RuntimeError('process-call', err)
        except os.error as err:
            raise RuntimeError('write-error', self.__out_filename, err)


    def get_out_str(self):
        """Return a string that contains the stdout of GPLSOL."""
        try:
            with open(self.__out_path, 'r') as file:
                return file.read()
        except os.error as err:
            raise RuntimeError('stdout-read-error', err)


    def get_err_str(self):
        """Return a string that contains the stderr of GPLSOL."""
        try:
            with open(self.__err_path, 'r') as file:
                return file.read()
        except os.error as err:
            raise RuntimeError('stderr-read-error', err)


    def get_raw_solution(self):
        """Return a list of string that contains the solution produced by GPLSOL. Remember to call a soluion_parsing function."""
        try:
            with open(self.__sol_path, 'r') as file:
                return file.read().splitlines()
        except os.error as err:
            raise RuntimeError('solution-read-error', err)


    # MANAGE INPUTS/GENDICT FILES -------------------
    def get_path_from_id(self, id, format):
        """Returns the path to the file selected with id."""
        assert id >= 0, "Id not valid."
        try:
            with open(self.__gendict_path, 'r') as file:
                gendict = json.load(file)
                info = gendict[str(id)]
                return os.path.join(self.__inputs_path, info['suite'], info[format])
        except os.error as err:
            raise RuntimeError('read-error', self.__gendict_path)
        except KeyError as err:
            raise RuntimeError('invalid-id', id)


    def get_input_from_path(self, path):
        """Returns the instance from the input from the selected path."""
        try:
            with open(path, 'r') as file:
                return file.read().strip()
        except os.error as err:
            raise RuntimeError('read-error', self.__gendict_path)


    def get_input_from_id(self, id, format):
        """Returns the instance from the input file with the selected id."""
        return self.get_input_from_path(self.get_path_from_id(id, format))


    def get_instances_paths_in(self, dir_name):
        """Returns the list of all file_path in the inputs directory grouped by instance"""
        assert isinstance(dir_name, str)
        try:
            dir_path = os.path.join(self.__inputs_path, dir_name)
            instances_paths = dict()
            for filename in os.listdir(dir_path):
                tmp_parse = filename.split('.')
                id = tmp_parse[0][len('instance'):]
                format = ".".join(tmp_parse[1:])
                if id not in instances_paths:
                    instances_paths[id] = {format : os.path.join(dir_path, filename)}
                else:
                    instances_paths[id][format] = os.path.join(dir_path, filename)
            return instances_paths
        except os.error as err:
            raise RuntimeError('read-error', self.__inputs_path)