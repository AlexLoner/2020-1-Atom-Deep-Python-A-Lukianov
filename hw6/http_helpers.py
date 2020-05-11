import json
import requests
import bs4
from collections import Counter
from nltk.corpus import stopwords, wordnet

class NonValidRequest(Exception):
    pass


# --------------------------------------------------------------------------------------------
class HttpParser:

    # --------------------------------------------------------------------------------------------
    def __init__(self, reqst: requests.Response):
        self.req = reqst

    # --------------------------------------------------------------------------------------------
    def __repr__(self):
        return self.req.status_code

    # --------------------------------------------------------------------------------------------
    def get_all_words(self) -> list:
        if 200 <= self.req.status_code < 300:
            page = bs4.BeautifulSoup(self.req.content, 'lxml')

            words = []
            for word in page.get_text().split():
                new_word = ''.join([i.lower() for i in word if i.isalpha() or i in ['.', '-']])
                if len(new_word) > 1 and new_word not in stopwords.words('russian') \
                                     and new_word not in stopwords.words('english'):
                    words.append(new_word)
            return words
        else:
            raise NonValidRequest(f'Check page address: response cose is {self.req.status_code}')

    # -------------------------------------------------------------------------------------------
    def top10(self) -> json:
        counter = Counter(self.get_all_words())
        tmp_lst = sorted([(key, value) for key, value in counter.items()], reverse=True, key=lambda x: x[1])
        result_dict = {str(i+1): tmp_lst[i] for i in range(10)}
        with open('top10.json', 'w') as f:
            json.dump(result_dict, f, ensure_ascii=False)
        return json.dumps(result_dict, ensure_ascii=False)
