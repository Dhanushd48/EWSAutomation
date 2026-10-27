from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time

from Utilities.driver_factory import DriverFactory


class OpenEWS:

    def run(self, printer_ip,logs,max_retries = 3):
        print_log = ""
        for attempt in range(max_retries):
            driver = DriverFactory.get_driver()
            try:

                driver.set_page_load_timeout(10)

                driver.get(f"http://{printer_ip}")

                #print("Page Title:", driver.title)
                print_log = print_log + "Page Title:"+ driver.title + "\n"
                #print("Current URL:", driver.current_url)
                print_log = print_log + "Current URL:" + driver.current_url + "\n\n"
                return driver,print_log

            except TimeoutException:
                msg = f"Attempt {attempt + 1}: Page load timed out"

                logs.append(msg)

            driver.quit()
        raise Exception(
            f"Unable to open EWS after {max_retries} attempts"
        )
        return None,print_log


