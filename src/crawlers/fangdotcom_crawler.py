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
        # target_url = "http://esf.xian.fang.com/house-a0482/g23-j280-k2140-l3010/" #高新+面积80/140+三室
        self.target_urls = [
            "http://esf.xian.fang.com/integrate/g23-kw%cc%ec%b5%d8%d4%b4%b7%e3%c1%d6%c2%cc%d6%de/", #天地源枫林绿洲
            "http://esf.xian.fang.com/integrate/g23-kw%d7%cf%de%b1%cc%ef%d4%b0%b6%bc%ca%d0/", #紫薇田园都市
            "http://esf.xian.fang.com/integrate/g23-kw%c2%cc%b5%d8%ca%c0%bc%cd%b3%c7/", #绿地世纪城
            "http://esf.xian.fang.com/integrate/g23-kw%d6%d0%bb%aa%ca%c0%bc%cd%b3%c7/", #中华世纪城
            "http://esf.xian.fang.com/integrate/g23-kw%bd%f0%cc%a9%bc%d9%c8%d5%bb%a8%b3%c7/", #金泰假日花城
            "http://esf.xian.fang.com/integrate/g23-kw%d2%dd%b4%e4%d4%b0/", #逸翠园
            "http://esf.xian.fang.com/integrate/g23-kw%c1%d6%d2%fe%cc%ec%cf%c2/", #林隐天下
            "http://esf.xian.fang.com/integrate/g23-kw%b7%e3%c1%d6%d2%e2%ca%f7/", #枫林意树
            "http://esf.xian.fang.com/integrate/g23-kw%b3%c7%ca%d0%b7%e7%be%b0%cf%c4%c8%d5%be%b0%c9%ab/", #城市风景夏日景色
            "http://esf.xian.fang.com/integrate/g23-kw%b7%e3%d2%b6%d0%c2%b6%bc%ca%d0/", #枫叶新都市
            "http://esf.xian.fang.com/integrate/g23-kw%e7%cd%b7%d7%c4%cf%bf%a4/", #缤纷南郡
            "http://esf.xian.fang.com/integrate/g23-kw%d7%cf%de%b1%d5%e9%c6%b7/", #紫薇臻品
            "http://esf.xian.fang.com/integrate/g23-kw%b3%c7%ca%d0%b7%e7%be%b0%b6%bc%ca%d0%d3%a1%cf%f3/", #城市风景都市印象
            "http://esf.xian.fang.com/integrate/g23-kw%cc%ec%c0%ca%c0%b6%ba%fe%ca%f7/", #天朗蓝湖树
            "http://esf.xian.fang.com/integrate/g23-kw%ba%e3%b4%f3%b3%c7/", #恒大城
            "http://esf.xian.fang.com/integrate/g23-kw%d2%d7%b5%c0%bf%a4%2b%c3%b5%b9%e5%b9%ab%b9%dd/", #易道郡+玫瑰公馆
            "http://esf.xian.fang.com/integrate/g23-kw%b8%df%bf%c6%c9%d0%b6%bc/", #高科尚都
            "http://esf.xian.fang.com/integrate/g23-kw%cd%fb%cd%a5%b9%fa%bc%ca/", #望庭国际
            "http://esf.xian.fang.com/integrate/g23-kw%b8%df%bf%c6%c0%ca%c9%bd/", #高科朗山
            "http://esf.xian.fang.com/integrate/g23-kw%bd%f5%b6%bc%bb%a8%d4%b0/", #锦都花园
            "http://esf.xian.fang.com/house/c61-c7125302-kw%c1%d6%d2%fe%cc%ec%cf%c2/", #林隐天下
            "http://esf.xian.fang.com/integrate/g23-kw%c9%d0%c6%b7%bb%a8%b6%bc/", #尚品花都
            "http://esf.xian.fang.com/house/g23-kw%c8%da%b4%b4%cc%ec%c0%ca%e7%e7%b8%ae/", #融创天朗珑府
            "http://esf.xian.fang.com/integrate/g23-kw%bd%f0%cc%a9%d0%c2%c0%ed%b3%c7/", #金泰新理城
            "http://esf.xian.fang.com/integrate/g23-kw%b6%ab%b7%bd%c3%d7%c0%bc%b9%fa%bc%ca%b3%c7/", #东方米兰国际城
        ]

    def tearDown(self):
        pass

    def test_go_to_home_page_and_search_for_blahblahblah(self):
        file = open("fangdotcom-data-{0}.csv".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")),"w")
        file.write(u'\ufeff')

        # noinspection SpellCheckingInspection
        for target_url in self.target_urls: #house_list_items[:3]
            self.driver.get(target_url)
            self.__close_meng_ceng()

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
                    subPageUrl = element.get_attribute("href")
                    
                    response = requests.get(subPageUrl)
                    houseInfoJson = self.__parse_house_info(response.text, subPageUrl)
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

        print("closing file....")
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

    def __parse_house_info(self, html, currentUrl):
        soup = BeautifulSoup(html,'html.parser')
        # fang_wu_lei_xing_css_selector = ["div.content-item.fydes-item > div.cont.clearfix > div:nth-of-type(4) > span.rcont"]

        title_css_selector = ["div.title.rel > div.floatl", "div.title.rel"]
        fa_bu_shi_jian_regex_selector = ["<span.*>挂牌时间<\/span>\s*<span.*>(.*)<\/span>"]
        fang_yuan_bian_hao_regex_selector = ["<span.*>房源编号<\/span>\s*<span.*>(.*)<\/span>"]

        fang_wu_zong_jia_css_selector = ["div.tab-cont-right > div.tr-line.clearfix.zf_new_title > div.trl-item_top > div.trl-item.price_esf.sty1"]
        suo_shu_xiao_qu_css_selector = ["div.tab-cont-right > div:nth-of-type(4) > div:nth-of-type(1) > div.rcont > div.floatl > a"]
        suo_zai_wei_zhi_css_selector = ["div.tab-cont-right > div:nth-of-type(4) > div:nth-of-type(1) > div.rcont > div.floatl > span"]
        jian_zao_nian_dai_regex_selector = ["<span.*>建筑年代<\/span>\s*<span.*>(.*)<\/span>"]

        fang_wu_hu_xing_regex_selector = ["<div.*>(.*)<\/div>\s*<div.*>户型<\/div>"] #房屋户型
        jian_zhu_mian_ji_regex_selector = ["<div.*>(.*)<\/div>\s*<div.*>建筑面积<\/div>"] #建筑面积
        fang_wu_chao_xiang_regex_selector = ["<div.*>(.*)<\/div>\s*<div.*>朝向<\/div>"] #房屋朝向
        suo_zai_lou_ceng_regex_selector = ["<div.*>(.*)<\/div>\s*<div.*>楼层.*<\/div>"]
        zhuang_xiu_cheng_du_regex_selector = ["<div.*>(.*)<\/div>\s*<div.*>装修<\/div>"]
        fang_wu_dan_jia_regex_selector = ["<div.*>(.*)<\/div>\s*<div.*>单价<\/div>"]
        can_kao_shou_fu_css_selector = ["div.tab-cont-right > div.tr-line.clearfix.zf_new_title > div.trl-item_top > div:nth-of-type(2)"]
        can_kao_yue_gong_css_selector = ["div.tab-cont-right > div.tr-line.clearfix.zf_new_title > div.trl-item_top > div:nth-of-type(3) > a > div > span"]

        hu_xing_jie_gou_regex_selector = ["<span.*>户型结构<\/span>\s*<span.*>(.*)<\/span>"]

        houseInfo = {
            "Title": self.__get_inner_text_by_css_selectors(soup, title_css_selector),
            "fa_bu_shi_jian": self.__get_inner_text_by_regex_selectors(html, fa_bu_shi_jian_regex_selector),
            "fang_yuan_bian_hao": self.__get_inner_text_by_regex_selectors(html, fang_yuan_bian_hao_regex_selector),
            "fang_wu_zong_jia": self.__get_inner_text_by_css_selectors(soup, fang_wu_zong_jia_css_selector), #房屋总价
            "suo_shu_xiao_qu": self.__get_inner_text_by_css_selectors(soup, suo_shu_xiao_qu_css_selector), #所属小区, innerHTML
            "suo_zai_wei_zhi": self.__get_inner_text_by_css_selectors(soup, suo_zai_wei_zhi_css_selector), #所在位置
            "jian_zao_nian_dai": self.__get_inner_text_by_regex_selectors(html, jian_zao_nian_dai_regex_selector), #建造年代
            "fang_wu_hu_xing": self.__get_inner_text_by_regex_selectors(html, fang_wu_hu_xing_regex_selector), #房屋户型
            "jian_zhu_mian_ji": self.__get_inner_text_by_regex_selectors(html, jian_zhu_mian_ji_regex_selector), #建筑面积
            "fang_wu_chao_xiang": self.__get_inner_text_by_regex_selectors(html, fang_wu_chao_xiang_regex_selector), #房屋朝向
            "suo_zai_lou_ceng": self.__get_inner_text_by_regex_selectors(html, suo_zai_lou_ceng_regex_selector), #所在楼层
            "zhuang_xiu_cheng_du": self.__get_inner_text_by_regex_selectors(html, zhuang_xiu_cheng_du_regex_selector), #装修程度
            "fang_wu_dan_jia": self.__get_inner_text_by_regex_selectors(html, fang_wu_dan_jia_regex_selector), #房屋单价
            "can_kao_shou_fu": self.__get_inner_text_by_css_selectors(soup, can_kao_shou_fu_css_selector), #参考首付
            "can_kao_yue_gong": self.__get_inner_text_by_css_selectors(soup, can_kao_yue_gong_css_selector), #参考月供
            "fang_wu_lei_xing": self.__get_inner_text_by_regex_selectors(html, hu_xing_jie_gou_regex_selector), #户型结构
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

    def __get_inner_text_by_regex_selectors(self, html, regexSelectors):
        for regexSelector in regexSelectors:
            try:
                match = re.search(regexSelector, html)
                if match is not None:
                    result = match.group(1)
                else:
                    result = ""
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

