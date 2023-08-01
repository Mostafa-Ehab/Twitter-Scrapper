from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import re
import json
from time import sleep
from excel import Excel

class Main:
    def __init__(self):
        self.start_chrome()
        self.set_token()

    def start(self, page, start_date, end_date):
        self.page = page
        self.driver.get(self.page)

        i = 0
        data = []
        while True:
            i += 1
            if i in range(4, 11):
                self.delete_first_tweet()
                continue

            row = {}
            tweet = self.get_first_tweet()

            if not tweet:
                self.delete_first_tweet()
                continue

            url, re_tweet = self.get_url(tweet)
            date = self.get_date(tweet)
            text = self.get_text(tweet)
            lang = self.get_lang(tweet)

            is_media = self.check_media(tweet)

            num_reply = self.get_num_reply(tweet)
            num_retweet = self.get_num_retweet(tweet)
            num_like = self.get_num_like(tweet)
            num_views = self.get_num_views(tweet, is_media)

            row['text'] = text
            row['retweet'] = re_tweet
            row['date'] = date
            row['lang'] = lang
            row['num_retweet'] = num_retweet
            row['num_like'] = num_like
            row['num_quote'] = 0
            row['num_views'] = num_views
            row['num_reply'] = num_reply
            row['media'] = is_media
            row['url'] = url

            if datetime.strptime(date, "%d/%m/%Y") < datetime.strptime(start_date, "%d/%m/%Y"):
                # if i == 1:
                #     # print("Deleteing first tweet")
                #     self.delete_first_tweet()
                #     continue
                # else:
                #     break
                break
            elif datetime.strptime(date, "%d/%m/%Y") > datetime.strptime(end_date, "%d/%m/%Y"):
                self.delete_first_tweet()
                continue

            data.append(row)
            print(row["url"])

            self.delete_first_tweet()

        return data
    
    def resume(self, data):
        for row in data:
            url = row['url']
            print(url)
            self.page_data(url, row)
        
        return data
    
    def to_excel(self, data):
        Excel(data)

    def page_data(self, url, row):
        self.driver.get(url)
        
        self.get_media(row)

        row["num_quote"] = self.get_num_quotes()

    def save(self, file, data):
        with open('data.json', 'w', encoding='utf8') as file:
            json.dump(data, file)

    def load(self, file):
        with open("data.json", "r", encoding="utf8") as file:
            data = json.loads(file.read())
        return data

    def start_chrome(self):

        # instance of Options class allows
        # us to configure Headless Chrome
        options = Options()

        # this parameter tells Chrome that
        # it should be run without UI (Headless)
        options.headless = True

        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://twitter.com")

    def set_token(self):
        auth_token = "bb6234f5d7d817da458a54934ac450cfa4f137fa"
        src = f"""
                let date = new Date();
                date.setTime(date.getTime() + (7*24*60*60*1000));
                let expires = "; expires=" + date.toUTCString();

                document.cookie = "auth_token={auth_token}"  + expires + "; path=/";
            """
        self.driver.execute_script(src)

    def get_first_tweet(self):
        for i in range(6):
            try:
                tweet = self.driver.find_element(
                    By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div/div/div[1]/div/div/article")
            except NoSuchElementException:
                sleep(0.5)
                continue
            return tweet
        return False

    def get_url(self, tweet):
        urls_obj = tweet.find_elements(By.CSS_SELECTOR, "a")
        urls_list = [i.get_attribute("href") for i in urls_obj]
        if urls_list[1] != self.page:
            url = urls_list[4]
            re_tweet = True
        else:
            url = urls_list[3]
            re_tweet = False

        return url, re_tweet

    def get_date(self, tweet):
        # 2023-07-11T12:59:22.000Z

        date = tweet.find_element(
            By.CSS_SELECTOR, "time").get_attribute("datetime")[:10]
        date = datetime.strptime(date, '%Y-%m-%d')

        return date.strftime('%d/%m/%Y')

    def get_text(self, tweet):
        try:
            element = tweet.find_element(
                By.CSS_SELECTOR, "div[data-testid='tweetText']")

            return element.get_attribute("innerText")
        except NoSuchElementException:
            return ""

    def get_lang(self, tweet):
        try:
            element = tweet.find_element(
                By.CSS_SELECTOR, "div[data-testid='tweetText']")
            lang = element.get_attribute("lang")
        except NoSuchElementException:
            return ""

        # if lang == "ar":
        #     parsed_lang = "Arabic"
        # elif lang == "en":
        #     parsed_lang = "English"
        # else:
        #     print(lang)
        #     raise Exception("Please Add this Language")

        # return parsed_lang

        return lang

    def get_num_reply(self, tweet):
        text = tweet.find_element(
            By.CSS_SELECTOR, "div[data-testid='reply']").get_attribute("aria-label")
        num = [int(s) for s in re.findall(r'\b\d+\b', text)]

        if num:
            return num[0]
        else:
            return 0

    def get_num_retweet(self, tweet):
        text = tweet.find_element(
            By.CSS_SELECTOR, "div[data-testid='retweet']").get_attribute("aria-label")
        num = [int(s) for s in re.findall(r'\b\d+\b', text)]

        if num:
            return num[0]
        else:
            return 0

    def get_num_like(self, tweet):
        text = tweet.find_element(
            By.CSS_SELECTOR, "div[data-testid='like']").get_attribute("aria-label")

        num = [int(s) for s in re.findall(r'\b\d+\b', text)]

        if num:
            return num[0]
        else:
            return 0

    def get_num_views(self, tweet, media):
        if media:
            element = tweet.find_element(
                By.XPATH, "./div/div/div[2]/div[2]/div[4]")
        else:
            element = tweet.find_element(
                By.XPATH, "./div/div/div[2]/div[2]/div[3]")

        text = element.find_element(
            By.XPATH, "./div/div[4]/a").get_attribute("aria-label")
        num = [int(s) for s in re.findall(r'\b\d+\b', text)]

        if num:
            return num[0]
        else:
            return 0

    def check_media(self, tweet):
        try:
            tweet.find_element(By.XPATH, "./div/div/div[2]/div[2]/div[4]")
            media = True
        except NoSuchElementException:
            media = False

        return media

    def delete_first_tweet(self):
        tweet = self.driver.find_element(
            By.XPATH, f"//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div/div/div[{1}]")
        self.driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, tweet)

    def get_media(self, row):
        if row["media"]:
            while True:
                try:
                    media = self.driver.find_element(
                        By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div/div/div[1]/div/div/article/div/div/div[3]/div[2]")
                except NoSuchElementException:
                    try:
                        media = self.driver.find_element(
                            By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div/div/div[2]/div/div/article/div/div/div[3]/div[2]")
                    except NoSuchElementException:
                        try:
                            media = self.driver.find_element(
                                By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div/div/div[3]/div/div/article/div/div/div[3]/div[2]")
                        except NoSuchElementException:
                            continue
                break

            try:
                media.find_element(
                    By.CSS_SELECTOR, "div[data-testid='videoPlayer']")
                row["media"] = "Video"
            except NoSuchElementException:
                pass

            try:
                media.find_element(
                    By.CSS_SELECTOR, "div[data-testid='tweetPhoto']")
                if row["media"] != "Video":
                    row["media"] = "Image"

            except NoSuchElementException:
                pass
            
            if not row["retweet"]:
                try:
                    media.find_element(
                        By.CSS_SELECTOR, "div[data-testid='tweetText']")
                    row["retweet"] = True
                    row["media"] = "No media"
                except NoSuchElementException:
                    pass

        else:
            row["media"] = "No media"

    def get_num_quotes(self):
        while True:
            try:
                try:
                    data_list = self.driver.find_element(
                        By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div/div/div[1]/div/div/article/div/div/div[3]/div[5]")
                except NoSuchElementException:
                    try:
                        data_list = self.driver.find_element(
                            By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div/div/div[2]/div/div/article/div/div/div[3]/div[5]")
                    except NoSuchElementException:
                        try:
                            data_list = self.driver.find_element(
                                By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div/div/div[3]/div/div/article/div/div/div[3]/div[5]")
                        except NoSuchElementException:
                            continue

                for element in data_list.find_elements(By.XPATH, "./div"):
                    text = element.get_attribute("innerText")
                    if "Quotes" in text:
                        return [int(s) for s in re.findall(r'\b\d+\b', text)][0]
                return 0
            except NoSuchElementException:
                continue

    
    def check_date(date):
        try:
            datetime.strptime(date, '%d/%m/%Y')
            return True
        except:
            return False


if __name__ == "__main__":
    url = input("Please enter page url: ")

    while True:
        start_date = input("Please enter start date (Ex: 25/01/2023): ")
        if Main.check_date(start_date):
            break
        print("Invalid date, ", end="")

    while True:
        end_date = input("Please enter end date (Ex: 25/12/2023): ")
        if Main.check_date(end_date):
            break
        print("Invalid date format, ", end="")

    main = Main()
    print("Fetching Tweets --------------------------------- ")
    data = main.start(url, start_date, end_date)
    main.save("data.json", data)

    print("Processing -------------------------------------- ")
    # data = main.load("data.json")
    data = main.resume(data)
    main.save("data.json", data)

    print("Saving ------------------------------------------ ")
    # data = main.load("data.json")
    main.to_excel(data)
