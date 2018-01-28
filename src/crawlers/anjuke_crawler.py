# -*- coding: utf-8 -*-

import unittest
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains, ChromeOptions
from selenium.webdriver.common.keys import Keys


class AnjukeCrawlerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # cls.driver = webdriver.PhantomJS("/usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs")
        cls.driver = webdriver.Chrome(
                "/usr/local/Cellar/chromedriver/2.19/bin/chromedriver",
                chrome_options=ChromeOptions()
        )
        # self.addCleanup(self.browser.quit)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        # pass

    def setUp(self):
        self.target_name = "紫薇臻品"
        pass

    def tearDown(self):
        pass

    def test_go_to_home_page_and_search_for_blahblahblah(self):
        # noinspection SpellCheckingInspection
        result_url = "http://xa.anjuke.com/sale/rd1?from=zjsr&kw={0}".format(self.target_name)
        self.driver.get(result_url)

        # Find element :house-list-item
        house_list_items = self.driver.find_elements_by_css_selector("#houselist-mod > li")

        for house_list_item in house_list_items:

            # move to element
            ActionChains(self.driver).move_to_element(house_list_item)

            # Find element : house-details-link
            element = house_list_item.find_element_by_css_selector("div.house-details > div.house-title > a")
            # Open the new tab
            ActionChains(self.driver).key_down(Keys.COMMAND).click(element).key_up(Keys.COMMAND).perform()
            # element.send_keys(Keys.COMMAND, Keys.ENTER)
            # Switch to new tab
            # self.driver.switch_to.window(self.driver.window_handles[-1])
            # ActionChains(self.driver).key_down(Keys.COMMAND).send_keys("2").key_up(Keys.COMMAND).perform()
            # self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND, "t")

            # self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
            # self.driver.switch_to.window(window_name=self.driver.current_window_handle)

            # 1.Current
            print(self.driver.current_url)

            # 2.Switch to next-to right tab
            self.driver.switch_to.window(self.driver.window_handles[1])
            print(self.driver.current_url)

            # 3.Close the next-to right tab and switch back to the original tab
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            print(self.driver.current_url)

            import time
            time.sleep(0.5)

        # Close this new tab
        # action.key_down(Keys.COMMAND).key_down('W').key_up('W').key_up(Keys.COMMAND).perform()
        # self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')

        # print(element.get_attribute('title'))

        # for section in sections:
        #     element = section.find_element_by_css_selector("div.house-details > div.house-title > a")
        #
        #     # Open the new tab
        #     action = ActionChains(self.driver)
        #     action.key_down(Keys.COMMAND).click(element).key_up(Keys.COMMAND).perform()
        #
        #     # Switch to new tab
        #     action.key_down(Keys.COMMAND).key_down(Keys.NUMPAD2).key_up(Keys.NUMPAD2).key_up(Keys.COMMAND).perform()
        #
        #     # Close this new tab
        #     action.key_down(Keys.COMMAND).key_down('W').key_up('W').key_up(Keys.COMMAND).perform()
        #
        #     print(element.get_attribute('title'))

    def test_some_stuff(self):
        pass
