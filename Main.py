#_____ИМПОРТЫ_____
import requests #Запросы на сервер
import datetime
from time import sleep

#Тупа инфа
token = "dc54d704dc54d704dc54d7049adc256519ddc54dc54d704839a84cacf70b105fbdf9838"
myid = "433849874"



#_____МЕТОДЫ_____
#Основной метод
def get_data(method, parameters, token = token):
    url = 'https://api.vk.com/method/'+ method +'?'+ parameters +'&v=5.52'+'&access_token=' + str(token)
    response = requests.get(url)
    return(response.json())


#Проверка id
def check_id(id_person):
    id_person = str(id_person).split("/")
    if len(id_person) > 2:
        id_person = id_person[3]
    else:
        id_person = id_person[0]
    #Превращаем id во внутренний id
    id_person = ((get_data(method = "users.get", parameters = "user_ids=" + str(id_person), token = token))["response"])[0]
    id_person = id_person["id"]
    
    return id_person


#Имя Фамилия id
def get_NamePerson(id_person):
    id_person = check_id(id_person)
    # Имя и фамилия
    name = ((get_data(method = "users.get", parameters = "user_ids=" + str(id_person), token = token))["response"])[0]
    firstname = name["first_name"] #Имя
    lastname = name["last_name"] #Фамимлия
    idp = name["id"]
    #Возврат значения
    return [firstname, lastname, idp]


#Онлайн пользователя
def get_OnlinePerson(id_person):
    id_person = check_id(id_person)
    #Получение статуса
    online = ((get_data(method = "users.get", parameters = "user_id=" + str(id_person) + "&fields=online", token = token))["response"])[0]
    online = online["online"]
    #Возврат значения
    return online



#Создание и редактирование личного файла на каждого человека
def file_edit(id_person, key):
    #Начальные параметры для работы
    key = str(key)
    id_person = check_id(id_person)
    first_name = (get_NamePerson(id_person))[0]
    last_name = (get_NamePerson(id_person))[1]

    #По ключу выбор че делать
    if key == "1": #Cтереть файлик  
        file_person = open((str(first_name) + "_" + str(last_name) + "_" + str(id_person) + ".txt"), "w")

    elif key == "2": #Дозапись Когда была в сети
        file_person = open((str(first_name) + "_" + str(last_name) + "_" + str(id_person) + ".txt"), "a")
        date = datetime.datetime.now()
        online = str(get_OnlinePerson(id_person))
        if online == "1":
            file_person.write(str(date) + "  " + "ONLINE")
            file_person.write("\n")
        if online == "0":
            file_person.write(str(date) + "  " + "OFFLINE")
            file_person.write("\n")
        

def main():
    ids = (input()).split(" ")
    num = 0 
    while num == 0:
        for i in ids:
            file_edit(i, 2)
            sleep(5)


main()