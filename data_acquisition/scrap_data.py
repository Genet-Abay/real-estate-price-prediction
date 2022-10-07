# import itertools
import json
import requests
from bs4 import BeautifulSoup
import logging as log
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor
from usp.tree import sitemap_tree_for_homepage
import pandas as pd

###################################################################
def get_property(url_property):
    all_property_dict = {}
    try:
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
    except Exception as arg:
            log.exception('problem occured in get_property function while scraping the page')

    
    required_properties = filter_out_dictionary(all_property_dict)
    return required_properties


###########################################################
def filter_out_dictionary(all_property_dict):
    '''
    This function constructs a dictionary which contains only required information
     from the original dictionary and returns the new filtered dictionary.
    '''
    required_properties = {}    
    if len(all_property_dict) > 0:        
        try:            
            properties = all_property_dict.get('property')
            property_type = properties.get('type')
            if property_type=="APARTMENT" or property_type=="HOUSE":
                required_properties['ID'] = all_property_dict.get('id')
                required_properties['Type'] = property_type

                if properties.get('subtype'):
                    required_properties['Sub type'] = properties.get('subtype')
                else:
                    required_properties['Sub type'] = ""
                
                if properties.get('bedroomCount'):
                    required_properties['BedroomCount'] = properties.get('bedroomCount')
                else:
                    required_properties['BedroomCount'] = ""
                # required_properties['BathroomCount'] = properties.get('id')
                if properties.get('location'):
                    if properties.get('location').get('province'):
                        required_properties['Province'] = properties.get('location').get('province')
                    else:
                        required_properties['Province'] = ""

                    if properties.get('location').get('region'):
                        required_properties['Region'] = properties.get('location').get('region')
                    else:
                        required_properties['Region'] = ""
                    
                    if properties.get('location').get('postalCode'):
                        required_properties['PostCode'] = properties.get('location').get('postalCode')
                    else:
                        required_properties['PostCode'] = ""
                    
                    if properties.get('location').get('street'):
                        required_properties['street'] = properties.get('location').get('street')
                    else:
                        required_properties['street'] = ""
                    
                    if properties.get('location').get('floor'):
                        required_properties['Floor'] = properties.get('location').get('floor')
                    else:
                        required_properties['Floor'] = ""
                    
                    if properties.get('location').get('regionCode'):
                        required_properties['RegionCode'] = properties.get('location').get('regionCode')
                    else:
                        required_properties['RegionCode'] = ""

                    if properties.get('location').get('type'):
                        required_properties['IsIsolated'] = properties.get('location').get('type')
                    else:
                        required_properties['IsIsolated'] = ""

                    if properties.get('location').get('hasSeaView'):
                        required_properties['HasSeaView'] = properties.get('location').get('hasSeaView')
                    else:
                        required_properties['HasSeaView'] = ""

                    if properties.get('location').get('pointsOfInterest'):
                        if properties.get('location').get('pointsOfInterest')[0].get('distance'):
                            required_properties['SchoolDistance'] = properties.get('location').get('pointsOfInterest')[0].get('distance')
                        else:
                            required_properties['SchoolDistance'] = ""

                        if len(properties.get('location').get('pointsOfInterest')) > 2:
                            required_properties['TransportDistance'] = properties.get('location').get('pointsOfInterest')[2].get('distance')
                        else:
                            required_properties['TransportDistance'] = ""
       
                
                if properties.get('netHabitableSurface'):
                    required_properties['NetHabitableSurface'] = properties.get('netHabitableSurface')
                else:
                    required_properties['NetHabitableSurface'] = ""

                if properties.get('roomCount'):
                    required_properties['TotalRoomCount'] = properties.get('roomCount')
                else:
                    required_properties['TotalRoomCount'] = ""

                if properties.get('hasAttic'):
                    required_properties['HasAttic'] = properties.get('hasAttic')
                else:
                    required_properties['HasAttic'] = ""          

                if properties.get('hasBasement'):
                    required_properties['HasBasement'] = properties.get('hasBasement')
                else:
                    required_properties['HasBasement'] = ""

                if properties.get('hasDiningRoom'):
                    required_properties['HasDiningRoom'] = properties.get('hasDiningRoom')
                else:
                    required_properties['HasDiningRoom'] = ""

                if properties.get('building'):
                    if properties.get('building').get('condition'):
                        required_properties['BuildingCondition'] = properties.get('building').get('condition')
                    else:
                        required_properties['BuildingCondition'] = ""

                    if properties.get('building').get('constructionYear'):
                        required_properties['ConstructionYear'] = properties.get('building').get('constructionYear')
                    else:
                        required_properties['ConstructionYear'] = ""

                    if properties.get('building').get('facadeCount'):
                        required_properties['FacadeCount'] = properties.get('building').get('facadeCount')
                    else:
                        required_properties['FacadeCount'] = ""

                if properties.get('hasLift'):
                    required_properties['HasLift'] = properties.get('hasLift')
                else:
                    required_properties['HasLift'] = ""

                if properties.get('constructionPermit'):
                    if properties.get('constructionPermit').get('floodZoneType'):
                        required_properties['FloodZoneType'] = properties.get('constructionPermit').get('floodZoneType')
                    else:
                        required_properties['FloodZoneType'] = ""

                if properties.get('energy'):
                    if properties.get('energy').get('heatingType'):   
                        required_properties['HeatingType'] = properties.get('energy').get('heatingType')   
                    else:
                        required_properties['HeatingType'] = ""

                    if properties.get('energy').get('hasDoubleGlazing'):   
                        required_properties['IsDoubleGlaze'] = properties.get('energy').get('hasDoubleGlazing')   
                    else:
                        required_properties['IsDoubleGlaze'] = ""


                if properties.get('kitchen'):
                    if properties.get('kitchen').get('type'):   
                        required_properties['KitchekType'] = properties.get('kitchen').get('type')   
                    else:
                        required_properties['KitchekType'] = ""

                    if properties.get('kitchen').get('surface'):   
                        required_properties['LivingRoomArea'] = properties.get('kitchen').get('surface')   
                    else:
                        required_properties['LivingRoomArea'] = ""
               
                if properties.get('hasBalcony'):
                    required_properties['HasBalcony'] = properties.get('hasBalcony')
                else:
                    required_properties['HasBalcony'] = ""

                if properties.get('hasGarden'):
                    required_properties['HasGarden'] = properties.get('hasGarden')
                else:
                    required_properties['HasGarden'] = ""

                if properties.get('gardenSurface'):
                    required_properties['GardenArea'] = properties.get('gardenSurface')
                else:
                    required_properties['GardenArea'] = ""
                # required_properties['NumberOfToilets'] = properties.get('specificities').get('toiletCount')
        except Exception as arg:
            log.exception(f'proplem occure in filter_out_dictionary function while reading property from {url_property}')
        else: 
            return(required_properties)

#########################################################
def iterate_urls_toget_properties(list_urls):
    count = 0
    batch_len = 8
    isFinished = False
    list_property_dict=[]
    try:
        while count < len(list_urls) and not isFinished:
            if count + batch_len < len(list_urls):
                batch_list_url = list_urls[count:count+batch_len]            
                count+=batch_len
            else:
                remaining_count = len(list_urls)-count
                batch_list_url = list_urls[count: count+remaining_count]
                count+=remaining_count
                isFinished=True
            
            with ThreadPoolExecutor() as pool:
                list_ = list(pool.map(get_property, batch_list_url))
            list_property_dict.extend(list_)

    except Exception as arg:
            log.exception('Problem occured iterating on urls to get property of links')
    else:
            return list_property_dict



######################################################
#immoweb home page "https://www.immoweb.be/en/search/house/for-sale?countries=BE"
def get_sitemap_info(home_page):
    tree = sitemap_tree_for_homepage(home_page)
    urls = [page.url for page in tree.all_pages()]
    print(len(urls), urls[0])
  

########################################################
def get_sitemap(link):
    '''
    The function get the recent sitemap from the given link
    and stores it to file
    
    '''
    r =requests.get(link)
    soup = BeautifulSoup(r.text)
    sites = soup.find_all('sitemap')
    file = open('C:\BeCode\LocalRepos\sitemapImo.txt', 'w')        
    for i in range(3):
        sitemap = sites[i].find('loc').text
        file.write(sitemap + '\n')
        print(sitemap)
    file.close()


###########################################################
def fetch_propertylinks_fromSiteMap():
    '''
    this function collects all the pages to search for House/Appartment 
    from sitemap files

    '''
    links = []
    with open('C:\BeCode\LocalRepos\documents\sitemapImo.txt', 'r') as f:
        sitemap = f.readline()
        # xml = requests.get(sitemap)
        xml = open('C:/BeCode/LocalRepos/documents/test_sitemap.xml', 'r')
        soup = BeautifulSoup(xml, features="lxml")
        
        urls = soup.find_all('url')
        for url in urls:
            loc = url.find('loc').text
            if 'https://www.immoweb.be/en' in loc:
                links.append(loc)
            
    return links

#######################################################
def export_dataframe(list_data, file_):
    '''
    This function accepts list of dictionaries and 
    export the dataframe to the given file

    '''
    df = pd.DataFrame.from_dict(list(filter(None, list_data)))
 
    # df.drop_duplicates()
    df.to_csv(file_, index=False)
    print('Properties saved to file')

#######################################################
def start_gathering_data():
    '''
    This function starts the process of scraping the page, gathering data
    and finally call the function to export the data into file
    '''

    print("Start getting links from sitemap")
    links = fetch_propertylinks_fromSiteMap()
    if len(links) > 0:
        print("links are successfully read and started to get properties")
        total_list_property = iterate_urls_toget_properties(links)
        if total_list_property and len(total_list_property) > 0: 

            print(f' a total of {len(total_list_property)} found and exporting them to a given file')
            export_dataframe(total_list_property, 'C:/BeCode/LocalRepos/documents/real_estate_data2.csv')
        else:
            print("list of properties are empty, nothing to export")



def main():
    start_gathering_data()

if __name__ == '__main__':
    main()
