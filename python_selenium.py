# -*- coding: utf-8 -*-
#######################################
# Written by Michael Mefenza
#
#Python script automaticaly interact with website through selenium driver, retrieve user information, login, logout, send messages to user.
#
#######################################
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import codecs
import random
import time
import sys


def rows(fd):
    n = 1
    rest = ""
    while 1:
        chunk = fd.read(1024).encode("utf-8")
        if not chunk:
            break

        while 1:
            chunk = rest + chunk
            pos = chunk.find("\n")
            if pos > -1:
                pos += 1
                line, rest = chunk[:pos], chunk[pos:]
                yield n, line.replace("\r", "").replace("\n", "").split("\t")
                chunk = ""
                n += 1
            else:
                break

#cities
cities = list()
fd = codecs.open("dataen.txt", "r", "utf-8")
for n, row in rows(fd):
    columns = [row[8], row[9], row[1]]  #Country,Region,City
    if all(columns):
        if row[8] == "Germany":
            #cities.add(",".join(columns))
            cities.append(row[1])
            

driver = webdriver.Firefox()
driver1 = webdriver.Firefox()
#driver = webdriver.Chrome('chromedriver')

#logout
driver.get("http://xxx/logout")
driver.implicitly_wait(1)
time.sleep(1)
driver1.get("http://xxx/logout")
driver1.implicitly_wait(1)
time.sleep(1)

#login
driver.get("http://xxx/login")
elem = driver.find_element_by_name("username")
elem.send_keys("username")
elem = driver.find_element_by_name("password")
elem.send_keys("password")
login_button = driver.find_element_by_xpath('//div[contains(@class,"formaction")]//button[contains(@class,"btnvalidation")]')
login_button.click()
driver.implicitly_wait(1)
time.sleep(1)
driver1.get("http://www.xxx/login")
elem = driver1.find_element_by_name("username")
elem.send_keys("username")
elem = driver1.find_element_by_name("password")
elem.send_keys("password")
login_button = driver1.find_element_by_xpath('//div[contains(@class,"formaction")]//button[contains(@class,"btnvalidation")]')
login_button.click()
driver1.implicitly_wait(1)
time.sleep(1)

trajets_checked = list()
user_written_to = list()
found_more =0    
count_try =0
while found_more ==0 :
    found_trajet =0  
    while found_trajet ==0 :
        random_city1 = repr(random.choice(cities)) 
        random_city2 = random_city1
        while random_city2 == random_city1:
            random_city2 = repr(random.choice(cities)) 
        trajets = [random_city1, random_city2]
        if trajets not in trajets_checked:
            trajets_checked.append(trajets)
            found_trajet =1 
            count_try =0
            print trajets
        else:
            count_try = count_try + 1
            print "trajet already checked .........................................."
            if count_try == 10000:
                found_more =1
                found_trajet =1 
            
    if found_more == 0:
        #select date: N days from today
        N = 2
        date_in_N_days = datetime.now() + timedelta(days=N)
        date = date_in_N_days.strftime("%d.%m.%Y")
        print date

        #push datas to website
        driver.get("http://xxx")
        elem = driver.find_element_by_name("fnt")
        elem.send_keys(random_city1)
        elem = driver.find_element_by_name("tnt")
        elem.send_keys(random_city2)
        elem = driver.find_element_by_name("dbt")
        elem.send_keys(date)
        find_button = driver.find_element_by_xpath('//div[contains(@class,"hpherosearch")]//button[contains(@class,"btn2action")]')
        find_button.click()
        driver.implicitly_wait(1)
        time.sleep(1)
        #process results of search
        found_results = 0
        try:
            search_results = driver.find_element_by_xpath('//ul[contains(@class,"searchresults")]')
            found_results = 1
        except:
            print "no results"
        if found_results == 1:
            pagination = 1
            while pagination == 1:
                links_results =  driver.find_elements_by_xpath('//a[@class="searchoneresult"]')
                for result in links_results:
                    result_link=result.get_attribute("href")
                    driver1.get(result_link)
                    time.sleep(1)
                    username = driver1.find_element_by_xpath('//div[@class="maincolumnblock"]//h4').text
                    userage = driver1.find_element_by_xpath('//div[@class="maincolumnblock"]//li[2]').text
                    try:
                        userrating = driver1.find_element_by_xpath('//p[contains(@class,"container")]//span[@class="bold"]').text
                    except:
                        userrating = 0
                    if userrating < 4.5 :
                        user = [username, userrage, userrating] 
                        if user not in user_written_to:
                            print user
                            #write to user
                            try:
                                write_link = driver1.find_element_by_xpath('//div[contains(@class,"actioncontainer")]//a[contains(@class,"btn2action")]')
                                write_link.click()
                                elem = driver1.find_element_by_name("message[content]")
                                message= "Dear " + username + ", \n We would like to wish you good luck. \n Regards \n Team"
                                elem.send_keys(message)
                                send_button = driver1.find_element_by_xpath('//div[contains(@class,"pullleft")]//button[contains(@class,"btnvalidation")]')
                                send_button.click()
                                user_written_to.append(user)
                            except:
                                 pass
                        else:
                             print " already written to " 
                             print Bdriver

                try:
                    next_results = driver.find_element_by_xpath('//li[contains(@class,"next") and not(contains(@class,"disabled"))]//a')
                    driver.get(next_results.get_attribute("href"))
                    driver.implicitly_wait(1)
                    time.sleep(1)
                except:
                    pagination = 0
driver1.close()
driver.close()   
