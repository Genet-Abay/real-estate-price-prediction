from gettext import find
import json
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import re
from csv import DictWriter


# class Home():
#     def __init__(self):        
#         locality = "" 
#         type_of_property = "House"
#         subtype_of_property = "" 
#         price = 0
#         type_of_sale = ""
#         number_of_rooms = 0
#         living_area = 0 #in meter squared
#         is_fully_equipped_kitchen =  False
#         is_furnished =  False
#         is_open_fire = False
#         has_terrace = False
#         terrace_area = 0 # only if there is terrace
#         has_garden = False
#         garden_are = 0 #if garden is available 
#         surface_of_the_land = 0 
#         #surface area of the plot of land 
#         number_of_facades = 1 
#         swimming_pool = False 
#         state_of_the_building = ''# (New, to be renovated, ...)

#     def pass_property(self):
#         pass

#     def set_property(self):
#         pass


def get_property(url_property):
    req = requests.get(url_property)
    content = req.text
    soup = BeautifulSoup(content, 'html.parser')
    
    scripts = soup.findAll('script', type='text/javascript') 
    properties = ""
    for script in scripts:
        text = script.text
        if 'window.classified' in text:
            text = text[text.find('{'): text.rfind(';')]
            all_property_dict = json.loads(text)
            break

    required_properties = {}    
    if len(all_property_dict) > 0:
        required_properties['ID'] = all_property_dict.get('id')
        try:
            properties = all_property_dict.get('property')

            required_properties['Type'] = properties.get('type')
            required_properties['Sub type'] = properties.get('subtype')
            required_properties['BedroomCount'] = properties.get('bedroomCount')
            required_properties['BathroomCount'] = properties.get('id')
            required_properties['Province'] = properties.get('location').get('province')
            required_properties['Region'] = properties.get('location').get('region')
            required_properties['PostCode'] = properties.get('location').get('postalCode')
            required_properties['street'] = properties.get('location').get('street')
            required_properties['Floor'] = properties.get('location').get('floor')
            required_properties['RegionCode'] = properties.get('location').get('regionCode')
            required_properties['IsIsolated'] = properties.get('location').get('type')
            required_properties['HasSeaView'] = properties.get('location').get('hasSeaView')
            required_properties['SchoolDistance'] = properties.get('location').get('pointsOfInterest')[0].get('distance')
            required_properties['TransportDistance'] = properties.get('location').get('pointsOfInterest')[2].get('distance')

            required_properties['NetHabitableSurface'] = properties.get('netHabitableSurface')
            required_properties['TotalRoomCount'] = properties.get('roomCount')
            required_properties['HasAttic'] = properties.get('hasAttic')            
            required_properties['HasBasement'] = properties.get('hasBasement')
            required_properties['HasDiningRoom'] = properties.get('hasDiningRoom')

            required_properties['BuildingCondition'] = properties.get('building').get('condition')
            required_properties['ConstructionYear'] = properties.get('building').get('constructionYear')
            required_properties['FacadeCount'] = properties.get('building').get('facadeCount')

            required_properties['HasLift'] = properties.get('hasLift')

            required_properties['FloodZoneType'] = properties.get('constructionPermit').get('floodZoneType')

            required_properties['HeatingType'] = properties.get('energy').get('heatingType')    
            required_properties['IsDoubleGlaze'] = properties.get('energy').get('hasDoubleGlazing') 

            required_properties['KitchekType'] = properties.get('kitchen').get('type')

            required_properties['LivingRoomArea'] = properties.get('kitchen').get('surface')
            required_properties['HasBalcony'] = properties.get('hasBalcony')
            required_properties['HasGarden'] = properties.get('hasGarden')
            required_properties['GardenArea'] = properties.get('gardenSurface')
            required_properties['NumberOfToilets'] = properties.get('specificities').get('toiletCount')
        except:
            print('proplem occure while reading property from the original ')

    return(required_properties)


def iterate_urls_toget_properties(list_urls):
    count = 0
    batch_len = 10
    isFinished = False
    while count < len(list_urls and not isFinished):
        if count + 10 < len(list_urls):
            batch_list_url = list_urls[count:count+10]            
            count+=10
        else:
            remaining_count = len(list_urls)-count
            batch_list_url = list_urls[count: count+remaining_count]
            count+=remaining_count
            isFinished=True

        list_property_dict=[]
        with ThreadPoolExecutor() as pool:
            list_property_dict = list(pool.map(get_property, batch_list_url))
        if len(list_property_dict): 
            with ThreadPoolExecutor() as pool:
                status = pool.map(save_data, list_property_dict) 
        else:
            print("nothing to save for this batch of links")


def save_data (list_properties_dict, dict_writer):
    for property_dict in list_properties_dict:
        values = property_dict.values()
        dict_writer.writerow(values)


def save_links():
    '''
    this function collects all the pages to search for House/Appartment 
    and save all the page link to the file which will be used later 
    '''
    for page_number in range(300):
        page_url = f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={page_number+1}&orderBy=relevance"
        r = requests.get(page_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        links_list = soup.find_all('li', class_='search-result')
        print(links_list)
        break


   

def start_gathering_data():
    done = save_links()
    if done:
        links = []
        with open("property_links.txt") as file:
            lines = file.readlines()
            links = [line.rstrip() for line in lines]

        if len(links) > 0:
            f = open("house_price_predict.csv", "w")
            header = ['locality', 'type_of_property' ,'subtype_of_property' ,'price' ,'type_of_sale' ,'number_of_rooms','living_area','is_fully_equipped_kitchen' ,is_furnished,is_open_fire,
            'has_terrace','terrace_area','has_garden','garden_area', 'surface_of_the_land','number_of_facades', 'swimming_pool', 'state_of_the_building']
            dict_writer = DictWriter(f, header, delimiter=",")
            iterate_urls_toget_properties(links, dict_writer)





# Test for save links to file function
save_links()


# Test for get_property function
# test_url = 'https://www.immoweb.be/en/classified/house/for-sale/ans/4430/10147032?searchId=633bf0a6dcebd'
# # session_param = requests.Session()
# home_property = get_property(test_url)
# print(home_property)
