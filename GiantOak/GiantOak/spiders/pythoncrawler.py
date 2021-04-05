#Steps for python crawler/scraping program
#1. Created a new Scrapy project called GiantOak
#2. Choose and Extract URL from csv file
#3. Write a Spider class to crawl the website and extract data
#4. Use appropriate html requests/ CSS Selectors that returns your extracted data
#5. Write a Spider recursive callback to extract further links within the website
#6. Extract the data and format entire dataset within dictonary
#7. yield the entire dataset to export to json file format

import csv
import scrapy

#Access the appropriate Source URL from the csv file.
with open("/Users/BrianAguilar/Documents/GiantOak/bad_people_lists.csv","r") as csvfile:
    data = csvfile.read().splitlines()
    third_row = data[3].split()
    source_URL = (third_row[-1])
    source_code = third_row[0]
    source_name = third_row[1:5]
    string = ' '.join(source_name)

#ChildSpiderClass is a subclass from the parent class Spider. The subclass has methods and behaviors 
#which are used to follow URL's amd extract data from website pages. 
#URL must be within a list format. 
class ChildSpiderClass(scrapy.Spider):
    name = "crawler"
    start_urls =   [source_URL]

    #Parse method used to return all scrape data and follows/tracks to the links.
    def parse(self, response):
        count = 0
        list_descriptions = []
        list_name = []
        scraped_info = {}
        Main_dict = {}
        dummy = {}
        i = 0
        j = 0
        k = 0
        l = 0
        m = 0
        #Starting main URL page requests for scraping information 
        names = response.css("span.field-content::text").getall()
        ages = response.css("span.date-display-interval::text").getall()
        crimes = response.css("div.field-content::text").getall()
        detail_links =  response.css("span.field-content a::attr(href)").getall()

        #Individual page links for each person, requests for scraping more information 
        more_info = response.css("li.taxonomy-term-reference-0::text").getall()
        state_case = response.css("div.even::text").getall()
        date_of_birth = response.css("span.date-display-single::text").get()
        name = response.css(".title::text")[0].getall()
        # height = response.css("div.field-label").get()

        #Extract data from main website and format into dictionary named scraped_info
        length = len(names)
        length_des = len(crimes)
        length_name = len(name)
        while(i<length):
            while(j<length):
                while(k<length_des and count<2):
                    list_descriptions.append(crimes[k])
                    k+=1
                    count+=1
                    if count == 2:
                        scraped_info[names[i]] = {"age": ages[j], "state": list_descriptions[0], "crimes": list_descriptions[1]}
                        #print(dict(fullname=names[i], age=ages[j], crimes=list_descriptions))
                        count = 0
                        list_descriptions.clear()
                        i+=1
                        j+=1
                        break
        
        #other info dictionary used to extract and store data from individual links from each person
        Other_info = {"name": name, "date_of_birth": date_of_birth, "state":state_case}
        #"Gender": more_info[0], "Height": more_info[1], "Eye-Colour": more_info[2], "Nationality": more_info[3], "Spoken_lanuguages": more_info[4]}
       

        Main_List = [scraped_info]
        Other_List = [Other_info]
        Main_dict ={"source_code" : source_code, "source_name": string, "source_URL": source_URL, "Persons" : Main_List, "Other" : Other_List}

        #Follow through with each link and crawl/scrape each dataset 
        for link in detail_links:
            if link is not None:
                yield response.follow(link, callback=self.parse)
        
        yield Main_dict
    pass