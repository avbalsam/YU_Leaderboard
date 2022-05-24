import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_rankings(div):
    el_list = div.find_elements_by_xpath(".//a[@class='nav-item']")

    unordered_list = list()
    for item in el_list:
        name = item.get_attribute('innerHTML')
        index = name.index("<span>")
        name = name[:index]
        shiur_count = item.find_element_by_tag_name('span')
        shiur_count = shiur_count.get_attribute('innerHTML')
        shiur_count = int(shiur_count.replace("(", "").replace(")", "").replace(",", ""))
        unordered_list.append({'name': name.strip(), 'shiur_count': shiur_count})
        # print(f"Name: {name.strip()}, Shiurim: {shiur_count}")

    ranked_list = sorted(unordered_list, key=lambda teacher: teacher['shiur_count'], reverse=True)

    return ranked_list


chrome_options = webdriver.ChromeOptions()

try:
    # setup chrome for selenium (needed for heroku builds)
    s = Service(os.environ.CHROMEDRIVER_PATH)
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
except:
    s = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=s, chrome_options=chrome_options)

driver.get('http://www.yutorah.com')

teachers_div = driver.find_element_by_id("navTeachersDropDown")
locations_div = driver.find_element_by_id("navVenuesDropDown")
teachers_ranked = get_rankings(teachers_div)
locations_ranked = get_rankings(locations_div)

print("\n\n\n\n\nRanking of all teachers on YU Torah by shiurim given:\n")
for t in range(0, len(teachers_ranked)):
    print(f"{t + 1}: {teachers_ranked[t]['name']}; Shiur Count: {teachers_ranked[t]['shiur_count']}")

print("\n\n\n\n\nRanking of all locations on YU Torah by shiurim given:\n")
for t in range(0, len(locations_ranked)):
    print(f"{t + 1}: {locations_ranked[t]['name']}; Shiur Count: {locations_ranked[t]['shiur_count']}")