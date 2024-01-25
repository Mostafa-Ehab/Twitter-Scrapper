from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from logger import Logger
import json

from tweet import Tweet
from excel import Excel

def main():
    log.warning("Loading configurations...")
    if not conf["token"]:
        log.warning("Please set your access token in './files/conf.json' file")
        log.warning("For more info visit this link: https://youtu.be/uHOz7BSPXCo")
        input("\n\tPress any key to exit...")
        return

    driver = open_driver(conf["headless"], conf["userAgent"])
    driver.get("https://twitter.com/")
    set_token(driver, conf["token"])
    driver.get("https://twitter.com/")

    log.warning("Starting...")
    data = profile_search(driver)

    log.warning("Saving...")
    Excel(data, conf["output_form"])


def profile_search(
        driver: webdriver.Chrome
):
    url = input("Enter profile URL: ")
    num = int(input("Enter the required number of tweets: "))
    driver.get(url)

    log.warning("Fetching...")
    Ad = []
    results = []
    while len(results) < num:
        tweet = Tweet(driver, Ad)

        data = {}

        data["URL"] = tweet.get_url()
        data["Date"] = tweet.get_date()
        data["Text"] = tweet.get_text()
        data["Lang"] = tweet.get_lang()
        data["Likes"] = tweet.get_num_likes()
        data["Retweets"] = tweet.get_num_retweet()
        data["Replies"] = tweet.get_num_reply()

        results.append(data)

        json.dump(results, open("./files/temp.json", "w"))
        
        log.info(f"{len(results) + 1} : {data['URL']}")

    return results


def open_driver(
        headless: bool,
        agent: str
) -> webdriver.Chrome:
    
    options = Options()

    options.add_argument('--log-level=3')
    options.add_argument('ignore-certificate-errors')

    if headless:
        options.add_argument('--headless')

    options.add_argument(f"user-agent={agent}")
    
    driver = webdriver.Chrome(options=options)

    return driver

def set_token(
        driver: webdriver.Chrome,
        token: str
) -> None:
    src = f"""
            let date = new Date();
            date.setTime(date.getTime() + (7*24*60*60*1000));
            let expires = "; expires=" + date.toUTCString();

            document.cookie = "auth_token={token}"  + expires + "; path=/";
        """
    driver.execute_script(src)

def load_conf() -> dict:
    with open("./files/conf.json", "r") as file:
        return json.loads(file.read())


if __name__  == "__main__":
    log = Logger()
    try:
        conf = load_conf()
    except Exception:
        log.warning("Sorry and error occured, Please check your config file")
        input("\n\tPress any key to exit...")
    else:
        main()


