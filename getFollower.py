from splinter import Browser
import time
with Browser('chrome') as browser:
    browser.visit('http://baidu.com')
    time.sleep(2)
    browser.fill('wd', '熹昀教育')
    time.sleep(2)
    button = browser.find_by_xpath('//input[@type="submit"]')
    button.click()
    if browser.is_text_present('sheenedu'):
        print("Yes, found it! :)")
    else:
        print("No, didn't find it :(")
    time.sleep(2)
    #browser.quit()