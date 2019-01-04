
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
from pprint import pprint
import re

driver = webdriver.Chrome("./chromedriver")
driver.get("https://montgomery.tncrtinfo.com/crcaseList.aspx")
table=None
tr=None
dict={}
init_dict = {"record": []}
with open('criminal.json', 'w+') as f:
    json.dump(init_dict,f)
last_name=None
def go_back(name):
    driver.get("https://montgomery.tncrtinfo.com/crcaseList.aspx")
    last_name = driver.find_element_by_id("ctl00_ctl00_cphContent_cphSelectionCriteria_txtPartyLastName")
    last_name.send_keys(name)
    last_name.send_keys(Keys.RETURN)
    find_now=driver.find_element_by_id("ctl00_ctl00_cphContent_cphSelectionCriteria_cmdFindNow")
    find_now.click()
    table=driver.find_element_by_id("ctl00_ctl00_cphContent_cphSearchResults_gridSearch")
    tr=table.find_elements_by_tag_name("tr")

            

for first_number in range(65,90):
    char1 = ""
    char1=chr(first_number)+""
    for second_number in range(65,90):
        char2 = ""
        char2=chr(second_number)+""
        last_name=char1+char2
        last_name_element = driver.find_element_by_id("ctl00_ctl00_cphContent_cphSelectionCriteria_txtPartyLastName")
        last_name_element.send_keys(last_name)
        last_name_element.send_keys(Keys.RETURN)
        find_now=driver.find_element_by_id("ctl00_ctl00_cphContent_cphSelectionCriteria_cmdFindNow")
        find_now.click()
        time.sleep(2)
        while True:
            table=driver.find_element_by_id("ctl00_ctl00_cphContent_cphSearchResults_gridSearch")
            tr=table.find_elements_by_tag_name("tr")
            count=1
            length_of_tr=len(tr)
            for i in range(1,length_of_tr-1):
                table=driver.find_element_by_id("ctl00_ctl00_cphContent_cphSearchResults_gridSearch")
                tr=table.find_elements_by_tag_name("tr")
                td=tr[count].find_elements_by_tag_name("td")
                count+=1
                dict['Name']=td[1].find_element_by_tag_name('a').get_attribute('innerHTML')
                dict['Role']=td[2].get_attribute('innerHTML')
                dict['Case Number']=td[3].get_attribute('innerHTML')
                dict['Filing Date']=td[5].get_attribute('innerHTML')
                dict['Status']=td[6].get_attribute('innerHTML')
                dict['Status Date']=td[7].get_attribute('innerHTML')
                td[1].find_element_by_tag_name('a').click()
                time.sleep(2)
                ul_id=driver.find_element_by_id('ctl00_ctl00_cphContent_cphTabbedBar_ultab')
                li=ul_id.find_elements_by_tag_name('li')
                li[1].click()
                time.sleep(2)
                charge_table_id=driver.find_element_by_id("ctl00_ctl00_cphContent_cphFormDetail_gridcharges")
                charge_tr=charge_table_id.find_elements_by_tag_name('tr')
                

                charges_arr = []

                for charge_tr_element in charge_tr[1:]:

                    charges_dict={}

                    charge_td=charge_tr_element.find_elements_by_tag_name("td")

                    charges_dict['TCA Code']=re.sub('[;]', '', charge_td[2].get_attribute('innerHTML'))
                    charges_dict['TCA Desc']=re.sub('[;]', '', charge_td[3].get_attribute('innerHTML'))
                    charges_dict['Violation Date']=charge_td[5].get_attribute('innerHTML')
                    charges_dict['Disposition Date']="NA" if charge_td[6].get_attribute('innerHTML')=="&nbsp;" else charge_td[6].get_attribute('innerHTML')
                    charges_dict['Disposition Type']="NA" if charge_td[7].get_attribute('innerHTML')=="&nbsp;" else charge_td[7].get_attribute('innerHTML')

                    charges_arr.append(charges_dict)

                dict['Charges']=charges_arr

                # print(dict)
                data = {}
                with open('criminal.json', 'r') as infile:
                    data = json.load(infile)
                with open('criminal.json', 'w') as fs:
                    data["record"].append(dict)
                    json.dump(data, fs)

                driver.back()    
            try:
                Next=driver.find_element_by_id('ctl00_ctl00_cphContent_cphContentPaging_nextpage')
            except:
                break
            Next.click()
        
driver.close()