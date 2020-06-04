import json
import requests
import bs4
from collections import Counter
from nltk.corpus import stopwords


# --------------------------------------------------------------------------------------------
class NonValidRequest(Exception):
    pass


# --------------------------------------------------------------------------------------------
class HttpParser:

    # --------------------------------------------------------------------------------------------
    def __init__(self, reqst):
        self.req = reqst

    # --------------------------------------------------------------------------------------------
    def get_all_words(self) -> list:
        try:
            page = bs4.BeautifulSoup(self.req, 'lxml')
            words = []
            for word in page.get_text().split():
                new_word = ''.join([i.lower() for i in word if i.isalpha() or i in ['.', '-']])
                if len(new_word) > 1 and new_word not in stopwords.words('russian') \
                                     and new_word not in stopwords.words('english'):
                    words.append(new_word)
            return words
        except:
            return [f'{self.req.url}']
            # raise NonValidRequest(f'Check page address: response code is {self.req.status_code}')

    # -------------------------------------------------------------------------------------------
    def top(self, n) -> json:
        counter = Counter(self.get_all_words())
        tmp_lst = sorted([(key, value) for key, value in counter.items()], reverse=True, key=lambda x: x[1])
        result_dict = {str(i+1): {tmp_lst[i][0]: tmp_lst[i][1]}  for i in range(min(n, len(tmp_lst)))}
        return json.dumps(result_dict, ensure_ascii=False)
