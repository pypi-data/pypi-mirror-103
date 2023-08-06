#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest

from digitallab.helper.experiment_setting import ExperimentSetting, ExperimentConfigs
from digitallab.helper.generate_seeds import generate_seeds_from_json


class TestExperimentSetting(unittest.TestCase):
    def test_iterates_correctly1(self):
        exp_setting = ExperimentSetting("test.json")
        max_i = 0
        for i, config in enumerate(exp_setting):
            self.assertTrue("test1" in config)
            self.assertTrue("test2" in config)
            if i == 0:
                max_i = 0
                self.assertEqual(config["test1"], 1)
                self.assertEqual(config["test2"], 3)
            if i == 1:
                max_i = 1
                self.assertEqual(config["test1"], 2)
                self.assertEqual(config["test2"], 3)
            if i == 2:
                max_i = 2
                self.assertEqual(config["test1"], 1)
                self.assertEqual(config["test2"], 4)
            if i == 3:
                max_i = 3
                self.assertEqual(config["test1"], 2)
                self.assertEqual(config["test2"], 4)
        self.assertEqual(max_i, 3)

    def test_iterates_correctly2(self):
        exp_setting = ExperimentSetting("test2.json")
        for i, config in enumerate(exp_setting):
            self.assertTrue("test1" in config)
            self.assertTrue("test2" in config)
            self.assertTrue("test_no_list" in config)
            self.assertEqual(config["test_no_list"], 5)
            if i == 0:
                self.assertEqual(config["test1"], 1)
                self.assertEqual(config["test2"], 3)
            if i == 1:
                self.assertEqual(config["test1"], 2)
                self.assertEqual(config["test2"], 3)
            if i == 2:
                self.assertEqual(config["test1"], 1)
                self.assertEqual(config["test2"], 4)
            if i == 3:
                self.assertEqual(config["test1"], 2)
                self.assertEqual(config["test2"], 4)

    def test_length1(self):
        exp_setting = ExperimentSetting("test2.json")
        self.assertEqual(len(exp_setting), 16)

    def test_length2(self):
        exp_setting = ExperimentSetting("test3.json")
        self.assertEqual(len(exp_setting), 7128)

    def test_experiment_configs(self):
        seeds = generate_seeds_from_json("test3.json")
        exp_setting = ExperimentSetting("test3.json")
        exp_configs = ExperimentConfigs(exp_setting, seeds)
        for i, config in enumerate(exp_configs):
            if i > 20:
                break
            self.assertEqual(config["ridge_parameter"], 0)
            self.assertEqual(config["sigma_param"], 0)
            self.assertEqual(config["snr"], 0.3)
            self.assertEqual(config["id"], i)
            self.assertEqual(config["seed"], seeds[i])
