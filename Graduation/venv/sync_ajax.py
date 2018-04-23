from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

def ajax_complete(dv):
    try:
        return 0 == dv.execute_script("return jQuery.active")
    except WebDriverException:
        pass