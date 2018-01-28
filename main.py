# -*- coding: utf-8 -*-
import os
import sys
import unittest

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from src.crawlers import linkedin_crawl


def main():
    # the_crawl = linkedin_crawl.LinkedInCrawl()
    # the_crawl.do_some_thing()
    # linkedin_crawl.start_crawling("fanyangxi@live.cn", "xxxxxx")
    pass


def executing_the_tests():
    unittests_dir = 'src/crawlers/'
    suite = unittest.TestSuite()
    unittest_module_names = [filename.replace(".py", "") for filename in os.listdir(unittests_dir)
                             if (filename.startswith("") and filename.endswith("_crawler.py"))]

    for module_name in unittest_module_names:
        module_full_name = '{0}{1}'.format(unittests_dir.replace("/", "."), module_name)
        module = __import__(module_full_name, fromlist=[module_name])
        suite.addTest(unittest.TestLoader().loadTestsFromModule(sys.modules[module_full_name]))
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    executing_the_tests()
    pass
