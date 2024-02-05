from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime
from time import sleep
import traceback


class Tweet:
    def __init__(self,
            driver: webdriver.Chrome,
            Ad: list
    ):
        self.driver = driver
        self.Ad = Ad

        while True:
            try:
                self.tweet = self.__get_first_tweet()
                
                self.__remove_pinned()

                self.tweet_url, self.retweet = self.__get_tweet_url()
                self.tweet_date = self.__get_tweet_date()
                self.tweet_text = self.__get_tweet_text()
                self.tweet_lang = self.__get_tweet_lang()
                self.tweet_num_likes = self.__get_tweet_num_likes()
                self.tweet_num_retweet = self.__get_tweet_num_retweet()
                self.tweet_num_reply = self.__get_tweet_num_reply()
            
            except TypeError:
                self.Ad.append(self.tweet)
                sleep(1)
                driver.execute_script("arguments[0].scrollIntoView();", self.tweet)
                continue

            except Exception:
                print(traceback.format_exc())
                sleep(1)
                # driver.execute_script("arguments[0].scrollIntoView();", self.tweet)
                input("An error occured: ")
                continue
            break

        self.__delete_tweet()

    
    def get_url(self) -> str:
        return self.tweet_url
    
    def get_date(self) -> str:
        return self.tweet_date
    
    def get_text(self) -> str:
        return self.tweet_text
    
    def get_lang(self) -> str:
        return self.tweet_lang
    
    def get_num_likes(self) -> str:
        return self.tweet_num_likes
    
    def get_num_retweet(self) -> str:
        return self.tweet_num_retweet

    def get_num_reply(self) -> str:
        return self.tweet_num_reply
    

    def __get_first_tweet(self) -> WebElement:
        while True:
            try:
                tweets = self.driver.find_elements(By.CSS_SELECTOR, "article[data-testid='tweet']")
                for tweet in tweets:
                    if tweet not in self.Ad:
                        return tweet
            except IndexError:
                sleep(0.5)
                continue
    
    
    def __remove_pinned(self):
        while True:
            try:
                if self.tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="socialContext"]').get_attribute("innerText") == "Pinned":
                    print("Skipping pinned...")
                    raise TypeError
                
            except NoSuchElementException:
                pass

            except StaleElementReferenceException:
                sleep(1)
                continue

            break


    def __get_tweet_url(self) -> (str, bool):
        urls = self.tweet.find_elements(By.CSS_SELECTOR, "a")

        if urls[0].get_attribute("href") == urls[1].get_attribute("href"):
            url = urls[3].get_attribute("href")
            re_tweet = False
        else:
            url = urls[4].get_attribute("href")
            re_tweet = True

        return url, re_tweet


    def __get_tweet_date(self) -> str:
        # 2023-07-11T12:59:22.000Z
        try:
            date = self.tweet.find_element(
                By.CSS_SELECTOR, "time").get_attribute("datetime")[:10]
            date = datetime.strptime(date, '%Y-%m-%d')
        except NoSuchElementException:
            raise TypeError

        return date.strftime('%d/%m/%Y')


    def __get_tweet_text(self) -> str:
        try:
            element = self.tweet.find_element(
                By.CSS_SELECTOR, "div[data-testid='tweetText']")

            return element.get_attribute("innerText")
        except NoSuchElementException:
            return ""


    def __get_tweet_lang(self) -> str:
        try:
            element = self.tweet.find_element(
                By.CSS_SELECTOR, "div[data-testid='tweetText']")
            return element.get_attribute("lang")
        except NoSuchElementException:
            return ""
        
    # def check_media(self):
    #     try:
    #         self.tweet.find_element(By.XPATH, "./div/div/div[2]/div[2]/div[4]")
    #         media = True
    #     except NoSuchElementException:
    #         media = False

    #     return media
    
    def __get_tweet_num_likes(self):
        return self.tweet.find_element(By.CSS_SELECTOR, "div[data-testid='like']").get_attribute("innerText")

    def __get_tweet_num_retweet(self):
        return self.tweet.find_element(By.CSS_SELECTOR, "div[data-testid='retweet']").get_attribute("innerText")
    
    def __get_tweet_num_reply(self):
        return self.tweet.find_element(By.CSS_SELECTOR, "div[data-testid='reply']").get_attribute("innerText")


    def __delete_tweet(self):
        self.driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, self.tweet)
