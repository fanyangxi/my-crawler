# -*- coding: utf-8 -*-

import json
import re
import time
import unittest
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
from selenium.webdriver import ActionChains, ChromeOptions
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class AnjukeCrawlerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # cls.driver = webdriver.PhantomJS("/usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        cls.driver = webdriver.Chrome(chrome_options=options)
        # self.addCleanup(self.browser.quit)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        # pass

    def setUp(self):
        self.target_name = "紫薇臻品"
        self.HOUSE_LIST_ITEMS_CSS_LOCATOR = "#houselist-mod-new > li"
        self.HOUSE_ITEM_LINK_CSS_LOCATOR = "div.house-details > div.house-title > a"
        self.NEXT_PAGE_ELEMENT_CSS_LOCATOR = "a.aNxt"
        pass

    def tearDown(self):
        pass

    def test_go_to_home_page_and_search_for_blahblahblah(self):
        # noinspection SpellCheckingInspection
        # result_url = "https://xa.anjuke.com/sale/rd1?from=zjsr&kw={0}".format(self.target_name)
        # result_url = "https://xa.anjuke.com/sale/gaoxinquxian/?from_area=80&to_area=140" #高新+面积80/140
        result_url = "https://xa.anjuke.com/sale/gaoxinquxian/b206/?from_area=80&to_area=140" #高新+面积80/140+三室
        self.driver.get(result_url)

        file = open("anjuke-testfile-{0}.csv".format(datetime.now().isoformat(timespec='minutes')),"w")
        file.write(u'\ufeff')

        condition = True
        pageIndex = 1
        while condition:

            pageItemCount = 0
            # Find element :house-list-item
            house_list_items = self.driver.find_elements_by_css_selector(self.HOUSE_LIST_ITEMS_CSS_LOCATOR)

            for house_list_item in house_list_items: #house_list_items[:3]

                pageItemCount += 1
                # move to element
                ActionChains(self.driver).move_to_element(house_list_item).perform()

                # Find element : house-details-link
                element = house_list_item.find_element_by_css_selector(self.HOUSE_ITEM_LINK_CSS_LOCATOR)
                # Open the new tab
                ActionChains(self.driver).key_down(Keys.COMMAND).click(element).key_up(Keys.COMMAND).perform()
                # element.send_keys(Keys.COMMAND, Keys.ENTER)
                # Switch to new tab
                # self.driver.switch_to.window(self.driver.window_handles[-1])
                # ActionChains(self.driver).key_down(Keys.COMMAND).send_keys("2").key_up(Keys.COMMAND).perform()
                # self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND, "t")

                # self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
                # self.driver.switch_to.window(window_name=self.driver.current_window_handle)

                # 1.Parent-Tab::Current
                print(self.driver.current_url)

                # 2.Sub-Tab::Switch to next-to right tab
                time.sleep(0.2)
                self.driver.switch_to.window(self.driver.window_handles[1])
                print("{0}:{1} {2}".format(pageIndex, pageItemCount, self.driver.current_url))
                houseInfoJson = self.__parse_house_info(self.driver)
                theValues = []
                for attribute, value in houseInfoJson.items():
                    # print value
                    theValues.append(value)

                houseInfoStr = json.dumps(houseInfoJson)
                theResult = ",".join(theValues)
                print(theResult)
                file.write(theResult)
                file.write("\r\n")

                # 3.Parent-Tab::Close the next-to right tab and switch back to the original tab
                self.driver.close()

                time.sleep(0.2)
                self.driver.switch_to.window(self.driver.window_handles[0])
                print(self.driver.current_url)

                # time.sleep(0.5)
                print("========================")

            pageIndex += 1
            # is there a next page?
            try:
                next_page_element = self.driver.find_element_by_css_selector(self.NEXT_PAGE_ELEMENT_CSS_LOCATOR)
                if next_page_element:
                    print("### GO to next page:")
                    ActionChains(self.driver).move_to_element(next_page_element).perform()
                    time.sleep(0.9)
                    ActionChains(self.driver).click(next_page_element).perform()
                    print(self.driver.current_url)
            except Exception as e:
                condition = False
                print(e)
                print("### 'Next-Page button is not available', so this's the last page:")

            # input("Press Enter to continue ...")

        file.close()


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

    def __parse_house_info(self, webDriver):
        title_css_selector = "h3.long-title"
        house_encode_css_selector = ["div.houseInfoBox > h4 > span.house-encode"]
        fang_wu_zong_jia_css_selector = ["div.basic-info.clearfix > span.light.info-tag"]

        suo_shu_xiao_qu_css_selector = ["div.houseInfoV2-detail > div.first-col.detail-col > dl:nth-child(1) > dd", 
            "div.houseInfo-detail > div.first-col.detail-col > dl:nth-child(1) > dd"]
        suo_zai_wei_zhi_css_selector = ["div.houseInfoV2-detail > div.first-col.detail-col > dl:nth-child(2) > dd",
            "div.houseInfo-detail > div.first-col.detail-col > dl:nth-child(2) > dd"]
        jian_zao_nian_dai_css_selector = ["div.houseInfoV2-detail > div.first-col.detail-col > dl:nth-child(3) > dd",
            "div.houseInfo-detail > div.first-col.detail-col > dl:nth-child(3) > dd"]
        fang_wu_lei_xing_css_selector = ["div.houseInfoV2-detail > div.first-col.detail-col > dl:nth-child(4) > dd",
            "div.houseInfo-detail > div.first-col.detail-col > dl:nth-child(4) > dd"]

        fang_wu_hu_xing_css_selector = ["div.houseInfoV2-detail > div.second-col.detail-col > dl:nth-child(1) > dd",
            "div.houseInfo-detail > div.second-col.detail-col > dl:nth-child(1) > dd"]
        jian_zhu_mian_ji_css_selector = ["div.houseInfoV2-detail > div.second-col.detail-col > dl:nth-child(2) > dd",
            "div.houseInfo-detail > div.second-col.detail-col > dl:nth-child(2) > dd"]
        fang_wu_chao_xiang_css_selector = ["div.houseInfoV2-detail > div.second-col.detail-col > dl:nth-child(3) > dd",
            "div.houseInfo-detail > div.second-col.detail-col > dl:nth-child(3) > dd"]
        suo_zai_lou_ceng_css_selector = ["div.houseInfoV2-detail > div.second-col.detail-col > dl:nth-child(4) > dd",
            "div.houseInfo-detail > div.second-col.detail-col > dl:nth-child(4) > dd"]

        zhuang_xiu_cheng_du_css_selector = ["div.houseInfoV2-detail > div.third-col.detail-col > dl:nth-child(1) > dd",
            "div.houseInfo-detail > div.third-col.detail-col > dl:nth-child(1) > dd"]
        fang_wu_dan_jia_css_selector = ["div.houseInfoV2-detail > div.third-col.detail-col > dl:nth-child(2) > dd",
            "div.houseInfo-detail > div.third-col.detail-col > dl:nth-child(2) > dd"]
        can_kao_shou_fu_css_selector = ["div.houseInfoV2-detail > div.third-col.detail-col > dl:nth-child(3) > dd",
            "div.houseInfo-detail > div.third-col.detail-col > dl:nth-child(3) > dd"]
        can_kao_yue_gong_css_selector = ["div.houseInfoV2-detail > div.third-col.detail-col > dl:nth-child(4) > dd",
            "div.houseInfo-detail > div.third-col.detail-col > dl:nth-child(4) > dd"]

        fang_wu_bian_ma = ""
        fa_bu_shi_jian = ""
        try:
            match = re.findall(r"\W*(\d*)\W*(.*)$", self.__get_html_element_inner_text_by_multi_selectors(house_encode_css_selector)) #房屋编码\W*(\d*)，发布时间\W*(.*)$
            fang_wu_bian_ma = match[0][0]
            fa_bu_shi_jian = match[0][1]
        except Exception as e:
            fa_bu_shi_jian = self.__get_html_element_inner_text_by_multi_selectors(house_encode_css_selector)
            print(fa_bu_shi_jian)
            print(e)

        houseInfo = {
            "Title": self.__strip_text(webDriver.title),
            "fang_wu_bian_ma": fang_wu_bian_ma,
            "fa_bu_shi_jian": fa_bu_shi_jian,
            "fang_wu_zong_jia": self.__get_html_element_inner_text_by_multi_selectors(fang_wu_zong_jia_css_selector), #房屋总价
            "suo_shu_xiao_qu": self.__get_html_element_inner_text_by_multi_selectors(suo_shu_xiao_qu_css_selector), #所属小区, innerHTML
            "suo_zai_wei_zhi": self.__get_html_element_inner_text_by_multi_selectors(suo_zai_wei_zhi_css_selector), #所在位置
            "jian_zao_nian_dai": self.__get_html_element_inner_text_by_multi_selectors(jian_zao_nian_dai_css_selector), #建造年代
            "fang_wu_lei_xing": self.__get_html_element_inner_text_by_multi_selectors(fang_wu_lei_xing_css_selector), #房屋类型
            "fang_wu_hu_xing": self.__get_html_element_inner_text_by_multi_selectors(fang_wu_hu_xing_css_selector), #房屋户型
            "jian_zhu_mian_ji": self.__get_html_element_inner_text_by_multi_selectors(jian_zhu_mian_ji_css_selector), #建筑面积
            "fang_wu_chao_xiang": self.__get_html_element_inner_text_by_multi_selectors(fang_wu_chao_xiang_css_selector), #房屋朝向
            "suo_zai_lou_ceng": self.__get_html_element_inner_text_by_multi_selectors(suo_zai_lou_ceng_css_selector), #所在楼层
            "zhuang_xiu_cheng_du": self.__get_html_element_inner_text_by_multi_selectors(zhuang_xiu_cheng_du_css_selector), #装修程度
            "fang_wu_dan_jia": self.__get_html_element_inner_text_by_multi_selectors(fang_wu_dan_jia_css_selector), #房屋单价
            "can_kao_shou_fu": self.__get_html_element_inner_text_by_multi_selectors(can_kao_shou_fu_css_selector), #参考首付
            "can_kao_yue_gong": self.__get_html_element_inner_text_by_multi_selectors(can_kao_yue_gong_css_selector), #参考月供
            "URL": webDriver.current_url
        }
        return houseInfo

    def __strip_text(self, inputText):
        return re.sub(r"[\\n\\t\s,]*", "", inputText)

    def __get_html_element_inner_text_by_multi_selectors(self, cssSelectors):
        for cssSelector in cssSelectors:
            # try:
            #     element_present = EC.presence_of_element_located((By.CSS_SELECTOR, cssSelector))
            #     WebDriverWait(self.driver, 3).until(element_present)
            # except TimeoutException:
            #     print ("Timed out waiting for element to load")
            try:
                text = self.__strip_text(self.driver.find_element_by_css_selector(cssSelector).get_attribute('innerText'))
                return re.sub(r"[\\n\\t\s,]*", "", text)
            except Exception as e:
                pass
        return ""

