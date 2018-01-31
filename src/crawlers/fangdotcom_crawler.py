# -*- coding: utf-8 -*-

import json
import re
import time
import unittest
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
from selenium.webdriver import ActionChains, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class FangDotcomCrawlerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # cls.driver = webdriver.PhantomJS("/usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        cls.driver = webdriver.Chrome(chrome_options=options)
        # self.addCleanup(self.browser.quit)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        # pass

    def setUp(self):
        self.target_name = "紫薇臻品"
        self.HOUSE_LIST_ITEMS_CSS_LOCATOR = "div.houseList > dl.list.rel"
        self.HOUSE_ITEM_LINK_CSS_LOCATOR = "dd > p.title > a"
        self.NEXT_PAGE_ELEMENT_CSS_LOCATOR = "#PageControl1_hlk_next"
        pass

    def tearDown(self):
        pass

    def test_go_to_home_page_and_search_for_blahblahblah(self):
        # noinspection SpellCheckingInspection
        result_url = "http://esf.xian.fang.com/house-a0482/g23-j280-k2140-l3010/" #高新+面积80/140+三室
        self.driver.get(result_url)
        self.__close_meng_ceng()

        file = open("fangdotcom-data-{0}.csv".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")),"w")
        file.write(u'\ufeff')

        condition = True
        pageIndex = 1
        while condition:

            pageItemCount = 0            
            # Find element :house-list-item
            house_list_items = self.driver.find_elements_by_css_selector(self.HOUSE_LIST_ITEMS_CSS_LOCATOR)

            for house_list_item in house_list_items[:3]: #house_list_items[:3]

                pageItemCount += 1
                # move to element
                ActionChains(self.driver).move_to_element(house_list_item).perform()

                # Find element : house-details-link
                element = house_list_item.find_element_by_css_selector(self.HOUSE_ITEM_LINK_CSS_LOCATOR)
                subPageUrl = element.get_attribute("href")
                
                response = requests.get(subPageUrl)
                soup = BeautifulSoup(response.text,'html.parser')
                houseInfoJson = self.__parse_house_info(soup, subPageUrl)
                theValues = []
                for attribute, value in houseInfoJson.items():
                    theValues.append(value)

                houseInfoStr = json.dumps(houseInfoJson)
                theResult = ",".join(theValues)
                print(theResult)
                print("{0}:{1} {2}".format(pageIndex, pageItemCount, subPageUrl))
                
                file.write(theResult)
                file.write("\r\n")

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


    def test_some_stuff(self):
        pass

    def __close_meng_ceng(self):
        try:
            meng_ceng_element = self.driver.find_element_by_css_selector("#closemengceng")
            if meng_ceng_element:
                ActionChains(self.driver).move_to_element(meng_ceng_element).perform()
                time.sleep(0.9)
                ActionChains(self.driver).click(meng_ceng_element).perform()
        except Exception as e:
            pass

    def __parse_house_info(self, soup, currentUrl):

        title_css_selector = ["div.title.rel > div.floatl"]
        fa_bu_shi_jian_css_selector = ["div.content-item.fydes-item > div.cont.clearfix > div:nth-of-type(7) > span.rcont"]
        fang_wu_zong_jia_css_selector = ["div.tab-cont-right > div.tr-line.clearfix.zf_new_title > div.trl-item_top > div.trl-item.price_esf.sty1"]

        suo_shu_xiao_qu_css_selector = ["div.tab-cont-right > div:nth-of-type(4) > div:nth-of-type(1) > div.rcont > a.blue"]
        suo_zai_wei_zhi_css_selector = ["div.tab-cont-right > div:nth-of-type(4) > div:nth-of-type(1) > div.rcont > span"]
        jian_zao_nian_dai_css_selector = ["div.content-item.fydes-item > div.cont.clearfix > div:nth-of-type(1) > span.rcont"]
        fang_wu_lei_xing_css_selector = ["div.content-item.fydes-item > div.cont.clearfix > div:nth-of-type(4) > span.rcont"]

        fang_wu_hu_xing_css_selector = ["div.tab-cont-right > div:nth-of-type(2) > div.trl-item1.w146 > div.tt"]
        jian_zhu_mian_ji_css_selector = ["div.tab-cont-right > div:nth-of-type(2) > div.trl-item1.w182 > div.tt"]
        fang_wu_chao_xiang_css_selector = ["div.tab-cont-right > div:nth-of-type(3) > div.trl-item1.w146 > div.tt"]
        suo_zai_lou_ceng_css_selector = ["div.tab-cont-right > div:nth-of-type(3) > div.trl-item1.w182"]

        zhuang_xiu_cheng_du_css_selector = ["div.tab-cont-right > div:nth-of-type(3) > div.trl-item1.w132 > div.tt"]
        fang_wu_dan_jia_css_selector = ["div.tab-cont-right > div:nth-of-type(2) > div.trl-item1.w132 > div.tt"]
        can_kao_shou_fu_css_selector = ["div.tab-cont-right > div.tr-line.clearfix.zf_new_title > div.trl-item_top > div:nth-of-type(2)"]
        can_kao_yue_gong_css_selector = ["div.tab-cont-right > div.tr-line.clearfix.zf_new_title > div.trl-item_top > div:nth-of-type(3) > a > div > span"]

        houseInfo = {
            "Title": self.__get_inner_text_by_css_selectors(soup, title_css_selector),
            "fa_bu_shi_jian": self.__get_inner_text_by_css_selectors(soup, fa_bu_shi_jian_css_selector),
            "fang_wu_zong_jia": self.__get_inner_text_by_css_selectors(soup, fang_wu_zong_jia_css_selector), #房屋总价
            "suo_shu_xiao_qu": self.__get_inner_text_by_css_selectors(soup, suo_shu_xiao_qu_css_selector), #所属小区, innerHTML
            "suo_zai_wei_zhi": self.__get_inner_text_by_css_selectors(soup, suo_zai_wei_zhi_css_selector), #所在位置
            "jian_zao_nian_dai": self.__get_inner_text_by_css_selectors(soup, jian_zao_nian_dai_css_selector), #建造年代
            "fang_wu_lei_xing": self.__get_inner_text_by_css_selectors(soup, fang_wu_lei_xing_css_selector), #房屋类型
            "fang_wu_hu_xing": self.__get_inner_text_by_css_selectors(soup, fang_wu_hu_xing_css_selector), #房屋户型
            "jian_zhu_mian_ji": self.__get_inner_text_by_css_selectors(soup, jian_zhu_mian_ji_css_selector), #建筑面积
            "fang_wu_chao_xiang": self.__get_inner_text_by_css_selectors(soup, fang_wu_chao_xiang_css_selector), #房屋朝向
            "suo_zai_lou_ceng": self.__get_inner_text_by_css_selectors(soup, suo_zai_lou_ceng_css_selector), #所在楼层
            "zhuang_xiu_cheng_du": self.__get_inner_text_by_css_selectors(soup, zhuang_xiu_cheng_du_css_selector), #装修程度
            "fang_wu_dan_jia": self.__get_inner_text_by_css_selectors(soup, fang_wu_dan_jia_css_selector), #房屋单价
            "can_kao_shou_fu": self.__get_inner_text_by_css_selectors(soup, can_kao_shou_fu_css_selector), #参考首付
            "can_kao_yue_gong": self.__get_inner_text_by_css_selectors(soup, can_kao_yue_gong_css_selector), #参考月供
            "URL": currentUrl
        }
        return houseInfo

    def __strip_text(self, inputText):
        return re.sub(r"[\\n\\t\s,]*", "", inputText)

    def __get_inner_text_by_css_selectors(self, soup, cssSelectors):
        for cssSelector in cssSelectors:
            try:
                result = soup.select_one(cssSelector).text
                return re.sub(r"[\\n\\t\s,]*", "", result)
            except Exception as e:
                pass
        return ""

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

