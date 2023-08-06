#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from unittest import TestCase
from digitallab.helper.chunks import divide_into_chunks


class Test(TestCase):
    def test_divide_into_chunks1(self):
        lst = list(range(9))
        chunks = divide_into_chunks(lst, 3)
        self.assertEqual(len(chunks), 3)
        for chunk in chunks:
            self.assertEqual(len(chunk[0]), 3)

    def test_divide_into_chunks2(self):
        lst = list(range(10))
        chunks = divide_into_chunks(lst, 3)
        for i, chunk in enumerate(chunks):
            if i != len(chunks) - 1:
                self.assertEqual(len(chunk[0]), 3)
            else:
                self.assertEqual(len(chunk[0]), 4)

    def test_divide_into_chunks3(self):
        lst = list(range(360))
        chunks = divide_into_chunks(lst, 10)
        self.assertEqual(len(chunks), 10)
        for chunk in chunks:
            self.assertEqual(len(chunk[0]), 36)

    def test_divide_into_chunks4(self):
        lst = list(range(359))
        chunks = divide_into_chunks(lst, 10)
        for i, chunk in enumerate(chunks):
            if i < len(chunks) - 9:
                self.assertEqual(len(chunk[0]), 35)
            else:
                self.assertEqual(len(chunk[0]), 36)

    def test_divide_into_chunks5(self):
        lst = list(range(7128))
        chunks = divide_into_chunks(lst, 1000)
        self.assertEqual(len(chunks), 1000)
        for i, chunk in enumerate(chunks):
            if i < len(chunks) - 128:
                self.assertEqual(len(chunk[0]), 7)
            else:
                self.assertEqual(len(chunk[0]), 8)
