# encoding: utf-8
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as GCOptions
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from robot.api.deco import keyword
import logging


class CKWeb(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 0.1

    def __init__(self):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)
        logger = logging.getLogger(__name__)

    @keyword('Browser Open')
    def browseropen(self, browserType='chrome', headless='off'):
        """ 
        browserType
            |    = Browser =    |        = Name(s) =       |
            | Firefox           | firefox, ff              |
            | Google Chrome     | googlechrome, chrome, gc |

        headless
            |    = Options =    |
            | off               |
            | on                |

        Examples:
            | `Browser Open` | chrome  |         |
            | `Browser Open` | chrome  | on      |
            | `Browser Open` | chrome  | off     |
        """
        global driver
        global actions
        if (browserType == 'chrome' or 'gc' or 'googlechrome'):
            driver_path = os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + "/driver/chromedriver.exe"
            options = GCOptions()
            if (headless=='on'):
                options.headless = True
            driver = webdriver.Chrome(executable_path=driver_path, options=options)
        elif(browserType == 'firefox' or 'ff'):
            driver_path = os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + "/driver/geckodriver.exe"
            options = FFOptions()
            if (headless=='on'):
                options.headless = True
            driver = webdriver.Firefox(executable_path=driver_path, options=options)
        driver.implicitly_wait(15)
        actions = ActionChains(driver)

    @keyword('Browser Maximize Window')
    def browsermaximizewindow(self):
        driver.maximize_window()

    @keyword('Browser Goto')
    def browsergoto(self, url):
        """ 
        Examples:
            | Browser Goto     | https://www.google.com/  |
        """
        driver.get(url)

    @keyword('Browser Input')
    def browserinput(self, xPath, text):
        """ 
        Examples:
            | Browser Input     | //*[@name='q']  |  test     |
        """
        input_text = driver.find_element(By.XPATH, xPath)
        driver.execute_script("arguments[0].focus();", input_text)
        input_text.clear()
        input_text.send_keys(text)

    @keyword('Browser Click')
    def browserclick(self, xPath):
        """ 
        Examples:
            | Browser Click     | //*[@name='q']  |
        """
        click_element = driver.find_element(By.XPATH, xPath)
        driver.execute_script("arguments[0].focus();", click_element)
        click_element.click()

    @keyword('Browser Get')
    def browserget(self, xPath):
        """ 
        Examples:
            | ${value}   | Browser Get     | //*[@name='q']  |
        """
        get_element = driver.find_element(By.XPATH, xPath)
        driver.execute_script("arguments[0].focus();", get_element)
        get = get_element.text
        return get

    @keyword('Browser Select Frame')
    def browseriframe(self, xPath):
        """ 
        Examples:
            | Browser Select Frame     | //*[@name='q']  |
        """
        browseriframe = driver.find_element(By.XPATH, xPath)
        driver.execute_script("arguments[0].focus();", browseriframe)
        driver.switchTo.frame(browseriframe)

    @keyword('Browser Unselect Frame')
    def browseruniframe():
        """ 
        Examples:
            | Browser Unselect Frame     |
        """
        uniframe = driver.switchTo.default_content()
        driver.execute_script("arguments[0].focus();", uniframe)
        actions.move_to_element(uniframe).perform()

    @keyword('Browser Select Value')
    def selectValue(self, xPath, value):
        """ 
        Examples:
            | Browser Select Value     | //*[@name='q']  |  test     |
        """
        selectValue = driver.find_element(By.XPATH, xPath)
        driver.execute_script("arguments[0].focus();", selectValue)
        dropdown = Select(selectValue)
        dropdown.select_by_value(value);

    @keyword('Browser Select Index')
    def selectIndex(self, xPath, index):
        """ 
        Examples:
            | Browser Select Index     | //*[@name='q']  |  test     |
        """
        selectIndex = driver.find_element(By.XPATH, xPath)
        driver.execute_script("arguments[0].focus();", selectIndex)
        dropdown = Select(selectIndex)
        dropdown.select_by_index(index);

    @keyword('Browser Select Text')
    def selectText(self, xPath, text):
        """ 
        Examples:
            | Browser Select Text     | //*[@name='q']  |  test     |
        """
        selectText = driver.find_element(By.XPATH, xPath)
        driver.execute_script("arguments[0].focus();", selectText)
        dropdown = Select(selectText)
        dropdown.select_by_visible_text(text);

    @keyword('Browser Close')
    def close(self):
        """ 
        Examples:
            | Browser Close     |
        """
        driver.quit()
        debuglog('close')

