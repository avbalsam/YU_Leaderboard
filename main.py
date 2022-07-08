import os
import threading
import time

from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template
from selenium.common.exceptions import WebDriverException, NoSuchElementException


def run_web_app():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


app = Flask(__name__)

t = threading.Thread(target=run_web_app)
t.start()


@app.route("/")
def index():
    return "Go to /teachers, /publications, or /series to see rankings!"


@app.route("/<name>")
def main_page(name):
    return render_template('rankings.html', list_header=f"{name.capitalize()} Ranked", teachers_ranked=get_rankings(name),
                           site_title="YULeaderboard.com")


def get_rankings(name):
    if name == 'teachers':
        ranking = "navTeachers"
    elif name == 'series':
        ranking = "navSeries"
    elif name == 'venues':
        ranking = "navVenues"
    else:
        return list()

    # Depending on size of page, find dropdown or side menu
    try:
        div = driver.find_element(by=By.ID, value=f"{ranking}DropDown")
    except NoSuchElementException:
        div = driver.find_element(by=By.ID, value=f"{ranking}Holder")
        div = div.find_element(by=By.ID, value=f"{ranking}DropDown")

    el_list = div.find_elements(by=By.XPATH, value="//a[@class='nav-item']")

    unordered_list = list()
    for item in el_list:
        name = item.get_attribute('innerHTML')
        link = item.get_attribute('href')
        index = name.index("<span>")
        name = name[:index]
        shiur_count = item.find_element(by=By.TAG_NAME, value='span')
        shiur_count = shiur_count.get_attribute('innerHTML')
        shiur_count = int(shiur_count.replace("(", "").replace(")", "").replace(",", ""))
        unordered_list.append({'name': name.strip(), 'shiur_count': shiur_count, 'link': link})
        print(f"Name: {name.strip()}, Shiurim: {shiur_count}, Link: {link}")

    ranked_list = sorted(unordered_list, key=lambda teacher: teacher['shiur_count'], reverse=True)

    return ranked_list


def print_ranked_list(ranked_list):
    print("\n\n\n\n\nRanking on YU Torah by shiurim given:\n")
    for t in range(0, len(ranked_list)):
        print(f"{t + 1}: {ranked_list[t]['name']}; Shiur Count: {ranked_list[t]['shiur_count']}")


chrome_options = webdriver.ChromeOptions()

# setup chrome for selenium (needed for heroku builds)
s = Service(os.environ.get("CHROMEDRIVER_PATH"))
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=s, chrome_options=chrome_options)

time.sleep(1)
driver.get('http://www.yutorah.com')
time.sleep(1)
print("Window maximized...")
driver.maximize_window()
time.sleep(1)
