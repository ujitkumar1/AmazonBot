import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.log import log


class AmazonPhoneSearch:
    """
       Represents a utility for searching and placing an order for a phone on Amazon.

       Attributes:
           uname (str): User's username for login.
           password (str): User's password for login.
           driver_path (str): Path to the ChromeDriver executable.
           start_price (float): Minimum price range for phone search.
           end_price (float): Maximum price range for phone search.
           product_name (str): Name of the product (phone) to search for.
           product_company (str): Company/brand of the product (phone) to search for.
           driver (WebDriver): Selenium WebDriver instance for browser automation.

       Methods:
           _initialize_driver(): Initializes the Selenium WebDriver.
           login(): Performs user login on Amazon.
           search_product(): Searches for the specified product on Amazon.
           apply_filters(): Applies filters such as brand and price range.
           extract_and_process_data(): Extracts and processes phone data.
           close_driver(): Closes the Selenium WebDriver.
           run(): Executes the complete phone search and order placement process.
    """

    def __init__(self, uname, password, driver_path, start_price, end_price, product_name, product_company):

        """
        Initializes the AmazonPhoneSearch instance.

        Args:
            uname (str): User's username for login.
            password (str): User's password for login.
            driver_path (str): Path to the ChromeDriver executable.
            start_price (float): Minimum price range for phone search.
            end_price (float): Maximum price range for phone search.
            product_name (str): Name of the product (phone) to search for.
            product_company (str): Company/brand of the product (phone) to search for.
        """
        log.info("AmazonPhoneSearch - __init__ method")
        self.driver_path = driver_path
        self.start_price = start_price
        self.end_price = end_price
        self.product_name = product_name
        self.product_company = product_company
        self.uname = uname
        self.password = password
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        """
        Initializes the Selenium WebDriver for browser automation.

        Returns:
            WebDriver: Initialized Selenium WebDriver instance.
        """

        log.info("Initializing Selenium Drive")
        service = Service(self.driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=service, options=options)
        log.info("Initiation Done")
        return driver

    def login(self):
        """
        Performs user login on Amazon using provided credentials.
        """
        log.info("AmazonPhoneSearch - Login Method")
        self.sigin_url = "https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"

        self.driver.get(self.sigin_url)

        try:
            unameO = self.driver.find_element(By.ID, "ap_email")
            unameO.send_keys(self.uname)
            unameO.send_keys(Keys.RETURN)
            time.sleep(7)

            passwordO = self.driver.find_element(By.ID, "ap_password")
            passwordO.send_keys(self.password)
            passwordO.send_keys(Keys.RETURN)

            log.info("Login Successful")

        except Exception as e:
            self.close_driver()
            log.error("Error Occurred", e)

    def search_product(self):
        """
        Searches for the specified product on Amazon.
        """
        try:
            log.info("Searching Product")
            self.driver.get("https://amazon.in")
            search_bar = self.driver.find_element(By.ID, "twotabsearchtextbox")
            search_bar.send_keys(self.product_name)
            search_bar.send_keys(Keys.RETURN)

        except Exception as e:
            self.close_driver()
            log.error("Error Occurred", e)

    def apply_filters(self):
        """
        Applies filters such as brand and price range to the search results.
        """
        log.info("Applying Filter")

        try:
            WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, "a-expander-prompt")))
            brand_filter = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//*[@id='p_89/{self.product_company}']/span/a/div/label/input")))
            self.driver.execute_script("arguments[0].click();", brand_filter)

            low_price = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "low-price")))
            high_price = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "high-price")))

            low_price.send_keys(self.start_price)
            high_price.send_keys(self.end_price)
            high_price.send_keys(Keys.RETURN)
            log.info("Price range applied")

        except Exception as e:
            self.close_driver()
            log.error("Error Occurred", e)

    def extract_and_process_data(self):
        """
        Extracts and processes phone data from search results.
        """
        log.info("Extracting Data...!")
        time.sleep(5)
        url = self.driver.page_source
        soup = BeautifulSoup(url, "html.parser")
        results = soup.find_all("div", class_="a-section a-spacing-small a-spacing-top-small")

        rating_dict = {}
        num = 0
        for result in results[1:]:
            ratings = result.text.split("₹")[0].split("stars ")[1].replace(",", "").replace(' ', "")
            rate = ""
            for i in ratings:
                if i.isdigit():
                    rate += i
            rating_dict[num] = int(rate)
            num += 1

        ratings_index = sorted(rating_dict.items(), key=lambda x: x[1])
        phone_name = ratings_index[-2][0] + 1
        var = str(results[phone_name])
        var = var.split("href")[-1].split(";")[0][2:]
        self.driver.get("https://www.amazon.in" + var)
        try:
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.NAME, "submit.add-to-cart"))).click()
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "attach-close_sideSheet-link"))).click()
            WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.ID, "nav-cart-count"))).click()
            log.info("Order Placed.....!")
            time.sleep(5)
        except Exception as e:
            self.close_driver()
            log.error("Error Occurred", e)

    def close_driver(self):
        """
        Closes the Selenium WebDriver instance.
        """
        self.driver.quit()

    def run(self):
        try:
            """
            Executes the complete phone search and order placement process.
            """
            self.login()
            self.search_product()
            self.apply_filters()
            self.extract_and_process_data()
        finally:
            self.close_driver()
