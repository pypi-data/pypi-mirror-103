#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import datetime
import functools
import json
import logging
import random
import types
from functools import partial
from itertools import compress
from logging.handlers import RotatingFileHandler

# from pathos.multiprocessing import ProcessPool as Pool
from multiprocessing import Pool
from typing import Union

from sacred import Experiment
from sacred.observers import MongoObserver

from digitallab.helper.chunks import divide_into_chunks
from digitallab.helper.db_access import DBAccess
from digitallab.helper.experiment_setting import ExperimentSetting, ExperimentConfigs
from digitallab.helper.generate_seeds import generate_seeds_from_json
from digitallab.helper.output import *
from digitallab.helper.query_experiment import query_experiments_eligible, query_experiment_eligible


def run_with_separate_interpreter(interpreter="python3", temporary_folder="./"):
    def remove_decorators_from_source_code(source_code):
        count = 0
        for line in source_code[0]:
            if line[0] == "@":
                count += 1
            else:
                break
        return source_code[0][count:]

    def build_python_file_text(source_code, ident, function_name):
        code = [
                   'import json\n',
                   'import traceback\n',
                   '\n',
               ] + remove_decorators_from_source_code(source_code) + [
                   '\n'
                   'with open("' + temporary_folder + 'dlab_tmp_config_' + ident + '.json") as f:\n',
                   '    config = json.load(f)\n',
                   'try:\n'
                   '    ret = ' + function_name + '(config)\n',
                   '    with open("' + temporary_folder + 'dlab_tmp_result_' + ident + '.json", "w") as json_file:\n',
                   '        json.dump(ret, json_file)\n',
                   'except Exception as e:\n',
                   '    error_string = traceback.format_exc()\n',
                   '    with open("' + temporary_folder + 'dlab_tmp_error_' + ident + '.txt", "w") as f:\n',
                   '        f.write(error_string)\n'
               ]
        return code

    def specialized_decorator(fn):
        @functools.wraps(fn)
        def wrapper(_config):
            salt = random.randint(-1e8, 1e8)
            ident = str(hash(frozenset(_config.items())) + hash(salt))
            while os.path.isfile(temporary_folder + "dlab_tmp_script_" + ident + ".py"):
                salt = random.randint(-1e8, 1e8)
                ident = str(hash(_config) + hash(salt))

            source_code = inspect.getsourcelines(fn)
            function_name = fn.__name__
            code = build_python_file_text(source_code, ident, function_name)
            with open(temporary_folder + "dlab_tmp_script_" + ident + ".py", "w") as f:
                for line in code:
                    f.write(line)
            with open(temporary_folder + "dlab_tmp_config_" + ident + ".json", "w") as json_file:
                json.dump(_config, json_file)
            status = os.system(interpreter + " " + temporary_folder + "dlab_tmp_script_" + ident + ".py")
            if status != 0:
                if os.path.isfile(temporary_folder + "dlab_tmp_config_" + ident + ".json"):
                    os.remove(temporary_folder + "dlab_tmp_config_" + ident + ".json")
                os.remove(temporary_folder + "dlab_tmp_script_" + ident + ".py")
                raise RuntimeError("Unknown error which could not be catched thrown by interpreter.")
            if os.path.isfile(temporary_folder + "dlab_tmp_error_" + ident + ".txt"):
                with open(temporary_folder + "dlab_tmp_error_" + ident + ".txt") as f:
                    error = f.readlines()
                os.remove(temporary_folder + "dlab_tmp_error_" + ident + ".txt")
                os.remove(temporary_folder + "dlab_tmp_config_" + ident + ".json")
                os.remove(temporary_folder + "dlab_tmp_script_" + ident + ".py")
                raise ChildProcessError("".join(error))
            with open(temporary_folder + "dlab_tmp_result_" + ident + ".json") as f:
                result = json.load(f)
            os.remove(temporary_folder + "dlab_tmp_result_" + ident + ".json")
            os.remove(temporary_folder + "dlab_tmp_config_" + ident + ".json")
            os.remove(temporary_folder + "dlab_tmp_script_" + ident + ".py")
            return result

        return wrapper

    return specialized_decorator


def check_eligible(chunk, mongodb_url, mongodb_db):
    return query_experiments_eligible(mongodb_url, mongodb_db, chunk[0])


def prepare_and_run_experiment(config, ex, mongodb_url, mongodb_db, config_to_str=str):
    if query_experiment_eligible(mongodb_url, mongodb_db, config):
        with suppress_stderr():
            with redirect_to_tqdm():
                if not ex.observers:
                    ex.observers.append(MongoObserver(mongodb_url, mongodb_db))
                ex.add_config(config)
                ex.run()
        return True, config_to_str(config)
    return False, config_to_str(config)


def connect_to_mongodb(mongodb_url, mongodb_db, keys_json_path):
    DBAccess.instance().connect(mongodb_url, mongodb_db, keys_json_path)


class Lab:
    def __init__(self, name, mongodb_url, database, config_to_string_func=str):
        self.logger = None
        self.mongodb_url = mongodb_url
        self.mongodb_db = database
        self.experiment_settings = None

        self.name = name
        # self.__experiment = Experiment(name, save_git_info=False)
        self.__config_to_string_func = config_to_string_func

    def experiment(self, fn):
        experiment = Experiment(self.name, save_git_info=False)
        experiment.main(fn)
        mongodb_url = self.mongodb_url
        mongodb_db = self.mongodb_db
        config_to_string_func = str

        @functools.wraps(fn)
        def wrapper(config):
            return prepare_and_run_experiment(config, experiment, mongodb_url, mongodb_db,
                                              config_to_str=config_to_string_func)

        return wrapper

    def run_experiments(self, experiment_function, experiment_settings: Union[str, dict],
                        number_of_parallel_runs: int = 1, number_of_query_workers: int = 100,
                        number_of_query_chunks: int = 1000, path_to_log=None):
        self.experiment_settings = experiment_settings
        if path_to_log:
            self.__setup_logger(path_to_log)
        else:
            self.logger = None

        seeds = generate_seeds_from_json(self.experiment_settings)

        configs = self.__collect_possible_configs(seeds)
        configs = self.__filter_eligible_configs(configs, number_of_query_chunks, number_of_query_workers)
        random.shuffle(configs)

        if number_of_parallel_runs > 1:
            self.__execute_experiments_in_parallel(configs, experiment_function, number_of_parallel_runs)
        else:
            self.__execute_experiments_sequentially(configs, experiment_function)

    def __execute_experiments_sequentially(self, configs, experiment_func):
        for experiment_was_run, config_to_string in tqdm(map(experiment_func, configs), desc="Running experiments",
                                                         total=len(configs),
                                                         dynamic_ncols=True, file=sys.stdout, ascii=True,
                                                         colour="RED"):
            self.write_log(experiment_was_run, config_to_string)

    def __execute_experiments_in_parallel(self, configs, experiment_func, number_of_parallel_runs):
        with Pool(number_of_parallel_runs) as pool:
            for experiment_was_run, config_to_string in tqdm(pool.imap(experiment_func, configs),
                                                             desc="Running experiments", total=len(configs),
                                                             dynamic_ncols=True):
                self.write_log(experiment_was_run, config_to_string)

    def write_log(self, was_experiment_run, message):
        if self.logger:
            if was_experiment_run:
                self.logger.info("Finished Experiment:\n" + message)
            else:
                self.logger.info("Already running or finished:\n" + message)

    def __filter_eligible_configs(self, configs, number_of_query_chunks, number_of_query_workers):
        eligible = []
        chunks = divide_into_chunks(configs, number_of_query_chunks)
        with Pool(number_of_query_workers) as pool:
            for logic_chunk in tqdm(pool.imap(partial(
                    check_eligible, mongodb_url=self.mongodb_url, mongodb_db=self.mongodb_db), chunks),
                    desc="Querying eligible experiments to run",
                    total=len(chunks), dynamic_ncols=True):
                eligible += logic_chunk
        configs = list(compress(configs, eligible))
        return configs

    def __collect_possible_configs(self, seeds):
        configs = []
        setting = ExperimentSetting(self.experiment_settings)
        configs_iterator = ExperimentConfigs(setting, seeds)
        total_estimated_seconds = 0
        timelimit_found = False
        with tqdm(total=len(setting), desc="Collecting possible experiments", dynamic_ncols=True) as pbar:
            for config in configs_iterator:
                if "timelimit" in config:
                    total_estimated_seconds += config["timelimit"]
                    timelimit_found = True
                if "time_limit" in config:
                    total_estimated_seconds += config["time_limit"]
                    timelimit_found = True
                configs.append(config)
                pbar.update(1)
        if timelimit_found:
            total_estimated_timedelta = datetime.timedelta(seconds=total_estimated_seconds)
            print("Found 'timelimit' or 'time_limit' in configs. Assuming you mean seconds and assuming each run takes "
                  "as long as the time limit allows, this computation would take ", str(total_estimated_timedelta), ".")
        return configs

    def __setup_logger(self, path_to_log):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(path_to_log, maxBytes=1000)
        # set a formatter to include the level name
        handler.setFormatter(logging.Formatter(
            '[%(levelname)s] %(message)s'
        ))
        # add the journald handler to the current logger
        self.logger.addHandler(handler)
