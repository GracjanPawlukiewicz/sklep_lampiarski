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


def get_random_string(length: int) -> str:
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


# inherit TestCase Class and create a new test class
class LampexTest(unittest.TestCase):

    # initialization of webdriver
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(options=options)

    # cleanup method called after every test performed

    def test_is_10_products_different_categories(self):
        driver = self.driver
        driver.get("https://10.144.0.1/prestashop/2-strona-glowna")
        element = driver.find_element(By.XPATH, "/html/body/main/section/div/div[2]/section/div[2]/ul/li[1]/div/a")
        element.click()

        element = driver.find_element(By.XPATH, "/html/body/main/section/div/div[2]/section/div[2]/ul/li[2]/div/a")
        element.click()
        for i in range(2):
            # click on product
            element = driver.find_element(By.XPATH, f"/html/body/main/section/div/div[2]/section/section/div[3]/div[1]/div[{i+1}]/article/div/div[1]/a/img")
            element.click()
            # click on amount
            element = driver.find_element(By.XPATH, "/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[2]/div/div[1]/div/span[3]/button[1]/i")
            for j in range(i+1):
                element.click()
            # click buy
            element = driver.find_element(By.XPATH, "/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[2]/div/div[2]/button")
            element.click()
            time.sleep(1)
            # click continue shopping
            element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/button")
            element.click()
            time.sleep(1)
            driver.get("https://10.144.0.1/prestashop/2-strona-glowna")
            element = driver.find_element(By.XPATH, "/html/body/main/section/div/div[2]/section/div[2]/ul/li[1]/div/a")
            element.click()

            element = driver.find_element(By.XPATH, "/html/body/main/section/div/div[2]/section/div[2]/ul/li[2]/div/a")
            element.click()
        driver.get("https://10.144.0.1/prestashop/2-strona-glowna")

        element = driver.find_element(By.XPATH, "/html/body/main/section/div/div[2]/section/div[2]/ul/li[2]/div/a")
        element.click()

        for i in range(2):
            # click on product
            element = driver.find_element(By.XPATH, f"/html/body/main/section/div/div[2]/section/section/div[3]/div[1]/div[{i+1}]/article/div/div[1]/a/img")
            element.click()
            # click on amount
            element = driver.find_element(By.XPATH, "/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[2]/div/div[1]/div/span[3]/button[1]/i")
            for j in range(i+1):
                element.click()
            # click buy
            element = driver.find_element(By.XPATH, "/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[2]/div/div[2]/button")
            element.click()
            time.sleep(1)
            # click continue shopping
            element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/button")
            element.click()
            time.sleep(1)
            driver.get("https://10.144.0.1/prestashop/2-strona-glowna")

            element = driver.find_element(By.XPATH, "/html/body/main/section/div/div[2]/section/div[2]/ul/li[2]/div/a")
            element.click()

        # click basket
        driver.get("https://10.144.0.1/prestashop/koszyk?action=show")
        assert "10 sztuk" in driver.page_source
        time.sleep(4)

    def test_delete_1_element_from_basket(self):
        driver = self.driver
        driver.get("https://10.144.0.1/prestashop/2-strona-glowna")
        element = driver.find_element(By.XPATH, "/html/body/main/section/div/div[2]/section/div[2]/ul/li[1]/div/a")
        element.click()

        element = driver.find_element(By.XPATH, "/html/body/main/section/div/div[2]/section/div[2]/ul/li[2]/div/a")
        element.click()
        for i in range(2):
            # click on product
            element = driver.find_element(By.XPATH,
                                          f"/html/body/main/section/div/div[2]/section/section/div[3]/div[1]/div[{i + 1}]/article/div/div[1]/a/img")
            element.click()
            # click buy
            element = driver.find_element(By.XPATH,
                                          "/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[2]/div/div[2]/button")
            element.click()
            time.sleep(1)
            # click continue shopping
            element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/button")
            element.click()
            time.sleep(1)
            driver.get("https://10.144.0.1/prestashop/2-strona-glowna")
            element = driver.find_element(By.XPATH, "/html/body/main/section/div/div[2]/section/div[2]/ul/li[1]/div/a")
            element.click()

            element = driver.find_element(By.XPATH, "/html/body/main/section/div/div[2]/section/div[2]/ul/li[2]/div/a")
            element.click()

        time.sleep(1)
        # click on basket
        driver.get("https://10.144.0.1/prestashop/koszyk?action=show")
        time.sleep(1)
        # assert 2 products
        assert "2 sztuk" in driver.page_source
        time.sleep(1)
        # remove element
        element = driver.find_element(By.XPATH, "/html/body/main/section/div/div/section/div/div[1]/div/div[2]/ul/li/div/div[3]/div/div[3]/div/a/i")
        element.click()
        time.sleep(1)
        # assert 1 product

        assert "1 produkt" in driver.page_source


    def test_setup_new_account(self):
        driver = self.driver
        driver.get("https://10.144.0.1/prestashop/logowanie?create_account=1")


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

        element = driver.find_element(By.XPATH, "/html/body/main/section/div/div/section/div/section/form/footer/button")
        element.click()

        delay = 60
        try:
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/header/nav/div/div/div[1]/div[2]/div[1]/div/a[2]/span')))
        except TimeoutException:
            print(
            "Loading took too much time!")
        assert "Jan Kowalski" in driver.page_source


    def test_payment_at_delivery(self):
        driver = self.driver
        driver.get("https://10.144.0.1/prestashop/2-strona-glowna")
        element = driver.find_element(By.XPATH, "/html/body/main/section/div/div[2]/section/div[2]/ul/li[1]/div/a")
        element.click()

        element = driver.find_element(By.XPATH, "/html/body/main/section/div/div[2]/section/div[2]/ul/li[2]/div/a")
        element.click()

        # click on product
        element = driver.find_element(By.XPATH, f"/html/body/main/section/div/div[2]/section/section/div[3]/div[1]/div[1]/article/div/div[1]/a/img")
        element.click()
        # click buy
        element = driver.find_element(By.XPATH, "/html/body/main/section/div/div/section/div[1]/div[2]/div[2]/div[2]/form/div[2]/div/div[2]/button")
        element.click()
        time.sleep(1)
        # click continue shopping
        element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/a")
        element.click()
        # order
        element = driver.find_element(By.XPATH, "/html/body/main/section/div/div/section/div/div[2]/div[1]/div[2]/div/a")
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

        element = driver.find_element("name", "customer_privacy")
        element.click()

        element = driver.find_element("name", "psgdpr")
        element.click()

        # next

        element = driver.find_element(By.XPATH, "/html/body/main/section/div/div/section/div/div[1]/section[1]/div/div[2]/div[1]/form/footer/button")
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
        element = driver.find_element(By.XPATH, "/html/body/main/section/div/div/section/div/div[1]/section[2]/div/div/form/div/div/footer/button")
        element.click()

        # order method
        element = driver.find_element(By.XPATH, "/html/body/main/section/div/div/section/div/div[1]/section[3]/div/div[2]/form/div/div[1]/div[4]/div/span")
        element.click()
        time.sleep(3)

        # next
        element = driver.find_element(By.XPATH, "/html/body/main/section/div/div/section/div/div[1]/section[3]/div/div[2]/form/button")
        element.click()

        # pay at delivery
        element = driver.find_element(By.XPATH, "/html/body/main/section/div/div/section/div/div[1]/section[4]/div/div[2]/div[4]/div/span")
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

        time.sleep(2)
        assert "Twoje zamówienie zostało potwierdzone" in driver.page_source
        time.sleep(5)


    def test_order_status(self):
        driver = self.driver
        driver.get("https://10.144.0.1/prestashop/logowanie?back=my-account")

        element = driver.find_element("name", "email")
        element.send_keys("switala.alb@gmail.com")

        element = driver.find_element("name", "password")
        element.send_keys("Password")

        element = driver.find_element("id", "submit-login")
        element.click()

        time.sleep(1)

        driver.get("https://10.144.0.1/prestashop/historia-zamowien")

        assert "Oczekiwanie na płatność przelewem" in driver.page_source

        time.sleep(1)

    def tearDown(self):
        self.driver.close()


# execute the script
if __name__ == "__main__":
    unittest.main()
