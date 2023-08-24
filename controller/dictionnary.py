from bs4 import BeautifulSoup
import requests as req
from requests.exceptions import ConnectionError

USERAGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"

HEADERS = {"User-Agent": USERAGENT}

# fr.m.wiktionary
# url_definition = "https://fr.m.wiktionary.org/wiki/"
# url_conjugaison = "https://fr.m.wiktionary.org/wiki/"

# lerobert
url_definition = "https://dictionnaire.lerobert.com/definition/"
url_conjugaison = "https://dictionnaire.lerobert.com/conjugaison/"

def check_exist_word(word):
    # print("Check word: " + word)
    """
    :param word: The word whose definition you are looking for
    :return: A list containing all the definitions of word
    """
    try:
        URL = url_definition + word.lower()
        response = req.get(URL, headers=HEADERS)
        code = response.status_code
        
        # soup = BeautifulSoup(response.text, "html.parser")
        # section = soup.find("section", attrs={"id": "definitions"})
        if code == 200:
            # return str(section)
            # print(str(section))
            return True
        else:
            # content = soup.find("section", attrs={"class": "corrector"})
            # if content:
            #     return NOT_RESULT + str(content)
            existed_verb = check_exist_verb(word)
            return existed_verb
        return NOT_RESULT
    except ConnectionError:
        print("Connection error")
        return False

def check_exist_verb(verb):
    try:
        URL = url_conjugaison + verb.lower()
        response = req.get(URL, headers=HEADERS)
        code = response.status_code
        # soup = BeautifulSoup(response.text, "html.parser")
        # section = soup.find("div", attrs={"class": "conj_verbe"})
        if code == 200:
            # return str(section)
            # print(str(section))
            return True
        else:
            # content = soup.find("section", attrs={"class": "corrector"})
            # if content:
            #     return NOT_RESULT + str(content)
            return False
        return NOT_RESULT
    except ConnectionError:
        print("Connection error")
        return False
