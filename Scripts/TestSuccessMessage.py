import os
import shutil
import time
from datetime import datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Utilities.user_context import get_user_ip


class TestSuccessMessage:
    def delete(self):
        screenshot_folder = f"Screenshots/{get_user_ip()}"
        if os.path.exists(screenshot_folder):
            shutil.rmtree(screenshot_folder)
        os.makedirs(screenshot_folder)
    def test_success(self,driver,name, xpath):
        print_log = ""
        screenshot_folder = f"Screenshots/{get_user_ip()}"
        try:
            success_message = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH, xpath))).text
            print(success_message)
            if "failed" in success_message or "Error" in success_message or "Welcome" in success_message:
                screenshot_name = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                screenshot_path = os.path.join(screenshot_folder, screenshot_name)
                driver.save_screenshot(screenshot_path)
                #print(name + " Screenshot Saved")
                print_log += name + " failed: " + name + " Screenshot Saved\n"
                return False,print_log

        except TimeoutException:
            screenshot_name = f"{name}_TimeOutException_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            screenshot_path = os.path.join(screenshot_folder, screenshot_name)
            driver.save_screenshot(screenshot_path)
            #print(name + " Exception Screenshot Saved")
            print_log += name + " : " + name + " Screenshot Saved\n"
        return True,print_log