import scrapy
from scrapy import Request as Request
from scrapy_splash import SplashRequest

class AlimentaricoopSpider(scrapy.Spider):
    name = 'alimentariCoop'

    def start_requests(self):

        alimenti_preparati = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-confezionati/Alimenti-preparati-e-altro/c/110102?q=%3Arelevance&page=0&pagesize=36']
        baby_food = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-confezionati/Baby-Food/c/110103?q=%3Arelevance&page={}&pagesize=36'.format(i) for i in range(2)]
        carne_pesce = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-freschi/Carne-e-pesce/c/110201?q=%3Arelevance&page={}&pagesize=36'.format(i) for i in range(3)]
        formaggi = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-freschi/Formaggi/c/110202?q=%3Arelevance&page={}&pagesize=36'.format(i) for i in range(3)]
        gastronomia = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-freschi/Gastronomia/c/110203?q=%3Arelevance&page={}&pagesize=36'.format(i) for i in range(2)]        
        latticini = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-freschi/Latticini-e-uova/c/110204?q=%3Arelevance&page={}&pagesize=36'.format(i) for i in range(4)]
        salumi = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-freschi/Salumi/c/110205?q=%3Arelevance&page={}&pagesize=36'.format(i) for i in range(3)]
        surgelati = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-freschi/Surgelati/c/110207?q=%3Arelevance&page={}&pagesize=36'.format(i) for i in range(6)]
        verdura = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-freschi/Verdura/c/110208?q=%3Arelevance&page={}&pagesize=36'.format(i) for i in range(3)]
        aromi = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-freschi/Aromi/c/110209?q=%3Arelevance&page=0&pagesize=36']
        bevande = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-confezionati/Acqua-e-bevande/c/110101?q=%3Arelevance&page={}&pagesize=36'.format(i) for i in range(5)]
        dolci = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-confezionati/Dolci-e-pasticceria/c/110104?q=%3Arelevance&page={}&pagesize=36'.format(i) for i in range(5)]
        snack_salati = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-confezionati/Pane-e-snack-salati/c/110105?q=%3Arelevance&page={}&pagesize=36'.format(i) for i in range(2)]
        pasta = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-confezionati/Pasta%2C-riso-e-farina/c/110106?q=%3Arelevance&page={}&pagesize=36'.format(i) for i in range(4)]
        merenda = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-confezionati/Prima-colazione-e-merenda/c/110108?q=%3Arelevance&page={}&pagesize=36'.format(i) for i in range(4)]
        condimenti_scatolame = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-confezionati/Salse%2C-condimenti-e-scatolame/c/110109?q=%3Arelevance&page={}&pagesize=36'.format(i) for i in range(7)]
        infusi = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-confezionati/Zucchero%2C-caff%C3%A8-e-infusi/c/110110?q=%3Arelevance&page={}&pagesize=36'.format(i) for i in range(2)]
        cibo_animali = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Alimentari-confezionati/Pet-food---pet-care/c/110107?q=%3Arelevance&page={}&pagesize=36'.format(i) for i in range(3)]
        celiaci = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Salutistici/Alimenti-per-celiaci/c/110301?q=%3Arelevance&page=0&pagesize=36']
        integratori = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Salutistici/Integratori/c/110303?q=%3Arelevance&page=0&pagesize=36']
        yogurt = ['http://www.catalogoprodotti.coop.it/pam/it/Categorie-PAM/Salutistici/Yogurt/c/110302?q=%3Arelevance&page=0&pagesize=36']

        urls = alimenti_preparati + baby_food + carne_pesce + formaggi + gastronomia + latticini + salumi + surgelati + verdura + aromi + bevande + dolci + snack_salati + pasta + merenda + condimenti_scatolame + infusi + cibo_animali + celiaci + integratori + yogurt 

        for url in urls:
            yield SplashRequest(url=url, callback=self.parse_page_products)


    def parse_page_products(self, response):
        urls = ["{}{}".format('http://www.catalogoprodotti.coop.it',i) for i in response.css('div.productGridItem .thumb a::attr(href)').getall()]

        for url in urls:
            yield SplashRequest(url=url, callback=self.get_info,args={'wait':2})


    def get_info(self, response):

        ean = response.css('.ean div.descrizione::text').get()

        nome = ', '.join(response.css('.manufacturer span ::text').getall()).replace('\"','')
        nome = self.remove_double_quotes(nome)

        marchio = response.css('.manufacturer h1 ::text').get()
        marchio = self.remove_tabs(marchio)
        marchio = self.remove_new_lines(marchio)

        origine = ', '.join(response.css('.origini p.descrizione::text').getall())
        origine = self.remove_tabs(origine)
        origine = self.remove_new_lines(origine)
        origine = self.remove_double_quotes(origine)

        descrizione = ''.join(response.css('div.description div.descrizione ::text').getall()) + ', '.join(response.css('div.description div.descrizione2 ::text').getall())
        descrizione = self.remove_tabs(descrizione)
        descrizione = self.remove_new_lines(descrizione)
        descrizione = self.remove_double_quotes(descrizione)
        
        ingredienti = ''.join(response.css('#div_descrizione_id::text').getall())
        ingredienti = self.remove_double_quotes(ingredienti)

        immagine = response.css('#primary_image_id::attr(src)')
        try:
            immagine = "http://www.catalogoprodotti.coop.it"+immagine.get()
        except:
            immagine = []

        conservazione = ', '.join(response.css('.conservazione div div::text').getall())

        preparazione = ', '.join(response.css('.preparazione div div::text').getall())
        preparazione = self.remove_double_quotes(preparazione)

        nutrienti = [i +': '+ j for i, j in zip(response.css('.valori_nutrizionali td.c1::text').getall(),response.css('.valori_nutrizionali td.c2::text').getall())]

        allergeni = response.css('#allergeni_table td::text').getall()
        allergeni = [self.remove_tabs(x) for x in allergeni]
        allergeni = [self.remove_new_lines(x) for x in allergeni]


        yield {
            'ean': ean,
            'nome': nome,
            'marchio': marchio,
            'origine': origine,
            'descrizione': descrizione,
            'ingredienti': ingredienti,
            'immagine': immagine,
            'conservazione': conservazione,
            'preparazione': preparazione,
            'nutrienti': nutrienti,
            'allergeni': allergeni,
        }

        print(response.css('.manufacturer span ::text').get())

    def get_page_product(self, response):
        url = response.url.split("/")[-3]
        index = response.url.find('page')
        field = url + '_Page_' + response.url[index+5]

        yield {
            field: ["{}{}".format('http://www.catalogoprodotti.coop.it',i) for i in response.css('div.productGridItem .thumb a::attr(href)').getall()]
        }
        print('Parsata:{}'.format(response.url))

    def remove_tabs(self, string):
        return string.replace('\t','')

    def remove_new_lines(self, string):
        return string.replace('\n','')

    def remove_double_quotes(self, string):
        return string.replace('\"',"")