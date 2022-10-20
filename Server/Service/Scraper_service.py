import datetime
import os
import re
import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

from Server.Service.OLX_Service import create_olx_post, get_with_limit
from Server.Service.Scraper_Meta_Service import create_info, get_info


def send_mail(email, size=20):

    # setting up mailing server
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)

    server.starttls()

    # using custom created mail for this process
    server.login('qpwoeireurty@outlook.com', 'test@evas')

    # creating Message body
    msg = MIMEMultipart()
    msg['From'] = "qpwoeireurty@outlook.com"
    msg['To'] = email
    msg['Subject'] = "This is TEST"

    # get listing from DB using given size
    list_of_ads = get_with_limit(size)

    message = ""

    number = 1
    for ad in list_of_ads:
        message += "--------------Listing number--------------: " + str(number) + "\n" \
                                                                    "title: " + ad.get('title', "Empty") + "\n\n" \
                                                                                                           "price: " + str(
            ad.get('price', "Empty")) + "\n\n" \
                                        "condition: " + ad.get('condition', "Empty") + "\n\n" \
                                                                                       "description: " + ad.get(
            'description', "Empty") + "\n\n" \
                                      "advertiser_name: " + ad.get('advertiser_name', "Empty") + "\n\n" \
                                                                                                 "mobile: " + str(
            ad.get('mobile', "Empty")) + "\n\n" \
                                         "location: " + ad.get('location', "Empty") + "\n\n\n"
        number += 1

    msg.attach(MIMEText(message, 'plain'))

    server.send_message(msg)

    print("mail sent")


def scrape_data(search_keyword, email, size=20):
    try:
        # new day will be used after getting meta info and the last date that the scraper was used in
        new_day = True
        last_date = get_info("last_date")
        # last_date = None
        if last_date is not None:
            if last_date.meta_info_value == str(datetime.date.today()):
                new_day = False

        if new_day:

            # setting up selenium details
            rootdir = os.getcwd()
            Selenium_Chrome_WebDriver = os.path.join(rootdir, "Selenium", "chromedriver.exe")

            link = 'https://www.olx.com.eg/en/'

            # using headless option
            options = Options()
            # options.add_argument('--no-sandbox')
            options.add_argument('headless')
            # options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(executable_path=Selenium_Chrome_WebDriver, chrome_options=options)
            # driver = webdriver.Chrome(executable_path=Selenium_Chrome_WebDriver)

            driver.get(link)

            # login process

            wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Login']")))
            driver.find_element_by_xpath("//button[@aria-label='Login']").click()

            wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Continue with Email']")))
            continue_with_mail_btn_el = driver.find_element_by_xpath("//span[text()='Continue with Email']")
            continue_with_mail_btn_el.click()

            wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
            driver.find_element_by_xpath("//input[@type='email']").send_keys("qpwoeireurty@outlook.com")

            driver.find_element_by_xpath("//button[@class='_5fd7b300 f3d05709' and @type='button']").click()

            wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
            driver.find_element_by_xpath("//input[@type='password']").send_keys("test@evas1")

            driver.find_element_by_xpath("//button[@class='_5fd7b300 f3d05709' and @type='button']").click()

            # get listings
            search_field_el = driver.find_element_by_xpath("//input[@class='fc60720d' and @type='search']")
            search_field_el.send_keys(search_keyword)
            search_field_el.send_keys(Keys.ENTER)

            new_page = True
            current_url = driver.current_url
            number_of_page = 1
            item_number = 0

            while new_page and item_number <= 100:

                print("at page: " + str(number_of_page))

                wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//li[@aria-label='Listing']")))
                ads_listing = driver.find_elements_by_xpath("//li[@aria-label='Listing']")
                ads_listing_links = []

                # store links of each lisiting to loop on
                for listing in ads_listing:
                    link = listing.find_element_by_xpath(".//article//div//a").get_attribute("href")
                    ads_listing_links.append(link)

                # start looping on each link and navigate to it then retreive all data required
                for ad_link in ads_listing_links:
                    driver.get(ad_link)

                    wait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Wallpaper Ad Body']")))

                    try:
                        wait(driver, 10).until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div._676a547f:nth-child(1) > div:nth-child(1) > span:nth-child(2)")))
                        price = driver.find_element_by_css_selector(
                            "div._676a547f:nth-child(1) > div:nth-child(1) > span:nth-child(2)").text
                        price = re.sub('[^A-Za-z0-9]+', '', str(price))
                        if not price.isnumeric():
                            price = "0"
                    except Exception:
                        price = "0"

                    try:
                        wait(driver, 10).until(EC.presence_of_element_located(
                            (By.XPATH, "//div[@aria-label='Overview']//h1[@class='a38b8112']")))
                        title = driver.find_element_by_xpath("//div[@aria-label='Overview']//h1[@class='a38b8112']").text
                    except Exception:
                        title = ""

                    try:
                        wait(driver, 10).until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div._676a547f:nth-child(4) > div:nth-child(1) > span:nth-child(2)")))
                        condition = driver.find_element_by_css_selector(
                            "div._676a547f:nth-child(4) > div:nth-child(1) > span:nth-child(2)").text
                    except Exception:
                        condition = ""

                    try:
                        wait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                               "//div[@aria-label='Details and "
                                                                               "description']//div["
                                                                               "@class='_59317dec']//div["
                                                                               "@class='_0f86855a']//span")))
                        description = driver.find_element_by_xpath(
                            "//div[@aria-label='Details and description']//div[""@class='_59317dec']//div["
                            "@class='_0f86855a']//span").text
                    except Exception:
                        description = ""

                    try:
                        wait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                               "//div[@class='_1075545d _6caa7349 "
                                                                               "_42f36e3b d059c029']//span["
                                                                               "@class='_261203a9 _2e82a662']")))
                        advertiser_name = driver.find_element_by_xpath(
                            "//div[@class='_1075545d _6caa7349 _42f36e3b d059c029']//span[@class='_261203a9 _2e82a662']").text
                    except Exception:
                        advertiser_name = ""

                    try:
                        wait(driver, 10).until(EC.presence_of_element_located(
                            (By.XPATH, "//div[@class='_1075545d e3cecb8b _5f872d11']//span[@aria-label='Location']")))
                        location = driver.find_element_by_xpath(
                            "//div[@class='_1075545d e3cecb8b _5f872d11']//span[@aria-label='Location']").text
                    except Exception:
                        location = ""

                    try:
                        wait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//span[@class='_8918c0a8 _09eb0c84 _79855a31']")))
                        driver.find_element_by_xpath("//span[@class='_8918c0a8 _09eb0c84 _79855a31']").click()

                        wait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "._45d98091")))
                        # mobile = driver.find_element_by_xpath("//span[@class='_34a7409b _45d98091 _2e82a662']").text
                        mobile = driver.find_element_by_css_selector("._45d98091").text
                    except Exception:
                        mobile = "0"

                    # saving the fetched listing in DB
                    create_olx_post(link=ad_link, price=int(price), title=title,
                                    condition=condition, description=description, advertiser_name=advertiser_name,
                                    location=location, mobile=int(mobile))
                    print("added item number: " + str(item_number))
                    item_number += 1

                # getting back after looping on the listing to get next page
                driver.get(current_url)
                next_el = wait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//a[@class='d73e7494']//div[@title='Next']")))
                if next_el is not None:
                    # print("next page exists")
                    next_el.click()
                    current_url = driver.current_url
                    new_page = True
                    number_of_page += 1
                else:
                    # print("end of pages")
                    new_page = False

            driver.quit()

            # save today's date in meta info for another run
            create_info(meta_info_name='last_date', meta_info_value=str(datetime.date.today()))

            # using the DB instances added to send email with desired size
            send_mail(email, size)
            return {"status": "data scrapped", "msg": "data added to DB and email sent"}
        else:
            # using the DB instances added to send email with desired size
            send_mail(email, size)
            return {"status": "failed to scrape data", "msg": "same day can not scrape data. but emails was sent"}
    except Exception:
        traceback.print_exc()
        return {"status": "failure", "msg": "issue happened during process please contact admin"}
