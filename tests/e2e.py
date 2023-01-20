# import all required frameworks
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from uuid import UUID


import random
import string


BASE_URL = "localhost:17154"

def get_random_string(length: int) -> str:
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


class LampexTest(unittest.TestCase):

    # initialization of webdriver
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(30)

    # cleanup method called after every test performed

    def test_e2e(self):
        ## TEST 10 PRODUCTS DIFFERENT CATEGORIES

        driver = self.driver
        driver.get(f"https://{BASE_URL}/934-oswietlenie")

        for i in range(5):
            element = driver.find_element(By.XPATH, "//*[contains(text(), 'Dostępny')]")
            element.click()
            time.sleep(4)

            # click on product
            element = driver.find_element(By.XPATH,
                                          f"/html/body/main/section/div/div[2]/section/section/div[3]/div[1]/div[{i + 1}]/article/div/div[1]/a/img")
            element.click()
            # click on amount
            element = driver.find_element(By.XPATH,
                                          "/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[2]/div/div[1]/div/span[3]/button[1]/i")
            for j in range(i%2):
                element.click()
            # click buy
            element = driver.find_element(By.XPATH,
                                          "/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[2]/div/div[2]/button")
            element.click()
            time.sleep(2)
            # click continue shopping
            element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/button")
            element.click()
            time.sleep(2)
            driver.get(f"https://{BASE_URL}/934-oswietlenie")

        driver.get(f"https://{BASE_URL}/939-do-wnetrz")


        for i in range(5):
            time.sleep(1)
            element = driver.find_element(By.XPATH, "//*[contains(text(), 'Dostępny')]")
            element.click()
            time.sleep(4)

            # click on product
            element = driver.find_element(By.XPATH,
                                          f"/html/body/main/section/div/div[2]/section/section/div[3]/div[1]/div[{i + 1}]/article/div/div[1]/a/img")
            element.click()
            # click on amount
            element = driver.find_element(By.XPATH,
                                          "/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[2]/div/div[1]/div/span[3]/button[1]/i")
            for j in range(i%2):
                element.click()
            # click buy
            element = driver.find_element(By.XPATH,
                                          "/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[2]/div/div[2]/button")
            element.click()
            time.sleep(3)
            # click continue shopping
            element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/button")
            element.click()
            time.sleep(2)
            driver.get(f"https://{BASE_URL}/939-do-wnetrz")


        time.sleep(10)
        # REMOVE ELEMENT FROM BASKET
        # click basket
        driver.get(f"https://{BASE_URL}/koszyk?action=show")
        time.sleep(5)
        element = driver.find_element(By.XPATH,
                                      "/html/body/main/section/div/div/section/div/div[1]/div/div[2]/ul/li/div/div[3]/div/div[3]/div/a/i")
        element.click()
        time.sleep(5)

        # CLICK BUY

        element = driver.find_element(By.XPATH,
                                      "/html/body/main/section/div/div/section/div/div[2]/div[1]/div[2]/div/a")
        element.click()

        # fill form
        element = driver.find_element("name", "id_gender")
        element.click()

        element = driver.find_element("name", "firstname")
        element.send_keys("Jan")

        element = driver.find_element("name", "lastname")
        element.send_keys("Kowalski")

        element = driver.find_element("name", "email")
        element.send_keys(f"{get_random_string(8)}@example.com")

        element = driver.find_element("name", "password")
        element.send_keys(get_random_string(10))

        element = driver.find_element("name", "customer_privacy")
        element.click()

        element = driver.find_element("name", "psgdpr")
        element.click()

        # next

        element = driver.find_element(By.XPATH,
                                      "/html/body/main/section/div/div/section/div/div[1]/section[1]/div/div[2]/div[1]/form/footer/button")
        element.click()

        # fill address
        element = driver.find_element("name", "address1")
        element.send_keys("Gdanska 1")

        element = driver.find_element("name", "postcode")
        element.send_keys("12-131")

        element = driver.find_element("name", "city")
        element.send_keys("Gdańsk")

        element = driver.find_element("name", "phone")
        element.send_keys("123123123")

        # next
        element = driver.find_element(By.XPATH,
                                      "/html/body/main/section/div/div/section/div/div[1]/section[2]/div/div/form/div/div/footer/button")
        element.click()

        # order method
        element = driver.find_element(By.XPATH,
                                      "/html/body/main/section/div/div/section/div/div[1]/section[3]/div/div[2]/form/div/div[1]/div[4]/div/span")
        element.click()
        time.sleep(5)

        # next
        element = driver.find_element(By.XPATH,
                                      "/html/body/main/section/div/div/section/div/div[1]/section[3]/div/div[2]/form/button")
        element.click()

        # pay at delivery
        element = driver.find_element(By.XPATH,
                                      "/html/body/main/section/div/div/section/div/div[1]/section[4]/div/div[2]/div[4]/div/span")
        element.click()
        time.sleep(3)

        element = driver.find_element("name", "conditions_to_approve[terms-and-conditions]")
        element.click()

        # order
        element = driver.find_element(By.XPATH, "/html/body/main/section/div/div/section/div/div[1]/section[4]/div/div[3]/div[1]/button")
        element.click()

        delay = 120
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/main/section/div/div/section/section[2]/div/div/div[1]/div[1]/h3[1]")))
        except TimeoutException:
            print(
            "Loading took too much time!")

        time.sleep(10)
        assert "Twoje zamówienie zostało potwierdzone" in driver.page_source
        time.sleep(5)

        driver.get(f"https://{BASE_URL}/historia-zamowien")

        assert "Oczekiwanie na płatność" in driver.page_source

        time.sleep(5)

    def tearDown(self):
        self.driver.close()



# execute the script
if __name__ == "__main__":
    unittest.main()
