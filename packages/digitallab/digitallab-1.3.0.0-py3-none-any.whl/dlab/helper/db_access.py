#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import json
from functools import partial
from multiprocessing import Pool
from typing import Union

import pandas as pd
import pymongo
from pymongo import MongoClient

from digitallab.evaluation.helper.cache import Cache
from digitallab.evaluation.helper.flatten import flatten_dict
from digitallab.helper.singleton import Singleton


@Singleton
class DBAccess:
    def connect(self, mongodb_url, mongodb_db, keys_json_path_or_dict: Union[str, dict, None] = None,
                cache_id: str = "default"):
        self.mongodb_url = mongodb_url
        self.mongodb_db = mongodb_db

        if keys_json_path_or_dict is None:
            keys_json_path_or_dict = {"result": 1, "config": 1}
        if isinstance(keys_json_path_or_dict, str):
            with open(keys_json_path_or_dict) as json_file:
                self.keys = json.load(json_file)
        elif isinstance(keys_json_path_or_dict, dict):
            self.keys = keys_json_path_or_dict
        else:
            raise TypeError("Argument must be either a string or a dictonary.")
        self.json_path_or_dict = keys_json_path_or_dict
        self.client = MongoClient(self.mongodb_url)
        self.db = self.client[self.mongodb_db]
        self.is_connected = True
        self.cache_id = cache_id

    def get_dataframe(self):
        if hasattr(self, "is_connected"):
            if self.is_connected:
                coll = self.db["runs"]
                stop_time = coll.find().sort("stop_time", pymongo.DESCENDING).limit(1)[0]["stop_time"]

                cache = Cache(self.cache_id, stop_time, self.keys)

                if cache.cache is None:
                    all_docs = coll.find({"status": "COMPLETED"})
                    with Pool(8) as pool:
                        flatten_docs = pool.map(
                            partial(flatten_dict, keys=self.keys),
                            all_docs)
                    df = pd.DataFrame(flatten_docs)
                    cache.save_cache(df)
                else:
                    df = cache.cache
                return df
        raise ConnectionError("Please connect to database first.")
