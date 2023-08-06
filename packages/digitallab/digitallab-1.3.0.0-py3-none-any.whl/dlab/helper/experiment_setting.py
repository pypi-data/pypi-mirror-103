#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
from typing import Union


class ExperimentConfigs:
    def __init__(self, experiment_setting, seeds):
        self.experiment_setting = experiment_setting
        self.seeds = seeds

    def __len__(self):
        return len(self.experiment_setting)

    def __iter__(self):
        for conf in self.experiment_setting:
            for i in range(conf["number_of_repetitions"]):
                modified_conf = dict(conf)
                modified_conf["id"] = i
                modified_conf["seed"] = self.seeds[i]
                yield modified_conf


class ExperimentSettingIterator:
    def __init__(self, experiment_setting):
        self.experiment_setting = experiment_setting

        self.__iterators = dict()
        self.__setup_iterator_list()
        self.__current_config = dict()
        self.__setup_first_config()
        self.__first_iteration = True
        self.__stop = False

    def __setup_iterator_list(self):
        for key in self.experiment_setting.keys:
            self.__setup_iterator(key)

    def __setup_iterator(self, key):
        if isinstance(self.experiment_setting.json_data[key], list):
            self.__iterators[key] = iter(self.experiment_setting.json_data[key])

    def __deep_copy_current_config(self):
        config = dict()
        for key in self.experiment_setting.keys:
            config[key] = self.__current_config[key]
        return config

    def __next__(self):
        if self.__stop:
            raise StopIteration
        config = self.__deep_copy_current_config()
        try:
            self.__generate_next_config()
        except StopIteration:
            self.__stop = True
        return config

    def __setup_first_config(self):
        for key in self.experiment_setting.keys:
            if key in self.__iterators.keys():
                self.__next_config_key(key)
            else:
                self.__current_config[key] = self.experiment_setting.json_data[key]

    def __generate_next_config(self):
        for key in self.experiment_setting.keys:
            if key in self.__iterators.keys():
                try:
                    self.__next_config_key(key)
                    return
                except StopIteration:
                    self.__setup_iterator(key)
                    self.__next_config_key(key)
        raise StopIteration

    def __next_config_key(self, key):
        self.__current_config[key] = next(self.__iterators[key])


class ExperimentSetting:
    def __init__(self, json_file_path_or_dict: Union[str, dict]):
        if isinstance(json_file_path_or_dict, str):
            with open(json_file_path_or_dict) as json_file:
                self.json_data = json.load(json_file)
        elif isinstance(json_file_path_or_dict, dict):
            self.json_data = json_file_path_or_dict
        else:
            raise TypeError("Argument must be either a string or a dictonary.")
        self.keys = list(self.json_data.keys())

    def __len__(self):
        count = 1
        for key in self.keys:
            try:
                if isinstance(self.json_data[key], list):
                    count *= len(self.json_data[key])
            except TypeError:
                count *= 1
        count *= self.json_data["number_of_repetitions"]
        return count

    def number_of_unique_experiments(self):
        count = 1
        for key in self.keys:
            try:
                if isinstance(self.json_data[key], list):
                    count *= len(self.json_data[key])
            except TypeError:
                count *= 1
        return count

    def __iter__(self):
        return ExperimentSettingIterator(self)
