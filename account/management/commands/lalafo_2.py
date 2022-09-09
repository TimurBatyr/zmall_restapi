from datetime import time

from selenium  import webdriver

url = " https://www.vk.com"
driver = webdriver.Firefox(executable_path = "/home/oskon/Документы/lab_driver/geckodriver")
try :
    driver.get (url = url )
    driver.save_screenshot ("vk.png")
    time.sleep(5)

except Exception as ex :
   print(ex)