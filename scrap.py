import requests as rq
from bs4 import BeautifulSoup as bs


class ScrapData:
    def __init__(self):
        self.energie = ["dies", "ess", "elec"]
        self.marque = ["PEUGEOT", "RENAULT", "AUDI",
                       "VOLKSWAGEN", "BMW", "MERCEDES", "CITROEN", "PORSCHE"]
        self.km_max = 40000
        self.km_min = 1
        self.prix_min = 10000
        self.prix_max = 60000
        self.annee_min = 2000
        self.annee_max = 2023

    def _url(self, marque, energie, page):
        url = "https://www.lacentrale.fr/listing?energies={}&makesModelsCommercialNames={}&mileageMax={}&mileageMin=1{}&page={}&priceMax={}&priceMin={}&yearMax={}&yearMin={}".format(
            self.energie[energie], self.marque[marque].upper(), self.km_max, self.km_min, page, self.prix_max, self.prix_min, self.annee_max, self.annee_min)
        return url

    def _browse_page(self, url, n):
        url_split = url.split("&")
        change = []
        for i in range(len(url_split)):
            if n == 1:
                if url_split[i] == "page={}".format(n):
                    change = url_split[i].split("=")
                    change[-1] = str(n)
                    url_split[i] = "=".join(change)
            else:
                if url_split[i] == "page={}".format(n - 1):
                    change = url_split[i].split("=")
                    change[-1] = str(n)
                    url_split[i] = "=".join(change)
        url = "&".join(url_split)
        return str(url)

    def display_voiture(self):
        cpt = 1
        marque = 0
        energie = 0
        while marque != len(self.marque):
            url = self._url(marque, energie, cpt)
            print("url = ", url)
            self.request_url = rq.get(self._browse_page(url, cpt))
            self.response = self.request_url.content
            self.html = bs(self.response, "lxml")
            h3 = self.html.find_all("h3", {
                                    "class": "Text_Text_text Vehiculecard_Vehiculecard_title Text_Text_subtitle2"})
            div_modele = self.html.find_all(
                "div", {"class": "Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2"})
            div_cara = self.html.find_all("div", {
                                          "class": "Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2"})
            car_list_h3 = [i.string.strip() for i in h3]
            car_list_div_modele = [i.string.strip() for i in div_modele]
            car_list_div_cara = [i.string.strip() for i in div_cara]
            list_tuple_cara = []
            element = 0
            while element != len(car_list_div_cara):
                list_tuple_cara.append([car_list_div_cara[cpt], car_list_div_cara[cpt+1],
                                       car_list_div_cara[cpt+2], car_list_div_cara[cpt+3]])
                element += 4
            iter_car = 0
            while iter_car != len(car_list_h3):
                print("marque = {}, modele = {},  {}, {}, {}, {}".format(
                    car_list_h3[iter_car], car_list_div_modele[iter_car], list_tuple_cara[iter_car][0], list_tuple_cara[iter_car][1], list_tuple_cara[iter_car][2], list_tuple_cara[iter_car][3]))
                iter_car += 1
            cpt += 1
            if energie == 2:
                marque += 1
                cpt = 0
                energie = 0
            else:
                if len(car_list_h3) == 0 or cpt == 10:
                    energie += 1
                    cpt = 0
