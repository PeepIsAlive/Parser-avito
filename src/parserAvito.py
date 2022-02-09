import requests
from bs4 import BeautifulSoup


class Parser:
    mainUrl = 'https://www.avito.ru/novosibirsk/bytovaya_elektronika?cd=1'
    urls = []
    params = {'page': 1}
    pages = 2
    searchWord = ""

    def __init__(self):
        self.searchWord = input("Input search word: ")
        self.main()

    def main(self):
        while self.params['page'] <= int(self.pages):
            lxmlText = self.HtmlStrToLxml()

            self.TakeTitle(lxmlText)
            self.GetPagesCount(lxmlText) if self.params['page'] == 1 else None
            self.PrintAPageParsingMessage()

            self.params['page'] += 1

        self.PrintAllUrlsWithNecessaryWord()

    def GetPagesCount(self, lxmlText):
        paginationItemList = lxmlText.find_all('span', class_='pagination-item-JJq_j')
        self.pages = paginationItemList[-2].text

    def HtmlStrToLxml(self):
        response = requests.get(self.mainUrl, params=self.params)
        return BeautifulSoup(response.text, 'lxml')

    def TakeTitle(self, lxmlText):
        cards = lxmlText.find_all('div', class_='iva-item-content-rejJg')

        for i in range(len(cards)):
            title = cards[i].find('div', class_='iva-item-titleStep-pdebR').text
            self.FindWord(title)

    def FindWord(self, title):
        wordsList = title.split(' ')

        for n, i in enumerate(wordsList, start=1):
            self.AddToTheListUrls() if i == self.searchWord else None

    def AddToTheListUrls(self):
        isExists = False
        bufUrl = (self.mainUrl[:-1] + f'{self.params["page"]}')

        for i in range(len(self.urls)):
            if bufUrl == self.urls[i]:
                isExists = True
                break

        self.urls.append(bufUrl) if not isExists else None

    def PrintAllUrlsWithNecessaryWord(self):
        print('\n-------------------------\n')

        for n, i in enumerate(self.urls, start=1):
            print(f'{n}: {i}')

    def PrintAPageParsingMessage(self):
        print(f'Page parsing {self.params["page"]} of {self.pages}...')


parser = Parser()
