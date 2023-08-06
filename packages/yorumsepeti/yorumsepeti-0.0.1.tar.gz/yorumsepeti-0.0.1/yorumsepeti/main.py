import time
from selenium import webdriver
import csv


def scroll(driver):
    """
    Function for scrolling to end of the page.
    :param selenium driver:
    :return None:
    """
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)


def get_restaurant_names(num):
    """

    :param number restaurants:
    :return list of restaurant names:
    """
    url = 'https://www.yemeksepeti.com/istanbul/restoran-arama'

    driver = webdriver.Chrome(executable_path="yorumsepeti/chromedriver.exe")
    driver.get(url)

    restaurants = []
    while len(restaurants) < num:
        restaurants = driver.find_elements_by_class_name('restaurantName ')
        try:
            scroll(driver)
        except:
            break

    return restaurants


def get_restaurant_urls(restaurants):
    """

    :param restaurants:
    :return:
    """
    urls = []
    for m in restaurants:
        rest_name = str(m.get_attribute("innerHTML").split("<")[0]).strip()

        rest_name = rest_name.lower()
        rest_name = rest_name.replace(",", "").replace("(", "").replace(")", "").replace("-", "").replace(".", "") \
            .replace("&", "").replace("amp;", "").replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş",
                                                                                                                "s").replace(
            "ö", "o") \
            .replace("ç", "c").replace("/", "").replace("\\", "").replace("'", "").replace("  ", " ").replace(" ", "-") \
            .replace("â", "a")

        url = 'https://www.yemeksepeti.com/' + rest_name + '-istanbul'

        urls.append(url)

    return urls


def get_restaurant_comments(urls):
    driver = webdriver.Chrome(executable_path="yorumsepeti/chromedriver.exe")
    comments = []
    for n in urls:
        driver.get(n)

        comment = driver.find_elements_by_class_name('user')
        for i in comment:
            if "Restoran Cevabı" in str(i.get_attribute("innerHTML")):
                continue
            if "<p>" not in str(i.get_attribute("innerHTML")):
                continue

            if "Hız: " in str(i.get_attribute("innerHTML")):
                speed = str(i.get_attribute("innerHTML")).split("Hız: ")[1].split("<")[0]
            else:
                speed = "-"
            if "Servis: " in str(i.get_attribute("innerHTML")):
                service = str(i.get_attribute("innerHTML")).split("Servis: ")[1].split("<")[0]
            else:
                service = "-"
            if "Lezzet: " in str(i.get_attribute("innerHTML")):
                flavour = str(i.get_attribute("innerHTML")).split("Lezzet: ")[1].split("<")[0]
            else:
                flavour = "-"

            review = str(i.get_attribute("innerHTML")).split("<p>")[1].split("</p>")[0]

            if "(Bu yorum Yemeksepeti tarafından otomatik yapılmıştır.)" in review:
                continue

            tuple = [speed, service, flavour, review]

            comments.append(tuple)

    return comments


def get_comments(num):
    names = get_restaurant_names(num)
    urls = get_restaurant_urls(names)
    comments = get_restaurant_comments(urls)

    with open('comments.csv', 'w', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["speed", "service", "flavour", "review"])
        writer.writerows(comments)
