import collections
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple
import statistics 
import mosspy
from bs4 import BeautifulSoup as bs

HEADERS = {"User-Agent": "Mozilla/5.0"}


class Result(dict):
    """Typing for moss results"""

    file1: str
    file2: str
    percentage: int
    no_of_lines_matched: int
    lines_matched: List[List[str]]


Results = List[Result]


def perc_str_to_int(string: str) -> int:
    """Convert string like "(42%)" to 42"""
    match = re.search(r"\((\d+)%\)$", string)
    if match:
        return int(match.group(1))
    raise ValueError("Cannot find percentage in table")


def request(url: str):
    """Request Webpage"""
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as response:
        req = response.read()

    return req.decode("utf-8")


def share_scores(moss_data: dict) -> dict:
    """Share Score Insights"""
    similar_code_files = []
    for result in moss_data:
        similar_code_files.append(result["file1"])
        similar_code_files.append(result["file2"])

    # frequency of files which are similar
    share_score = collections.Counter(similar_code_files)

    return dict(share_score)


class check:
    """
    Args:
        - Program Files (list)
        - Language (str)
        - Moss User ID (str)
    """

    def __init__(self, lang: str, user_id: str):

        self.__user_id = user_id
        languages = mosspy.Moss.languages
        if lang not in languages:
            raise ValueError(f"{lang} is not a supported language {languages}")
        self.lang = lang
        self.__moss = mosspy.Moss(self.__user_id, self.lang)

    def __extract_info(self) -> Results:
        """Scrape the webpage for file names, percentage match etc."""
        results: Results = []

        response = request(self.home_url)

        html = bs(response, "lxml")
        table = html.find("table")
        for row in table.find_all("tr")[1:]:
            col1, col2, col3 = row.find_all("td")
            filename1, perc1 = col1.text.strip().split()
            filename2, perc2 = col2.text.strip().split()

            with ThreadPoolExecutor() as executor:
                future = executor.submit(self.__get_line_numbers, col1.a.get("href"))
                lines = future.result()

            result_dict = Result(
                file1=filename1,
                file2=filename2,
                percentage_file1=perc_str_to_int(perc1),
                percentage_file2=perc_str_to_int(perc2),
                no_of_lines_matched=int(col3.text.strip()),
                lines_matched=lines,
            )
            results.append(result_dict)
        return results

    def __get_line_numbers(self, url: str) -> List[List[str]]:
        """Get Line Numbers which are same"""
        list_of_line_nos: List[List[str]] = []
        result_page = re.sub(r".html$", "-top.html", url)

        response = request(result_page)

        html = bs(response, "lxml")
        table = html.find("table")
        for row in table.find_all("tr")[1:]:
            matched_lines: List[str] = []
            for col in row.find_all("td"):
                line_nos: str = col.text.strip()
                if line_nos:
                    matched_lines.append(line_nos)
            list_of_line_nos.append(matched_lines)
        return list_of_line_nos

    def addFilesByWildCard(self, files):
        """Add multiple files"""
        self.__moss.addFilesByWildcard(files)

    def submit(self):
        """Submit files to the Moss Server"""
        url = self.__moss.send()

        self.home_url = url
        self.moss_results = self.__extract_info()

    def getHomePage(self):
        """Return Moss Results HomePage URL"""
        return self.home_url

    def getResults(self) -> Tuple[str, Results]:
        """Return the result as a list of dictionary"""

        return self.moss_results




##########################################
import os
def generate_results(language,path,marks):    
    extension=None
    if language=="python":
        extension="py"
    else:
        extension="java"
    userid = 942197121
    moss = check(language, userid)
    moss.addFilesByWildCard(f"{path}*.{extension}")
    moss.submit()
    result = moss.getResults()
    final=share_scores(result)
    arr=[]
    for ele in final:
        final[ele]=marks/final[ele]
        arr.append(final[ele])
    mean="NA"
    median="NA"
    mean="NA"
    maximum="NA"
    minimum="NA"
    try:
        mean=statistics.mean(arr)
    except Exception:
        pass
    try:
        median=statistics.median(arr)
    except Exception:
        pass
    try:
        minimum=min(arr)
    except Exception:
        pass
    try:
        maximum=max(arr)
    except Exception:
        pass
    output=[str(ele)+"="+str(final[ele]) for ele in final]
    output+=["mean="+str(mean),"median="+str(median),"minimum="+str(minimum),"maximum="+str(maximum),"total="+str(marks)]
    return "\n".join(output)

import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', type=str, default="python",help='language?')
    parser.add_argument('--path',type=str)
    parser.add_argument('--marks',type=int)
    args = parser.parse_args()
    print(generate_results(args.language,args.path,args.marks))
    
if __name__ == '__main__':
    main()
