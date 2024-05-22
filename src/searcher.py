import os
import dataset
import unittest
import datetime
from typing import Literal


SearcherQueryKind = Literal["word token"]


SearcherQueryBody = str


class SearcherQuery:
    """
    A wrapper class to hold the kind of search and its body used for search.
    """

    def __init__(self, kind: SearcherQueryKind, body: SearcherQueryBody):
        self.kind = kind
        self.body = body


class SearcherResultElement:
    """
    One element the `SearcherResult` will holds.
    """

    def __init__(self, left: list[str], target: list[str], right: list[str]):
        self.left = left
        self.target = target
        self.right = right

    def left_visual_len(self):
        left_len = len(self.left)
        for s in self.left:
            left_len += len(s)
        return left_len


class SearcherResult:
    """
    The result of search `Searcher.search` will returns.
    """

    def __init__(
        self, number: int, body: str, result: list[SearcherResultElement]
    ):
        self.number = number
        self.body = body
        self.result = result

    def colorize(self):
        left_len = 0
        for element in self.result:
            left_len = max(left_len, element.left_visual_len())
        for element in self.result:
            print(" " * (left_len - element.left_visual_len()), end="")
            for s in element.left:
                print(s + " ", end="")
            print("\033[31m", end="")
            for s in element.target:
                print(s + " ", end="")
            print("\033[0m", end="")
            for s in element.right:
                print(s + " ", end="")
            print()

    def save(self, path: str | os.PathLike):
        date = datetime.datetime.today().date()
        date = "{:04}{:02}{:02}".format(date.year, date.month, date.day)
        time = datetime.datetime.today().time()
        time = "{:02}{:02}".format(time.hour, time.minute)
        path = "{:03}-{}-{}-{}".format(self.number, date, time, self.body)
        with open(path, mode="w+") as f:
            for element in self.result:
                f.write("left: ")
                for s in element.left:
                    f.write(s + " ")
                f.write("\n")
                f.write("target: ")
                for s in element.target:
                    f.write(s + " ")
                f.write("\n")
                f.write("right: ")
                for s in element.right:
                    f.write(s + " ")
                f.write("\n")


class Searcher:
    """
    A class which provide a operation on specified dataset.
    """

    def __init__(self, database: str | os.PathLike):
        self.counter = 0
        self.manager = dataset.DatasetManager(database)

    def __del__(self):
        del self.manager

    def search(self, query: SearcherQuery) -> SearcherResult:
        names = self.manager.retrieve_names()
        result = []
        for name in names:
            text = self.manager.retrieve(name).split()
            text_size = len(text)
            for j in range(text_size):
                if (text[j] == query.body):
                    left = []
                    mid = []
                    right = []
                    for k in range(max(0, j-11), j-1):
                        left.append(text[k])

                    for k in range(j+1, min(j+11, text_size)):
                        right.append(text[k])

                    mid.append(text[j])
                    result.append(SearcherResultElement(left, mid, right))
        number = self.counter
        self.counter += 1
        return SearcherResult(number, query.body, result)


class TestSearcher(unittest.TestCase):
    def test_search(self):
        pass


if __name__ == "__main__":
    unittest.main()
