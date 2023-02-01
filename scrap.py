import requests as rq
from bs4 import BeautifulSoup as bs



class Url:
    def __init__(self):
        self.energie = input("entrez l'energie (dies, ess, elec): ")
        self.marque = input("entrez une marque: ")
        self.km_max = self._verify_int("entrez km max: ")
        self.km_min = self._verify_int("entrez km min: ")
        self.prix_max = self._verify_int("entrez un prix max: ")
        self.prix_min = self._verify_int("entrez un prix min: ")
        self.année_max = self._verify_int("entrez anne max: ")
        self.année_min = self._verify_int("entrez anne mmin: ")

    def _verify_int(self, string_input):
        choice_user = input(string_input)
        try:
            choice_user = int(choice_user)
            return choice_user
        except:
            print("merci de rentrez un entier !\n")
            return self._verify_int(string_input)


    def url(self): 
        return "https://www.lacentrale.fr/listing?energies={}&makesModelsCommercialNames={}&mileageMax={}&mileageMin=1{}&page=1&priceMax={}&priceMin={}&yearMax={}&yearMin={}".format(self.energie, self.marque.upper(), self.km_max, self.km_min,self.prix_max, self.prix_min, self.année_max, self.année_min)
class ScrapData:
    def __init__(self, url):
        self.url = url 
    

    def _browse_page(self, n):
        url_split = self.url.split("&")
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
        self.url = "&".join(url_split)
        return str(self.url)


    def display_voiture(self):
        cpt = 1
        car_list = [1]
        while len(car_list) != 0:
            self.request_url = rq.get(self._browse_page(cpt))  
            self.response = self.request_url.content 
            self.html = bs(self.response, "lxml")
            h3 = self.html.find_all("h3", {"class": "Text_Text_text Vehiculecard_Vehiculecard_title Text_Text_subtitle2"})
            car_list = [i.string.strip() for i in h3]
            if len(car_list) > 0:
                for i in car_list:
                    print(i)
            else:
                break
            cpt += 1
        
    




    