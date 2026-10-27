import sys
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Change_Password import Change_Password
from Scripts.SetWebService import SetWebService
from Scripts.Networking.TCP_IP_Settings import TCP_IP_Settings
from Scripts.Networking.Other_Settings import Other_Settings
from Scripts.Networking.Network_Settings import Network_Settings
from Scripts.SetFax import SetFax
from Scripts.SetGeneral import SetGeneral
from Scripts.SetSecurity import SetSecurity
from Scripts.SignUp import SignUp
from Scripts.OpenEWS import OpenEWS
from Scripts.TestSuccessMessage import TestSuccessMessage
from Utilities.driver_store import drivers
from Utilities.user_context import get_user_ip


def main(
    choice,
    printer_ip,
    password,
    domain="",
    ip1="",
    fax_number="",
    old_password="",
    new_password="",
    logs = None
):
    if logs is None:
        logs = []
    is_success = True
    TestSuccessMessage().delete()
    #printer_ip = input("Enter the printer ip address: ")
    #password = input("Enter the new password: ")
    start = time.time()
    driver, print_log = OpenEWS().run(printer_ip,logs)
    drivers[get_user_ip()] = driver
    logs.append(print_log)
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.ID, "SettingsPages"))
        )


    except TimeoutException:

        logs.append("Not signed in. Logging in...\n")

        is_success,print_log = SignUp().run(driver, password)
        logs.append(print_log)

    if not is_success:
        logs.append("Sign In Failed! Wrong Password\n")
        end = time.time()
        logs.append(f"{int((end - start) / 60)} minutes and {int((end - start) % 60)} seconds")
        #logs.append("__COMPLETED__")
        driver.quit()
        return False, "\n".join(logs)


    match choice:
        case 1:
            #domain =  input("Enter the domain: ")
            #ip1 =  input("Enter the server ip address: ")
            #fax_number = input("Enter the fax number: ")
            logs.append("Executing General........\n")
            result, print_log = SetGeneral().run(driver, ip1)
            is_success = result and is_success
            logs.append(print_log)

            logs.append("Executing Fax........\n")
            result, print_log = SetFax().run(driver, fax_number)
            is_success = result and is_success
            logs.append(print_log)

            logs.append("Executing Security........\n")
            result, print_log = SetSecurity().run(driver, password)
            is_success = result and is_success
            logs.append(print_log)

            logs.append("Executing Networking........\n")
            result, print_log = TCP_IP_Settings().run(driver, domain, ip1)
            is_success = result and is_success
            logs.append(print_log)

            result, print_log = Network_Settings().run(driver)
            is_success = result and is_success
            logs.append(print_log)

            result, print_log = Other_Settings().run(driver)
            is_success =  result and is_success
            logs.append(print_log)

            result, print_log = SetWebService().run(driver, printer_ip)
            is_success = result and is_success
            logs.append(print_log)

            if is_success:
                logs.append("EWS Automation Completed Successfully\n")
            else:
                logs.append("EWS Automation Failed.\n")
        case 2:
            #old_password = input("Enter the old password: ")
            #new_password = input("Enter the new password: ")
            is_success = Change_Password().run(driver,old_password, new_password)
            if (is_success):
                logs.append("Changed Password Successfully\n")
            else:
                logs.append("Password Change Failed.\n")
    time.sleep(5)
    end = time.time()
    logs.append(f"{int((end-start)/60)} minutes and {int((end-start)%60)} seconds")
    #logs.append("__COMPLETED__")
    driver.quit()
    for i, item in enumerate(logs):
        print(i, type(item), item)
    return is_success, "".join(logs)

if __name__ == "__main__":
    main()
