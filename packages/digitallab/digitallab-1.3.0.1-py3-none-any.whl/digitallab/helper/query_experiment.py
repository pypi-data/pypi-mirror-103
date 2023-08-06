#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from pymongo import MongoClient
import json


class ExperimentQuery:
    def __init__(self, mongodb_url, database, collection="runs", rerun_non_optimal=False):
        self.rerun_non_optimal = rerun_non_optimal
        self.mongodb_url = mongodb_url
        self.database = database
        self.collection = collection
        self.client = None
        self.db = None
        self.coll = None

    def open_connection(self):
        self.client = MongoClient(self.mongodb_url)
        self.db = self.client[self.database]
        self.coll = self.db[self.collection]

    def close_connection(self):
        self.client.close()

    def is_experiment_eligible(self, config):
        essential_keys = ("number_of_repetitions", "version")
        for k in essential_keys:
            if k not in config.keys():
                raise KeyError

        if self.coll.count() > 0:
            query = dict()
            query2 = dict()
            for key, value in config.items():
                if key not in ("number_of_repetitions", "time_limit"):
                    query["config." + key] = value
                    query2["config." + key] = value
            query["status"] = "COMPLETED"
            query2["status"] = "RUNNING"
            if self.rerun_non_optimal:
                query["result.optimal"] = True
                query2["result.optimal"] = True
            if self.coll.find(query).count() < 1 and self.coll.find(query2).count() < 1:
                return True
            return False
        return True


def query_experiment_eligible(mongodb_url, database, config, collection="runs", rerun_non_optimal=False):
    experiment_query = ExperimentQuery(mongodb_url, database, collection, rerun_non_optimal=rerun_non_optimal)
    experiment_query.open_connection()
    b = experiment_query.is_experiment_eligible(config)
    experiment_query.close_connection()
    return b


def query_experiments_eligible(mongodb_url, database, configs, collection="runs", rerun_non_optimal=False):
    experiment_query = ExperimentQuery(mongodb_url, database, collection, rerun_non_optimal=rerun_non_optimal)
    bool_list = []
    experiment_query.open_connection()
    for conf in configs:
        bool_list.append(experiment_query.is_experiment_eligible(conf))
    experiment_query.close_connection()
    return bool_list
