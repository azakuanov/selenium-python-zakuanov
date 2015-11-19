# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys  import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Untitled(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "localhost/php4dvd"
        self.verificationErrors = []
        self.accept_next_alert = True

    # Log In
    def test_login(self):
        driver = self.driver
        driver.get(self.base_url)

        self.log_in(driver)
        self.create_a_movie_with_positive_inputs(driver)
        self.delete_movie(driver)
        self.create_blank_year(driver) # try to create movie with blank year field

    def create_blank_year(self, driver):
        driver.find_element_by_css_selector("img[alt=\"Add movie\"]").click()
        driver.find_element_by_id("imdbsearch").clear()
        driver.find_element_by_id("imdbsearch").send_keys("qwerty")
        driver.find_element_by_name("name").clear()
        driver.find_element_by_name("name").send_keys("qwrety")
        driver.find_element_by_name("aka").clear()
        driver.find_element_by_name("aka").send_keys("qwerty")
        driver.find_element_by_id("submit").click()
        # ERROR: Caught exception [ERROR: Unsupported command [getTable | css=#updateform > table.3.1 | ]]

    def delete_movie(self, driver):
        driver.get(self.base_url)
        driver.find_elements_by_css_selector("div.nocover")[4].click()
        driver.find_element_by_css_selector("img[alt=\"Remove\"]").click()
        self.assertRegexpMatches(self.close_alert_and_get_its_text(), r"^Are you sure you want to remove this[\s\S]$")

    def create_a_movie_with_positive_inputs(self, driver):
        driver.find_element_by_css_selector("img[alt=\"Add movie\"]").click()
        driver.find_element_by_name("name").clear()
        driver.find_element_by_name("name").send_keys('Final Test3')
        driver.find_element_by_name("aka").clear()
        driver.find_element_by_name("aka").send_keys("testrrgregregregregregfdgfdv dfgfdgregerv rgreg")
        driver.find_element_by_name("aka").send_keys(Keys.CONTROL, "a")
        time.sleep(1)
        driver.find_element_by_name("aka").send_keys(Keys.DELETE)
        driver.find_element_by_name("aka").send_keys("privet")
        driver.find_element_by_name("year").clear()
        driver.find_element_by_name("year").send_keys("1992")
        driver.find_element_by_name("duration").clear()
        driver.find_element_by_name("duration").send_keys("180")
        driver.find_element_by_name("rating").clear()
        driver.find_element_by_name("rating").send_keys("7")
        driver.find_element_by_id("submit").click()

    def log_in(self, driver):
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("admin")
        driver.find_element_by_name("submit").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
