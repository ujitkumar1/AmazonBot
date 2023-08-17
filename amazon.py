import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

class AmazonPhoneSearch:
    def __init__(self, uname,password,driver_path, start_price, end_price, product_name, product_company):
        self.driver_path = driver_path
        self.start_price = start_price
        self.end_price = end_price
        self.product_name = product_name
        self.product_company = product_company
        self.uname = uname
        self.password = password
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        print("Initializing Drive")
        service = Service(self.driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=service, options=options)
        print("Initiation Done")
        return driver

    def login(self):
        self.sigin_url = "https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
        self.driver.get(self.sigin_url)

        unameO = self.driver.find_element(By.ID, "ap_email")
        unameO.send_keys(self.uname)
        unameO.send_keys(Keys.RETURN)
        time.sleep(7)

        passwordO = self.driver.find_element(By.ID, "ap_password")
        passwordO.send_keys(self.password)
        passwordO.send_keys(Keys.RETURN)


    def search_product(self):
        print("Searching Product")
        self.driver.get("https://amazon.in")
        search_bar = self.driver.find_element(By.ID, "twotabsearchtextbox")
        search_bar.send_keys(self.product_name)
        search_bar.send_keys(Keys.RETURN)

    def apply_filters(self):
        print("Applying Filter")
        WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, "a-expander-prompt")))
        brand_filter = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, f"//*[@id='p_89/{self.product_company}']/span/a/div/label/input")))
        self.driver.execute_script("arguments[0].click();", brand_filter)

        low_price = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "low-price")))
        high_price = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "high-price")))

        low_price.send_keys(self.start_price)
        high_price.send_keys(self.end_price)
        high_price.send_keys(Keys.RETURN)
        print("Price range applied")

    def extract_and_process_data(self):
        print("Extracting Data...!")
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
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID, "attach-close_sideSheet-link"))).click()
            WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.ID, "nav-cart-count"))).click()
            print("Order Placed.....!")
            time.sleep(5)
        except:
            print(Exception)
            pass

    def close_driver(self):
        self.driver.quit()

    def run(self):
        try:
            self.login()
            self.search_product()
            self.apply_filters()
            self.extract_and_process_data()
        finally:
            self.close_driver()

# if __name__ == "__main__":
#     driver_path = "C:\Program Files (x86)\chromedriver.exe"
#     start_price = "10000"
#     end_price = "20000"
#     product_name = "smartphone"
#     product_company = "Samsung"
#
#     search_instance = AmazonPhoneSearch(driver_path, start_price, end_price, product_name, product_company)
#     search_instance.run()
