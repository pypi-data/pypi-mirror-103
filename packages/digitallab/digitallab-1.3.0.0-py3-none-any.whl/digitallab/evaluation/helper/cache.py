#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import pathlib
import os
import pandas as pd
import hashlib


class Cache:
    def __init__(self, id: str, last_changed, keys: dict, dir="/tmp/"):
        assert isinstance(keys, dict)
        self._mongo_last_changed = last_changed
        self.dir = dir
        self.id = id
        self._keys_hash = hashlib.sha512(str(keys).encode("utf-8")).hexdigest()
        self.cache = None
        self._load_cache()

    def _load_cache(self):
        if os.path.isfile(self.dir + "/cache_hash_" + self.id + ".json") and os.path.isfile(
                self.dir + "/cache_" + self.id + ".h5"):
            with open(self.dir + "/cache_hash_" + self.id + ".json", "rb") as cache_hash:
                hashes = json.load(cache_hash)
            if hashes["last_changed"] == str(self._mongo_last_changed) and hashes["keys_hash"] == self._keys_hash:
                self.cache = pd.read_hdf(self.dir + "/cache_" + self.id + ".h5", "table")
            else:
                print("No cache hit. Rebuilding data.")
        else:
            print("Cache not found. Creating new cache.")

    def save_cache(self, data):
        self.cache = data
        with open(self.dir + "/cache_hash_" + self.id + ".json", "w") as cache_hash:
            d = {"last_changed": str(self._mongo_last_changed),
                 "keys_hash": self._keys_hash}
            json.dump(d, cache_hash)
        data.to_hdf(self.dir + "/cache_" + self.id + ".h5", "table", append=False)

    def clear_cache(self):
        if os.path.isfile(self.dir + "/cache_hash_" + self.id + ".json"):
            os.remove(self.dir + "/cache_hash_" + self.id + ".json")
            print("Removed " + self.dir + "/cache_hash_" + self.id + ".json")
        else:
            print("The file " + self.dir + "/cache_hash_" + self.id + ".json" +
                  " could not be found and hence was not removed.")
        if os.path.isfile(self.dir + "/cache_" + self.id + ".h5"):
            os.remove(self.dir + "/cache_" + self.id + ".h5")
            print("Removed " + self.dir + "/cache_" + self.id + ".h5")
        else:
            print("The file " + self.dir + "/cache_" + self.id + ".h5" +
                  " could not be found and hence was not removed.")
