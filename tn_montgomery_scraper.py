import logging
from time import sleep
from selenium import webdriver
from itertools import product
import csv
from random import random
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from lxml import html
from lxml import etree
import re

from fake_useragent import UserAgent

# setup logger configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)-25s %(levelname)-7s %(filename)-30s %(funcName)-45s %(lineno)-4s %(message)-8s')
logger = logging.getLogger(__name__)

options = Options()
user_agent = UserAgent()

"""
use this sleep so you see visually see the changes in the browser as it's automated; you can set it to 0 to run
the script as fast as possible
"""
sleep_seconds = 0


def main():
    logger.info("setup Selenium driver given its location on my computer...")
    browser = implement_new_user_agent()

    logger.info("instantiate object to use methods from ActionChains which involve mouse clicks")
    actions = ActionChains(browser)

    navigate_to_court_records_search_engine(browser, actions)

    # BREAKS HERE; immediately blocked on TOU page

    sleep(sleep_seconds + (2 * random()))
    two_letter_combos = create_list_of_search_engine_queries()

    with open('sc_case_details.csv', mode='w') as sc_case_details:
        writer_object = csv.writer(sc_case_details)

        logger.info("loop through all items in two_letter_combos...")
        for two_letter_combo in two_letter_combos[0:1]:
            make_search_query(browser, two_letter_combo)
            parse_page(browser)
            next_page(browser)

            logger.info("sleep a bit...")
            sleep(random()*4)

            logger.info("quit browser...")
            browser.quit()


def navigate_to_court_records_search_engine(browser, actions):
    """
    Uses Selenium to open browser, navigate to SC County site, accept disclaimer
    :param browser: Selenium driver
    :return: None
    """
    logger.info("open empty browser")
    browser.maximize_window()
    logger.info("sleep...")
    sleep(sleep_seconds + (2 * random()))

    montgomery_county_search = 'https://montgomery.tncrtinfo.com/crCaseList.aspx'

    logger.info("navigate to the page: {0}".format(montgomery_county_search))
    browser.get(montgomery_county_search)

    sleep(sleep_seconds + (2 * random()))
    return None


def create_list_of_search_engine_queries():
    """
    Generate Python list of all three letter combos for the letters in the alphabet
    :return: three_letter_combos
    """
    logger.info("generate the cartesian product of all 2 letter combos in the alphabet...")
    logger.info("therefore, we can search aa then ab then ac and so forth...")

    logger.info("use the itertools product method to generate a list of tuples - each tuple containing 2 letters")
    letters_tuple_combos = list(product('ABCDEFGHIJKLMNOPQRSTUVWXYZ', repeat=2))
    logger.info("first 2 tuple combos: {0}".format(letters_tuple_combos[0:3]))

    logger.info("join those three strings in each combo in a single string and add them to a list")
    two_letter_combos = ["".join(tuple_val) for tuple_val in letters_tuple_combos]
    logger.info("first 2 letter combos in three_letter_combos: {0}".format(two_letter_combos[0:3]))

    return two_letter_combos


def parse_page(browser):
    page = browser.find_element_by_tag_name('html').get_attribute('innerHTML').replace('\n', '');
    list1 = []
    tree = etree.HTML(page)
    table = tree.xpath("//table[@class='searchList']")
    print(table)
    for rows in table:
        for row in rows:
            list2 =[]
            for col in row:
                elem = col.xpath("./a")
                lenVal = len(elem)
                if lenVal==1:
                    list2.append(elem[0].text)
                else:
                    list2.append(col.text)
            list1.append(list2)

    # print(list1)

    # for subList in list1:
    #     if len(subList)!=0:
    #         # print re.sub('^,', '', c)
    #         print(', '.join(subList).strip())
    #         # for subElm in subList:
    #             # print(subElm)



def next_page(browser):
    try:
        logger.info("go to the next page...")
        next_page = browser.find_element_by_name('ctl00$ctl00$cphContent$cphContentPaging$nextpage')
        next_page.click()
    except:
        logger.info("no next page")
    return None


def make_search_query(browser, two_letter_combo_start):
    """

    :param browser: chrome driver
    :param two_letter_combo_start: 2 letter combination for search query
    :return: None
    """

    logger.info("find last name text box input...")
    last_name_text_box = browser.find_element_by_name('ctl00$ctl00$cphContent$cphSelectionCriteria$txtPartyLastName')
    logger.info("type in the value {0} into the last name text box input".format(two_letter_combo_start))
    last_name_text_box.send_keys(two_letter_combo_start)
    sleep(sleep_seconds + (2 * random()))

    logger.info("find the search button...")
    search_button = browser.find_element_by_name('ctl00$ctl00$cphContent$cphSelectionCriteria$cmdFindNow')
    logger.info("click the search button to execute our search query...")
    search_button.click()
    sleep(sleep_seconds + (2 * random()))
    return None


def implement_new_user_agent():
    new_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36" #user_agent.random
    logger.info("new user agent is: {0}".format(new_user_agent))
    options.add_argument(f'User-Agent={new_user_agent}')
    browser = webdriver.Chrome(chrome_options=options, executable_path='/usr/local/bin/chromedriver')
    return browser

if __name__ == "__main__":
    main()
