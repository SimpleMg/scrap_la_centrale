import requests as rq
from bs4 import BeautifulSoup as bs
import csv
import re
import json

class ScrapData:
    def __init__(self):
        self.energie = ["dies", "ess", "elec"]
        self.marque = ["PEUGEOT"]
        self.km_max = 40000
        self.km_min = 1
        self.prix_min = 10000
        self.prix_max = 60000
        self.annee_min = 2000
        self.annee_max = 2023

    def _url(self, marque, page, modele):
        url = "https://www.lacentrale.fr/listing?makesModelsCommercialNames={}%3A{}&mileageMax={}&mileageMin=1{}&page={}&priceMax={}&priceMin={}&yearMax={}&yearMin={}".format(
            self.marque[0].upper(), modele, self.km_max, self.km_min, page, self.prix_max, self.prix_min, self.annee_max, self.annee_min)
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

    def _data_org(self, data:list[str])->list[str]:
        org_data = {"marque":0, "modele":0, "année":0, "km":0, "mode":0, "energie":0}
        energie_org_data = ["Diesel", "Essence", "Électrique"]
        mode = ["Automatique" , "Manuelle"]
        for i in range(len(data)):
            if data[i].split()[0] in self.marque:
                org_data["marque"] = data[i]
            elif (data[i] not in mode) and (data[i] not in energie_org_data) and ("km" not in data[i].split()):
                try:
                    data[i] = int(data[i])
                    org_data["année"] = data[i]
                except:
                    org_data["modele"] = data[i]
            elif "km" in data[i].split():
                org_data["km"] = "".join(data[i].split())
            elif data[i] in energie_org_data:
                org_data["energie"] = data[i].replace("É", "E")
            else:
                org_data["mode"] = data[i]
        list_org_data = [org_data["marque"],org_data["modele"],org_data["année"],org_data["km"],org_data["mode"],org_data["energie"]]
        return list_org_data

    def _recup_element_json(self, element_recup):
        url = "https://www.lacentrale.fr/listing"
        response = rq.get(url)
        soup = bs(response.text, "html.parser")
        for script in soup.find_all("script"):
            if "window.__PRELOADED_STATE_LISTING__" in script.text:
                html_data = script.text
        data = re.search('({.*});', html_data).group(1)
        data = json.loads(data)
        modele_liste = []
        for marque in data["search"]["aggs"]["vehicle.make"]:
            if marque["key"] == element_recup.upper():
                for modele in marque["agg"]:
                    modele_liste.append(modele["key"])
        return modele_liste

    def display_voiture(self):
        marque = 0
        cpt2 = 1
        while marque != len(self.marque):
            modele = self._recup_element_json("PEUGEOT")
            print("modele = ", modele)
            for i in range(len(modele)):
                car_list_h3 = [1]
                while len(car_list_h3) != 0:
                    url = self._url(marque, cpt2, modele[i])
                    print("url = ", url)
                    self.request_url = rq.get(self._browse_page(url, cpt2))
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
                        list_tuple_cara.append([car_list_div_cara[0], car_list_div_cara[1],
                                            car_list_div_cara[2], car_list_div_cara[3], car_list_div_cara[4]])
                        element += 4
                    iter_car = 0
                    while iter_car != len(car_list_h3):
                        data = [car_list_h3[iter_car], car_list_div_modele[iter_car], list_tuple_cara[iter_car][0], list_tuple_cara[iter_car][1], list_tuple_cara[iter_car][2], list_tuple_cara[iter_car][3]]
                        data = self._data_org(data)
                        print("marque = {}, modele = {} ,  {}, {}, {}, {}".format(
                            data[0], data[1], data[2], data[3], data[4], data[5]))
                        with open("file.csv", "a") as file_descriptor:
                            csv_writer = csv.writer(file_descriptor)
                            csv_writer.writerow(['{}'.format(data[0]), '{}'.format(data[1]), '{}'.format(data[2]), '{}'.format(data[3]) ,'{}'.format(data[4]), '{}'.format(data[5])])
                        iter_car += 1
                    cpt2 += 1
                cpt2 = 1
            marque += 1                
