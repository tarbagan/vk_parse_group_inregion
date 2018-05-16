#!/usr/bin/python
# -*- coding: utf-8 -*-
from urllib.request import urlopen
from urllib.parse   import quote
import json
import time
import csv

q = quote("Поисковый запрос") #Например Новости. Можно поставить пробел " ", тогда найдет все группы у которых не менее двух слов
token = "TOKEN"

def get_multicity(): #Получаем населенные пункты вашего региона. Вместо 1157049& укажите свой индификатор региона ВК
    url = "https://api.vk.com/method/database.getCities.json?region_id=1157049&country_id=1&count=200&access_token=" + token + "&v=5.52"
    response = urlopen(url)
    data = response.read()
    city = json.loads(data)
    return city

def multi_search():
    gr = []
    for st in get_multicity()["response"]["items"]:
        stid = str((st["id"]))
        namecity = str((st["title"]))
        url2 = "https://api.vk.com/method/groups.search.json?q="+q+"&city_id="+stid+"&count=1000&sort=0&access_token="+ token +"&v=5.52"
        response2 = urlopen(url2)
        data2 = response2.read()
        group = json.loads(data2)
        time.sleep(0.5)
        if group ["response"]["count"] !=0:
            for pars in group["response"]["items"]:
                pars['city'] = namecity
                grid = str(pars['id'])
                print( "Получаем: %s" % namecity )
                url3 = "https://api.vk.com/method/groups.getMembers.json?group_id="+grid+"&access_token=" + token + "&v=5.52"
                response3 = urlopen(url3)
                data3 = response3.read()
                folower = json.loads(data3)
                fl = (folower["response"]["count"])
                pars['follower'] = fl
                pars['url'] = (str("https://vk.com/club"+grid))
                gr.append(pars)
                time.sleep(0.5)
    return gr

def save_cvs(): #Сохраняем результат в файл CVS
    datagroup = multi_search()
    with open( "d:/AnacodaProgect/group.csv", "w", encoding='utf-8' ) as file: #Укажите путь к ашему файлу cvs
        fieldnames = ['id', 'name', 'is_closed', 'type', 'photo_200', 'city', 'follower', 'url']
        writer = csv.DictWriter( file, fieldnames=fieldnames )
        writer.writeheader()
        for sgroup in datagroup:
            idg = (sgroup["id"])
            nmg = (sgroup["name"])
            icg = (sgroup["is_closed"])
            tyg = (sgroup["type"])
            phg = (sgroup["photo_200"])
            cig = (sgroup["city"])
            flg = (sgroup["follower"])
            urg = (sgroup["url"])
            writer.writerow({'id': idg, 'name': nmg, 'is_closed': icg, 'type': tyg, 'photo_200': phg, 'city': cig, 'follower': flg, 'url': urg} )

save_cvs()
print ("ok")
