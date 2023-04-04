import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from constants import  *

options = Options()
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")

@pytest.fixture(scope="module")
def driver():
     driver = webdriver.Chrome(options=options)
     driver.get("https://www.saucedemo.com/")
     yield driver

def logout(driver):
    try:
       menu_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, MENU_BTN )))
       menu_button.click()
       logout_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, LT_BTN_ID)))
       logout_button.click()
       sleep(1)
    except:
        pass

#ekran görüntüsü kaydı yapar
def EKRANGORUNTUSU(driver, name):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    directory = now.split('_')[0]
    if not os.path.exists(directory):
        os.mkdir(directory)
    filename = f"{directory}/{name}_{now}.png"
    driver.save_screenshot(filename)
     
def test_username_ve_password_null(driver):
        
        U_ID = driver.find_element(By.ID, ID_USER)
        PS_ID = driver.find_element(By.ID, ID_PASSWORD)
        LG_BTN_ID_LOGİN = driver.find_element(By.ID, LG_BTN_ID)
     
        U_ID.send_keys("")
        PS_ID.send_keys("")


        LG_BTN_ID_LOGİN.click()
        ERROR_M_C = driver.find_element(
            By.CLASS_NAME, ERROR_M)

        E_MESSAGE = BOS_U_M
        C_MESSAGE = ERROR_M_C.text
        DURUM = E_MESSAGE == C_MESSAGE
        assert DURUM
        EKRANGORUNTUSU(driver,"test_username_ve_PS_ID_null.png")

        print(f"Test Durumu: {'Geçerli' if DURUM else 'Geçersiz'}")

#adı kısmı yazılı şifre boş iken,
def test_password_null(driver):
     driver.refresh()

     U_ID = driver.find_element(By.ID, ID_USER)
     PS_ID = driver.find_element(By.ID, ID_PASSWORD)
     LG_BTN_ID_LOGİN = driver.find_element(By.ID, LG_BTN_ID)
 
     U_ID.send_keys("kod")
     PS_ID.send_keys("")
     
     LG_BTN_ID_LOGİN.click()
     ERROR_M_C = driver.find_element(
        By.CLASS_NAME, ERROR_M)

     E_MESSAGE = BOS_P_M 
     C_MESSAGE = ERROR_M_C.text
     DURUM = E_MESSAGE == C_MESSAGE
     assert DURUM 
     EKRANGORUNTUSU(driver,"test_PS_ID_null.png")

     print(f"Test Durumu: {'Geçerli' if DURUM else 'Geçersiz'}")

#kilitli kullanıcı
def test_user_locked_error_text(driver):
     driver.refresh()
     U_ID = driver.find_element(By.ID, ID_USER)
     PS_ID = driver.find_element(By.ID, ID_PASSWORD)
     LG_BTN_ID_LOGİN = driver.find_element(By.ID, LG_BTN_ID)
     
     U_ID.send_keys(LOCKEDUSER)
     PS_ID.send_keys(PS_S)

     LG_BTN_ID_LOGİN.click()
     ERROR_M_C = driver.find_element(
        By.CLASS_NAME, ERROR_M)

     E_MESSAGE = KİLİT_US_O_M
     C_MESSAGE = ERROR_M_C.text
     DURUM = E_MESSAGE == C_MESSAGE

     assert DURUM
     EKRANGORUNTUSU(driver,"test_user_locked_error_text.png")

     print(f"Test Durumu: {'Geçerli' if DURUM else 'Geçersiz'}")

# çarpı butonuna basar
def test_carpi_button_click(driver):
     driver.refresh()
  
     U_ID = driver.find_element(By.ID, ID_USER)
     PS_ID = driver.find_element(By.ID, ID_PASSWORD)
     LG_BTN_ID_LOGİN = driver.find_element(By.ID, LG_BTN_ID)
    

     U_ID.send_keys("")
     PS_ID.send_keys("")
    

     LG_BTN_ID_LOGİN.click()
     ERROR_M_C = driver.find_element(
        By.CLASS_NAME, ERROR_M)
     error_button = driver.find_element(By.CLASS_NAME, ERROR_B)

     error_button.click()
     sleep(4)

     EKRANGORUNTUSU(driver,"test_carpi_button_click.png")
     print("\nçarpı iconuna tıklama testi")

#site açııyor mu kontrol eder
def test_standartuser_input_inventoryhtml(driver):
     driver.refresh()
   
     U_ID = driver.find_element(By.ID, ID_USER)
     PS_ID = driver.find_element(By.ID, ID_PASSWORD)
     LG_BTN_ID_LOGİN = driver.find_element(By.ID, LG_BTN_ID)

     U_ID.send_keys(S_U )
     PS_ID.send_keys(PS_S)

     LG_BTN_ID_LOGİN.click()

     current_url = driver.current_url
     expected_url = EXPECTED_URL
     DURUM = current_url == expected_url
     
     assert DURUM
     EKRANGORUNTUSU(driver,"test_standartuser_input_inventoryhtml.png")

# 6 ürün var mı onu listeler
def test_6_item_list(driver):
     logout(driver)

     U_ID = driver.find_element(By.ID, ID_USER)
     PS_ID = driver.find_element(By.ID, ID_PASSWORD)
     LG_BTN_ID_LOGİN = driver.find_element(By.ID, LG_BTN_ID)
     sleep(2)

     U_ID.send_keys(S_U )
     PS_ID.send_keys(PS_S)
     sleep(2)

     LG_BTN_ID_LOGİN.click()
     sleep(2)

     items = driver.find_elements(By.CLASS_NAME, "inventory_item")
     expected_item_count = 6
     DURUM = len(items) == expected_item_count

     print(f"Test Durumu: {'Geçerli' if DURUM else 'Geçersiz'}")
     assert DURUM
     EKRANGORUNTUSU(driver,"test_6_item_lis.png")
     sleep(8)

@pytest.mark.parametrize("item_name, item_price", [("Sauce Labs Backpack", 29.99),
                                                    ("Sauce Labs Bike Light", 9.99),
                                                    ("Sauce Labs Bolt T-Shirt", 15.99)])
def test_urun_fiyat_dogrulama(driver, item_name, item_price):

    driver.refresh()
    logout(driver)
    U_ID = driver.find_element(By.ID, ID_USER)
    PS_ID = driver.find_element(By.ID, ID_PASSWORD)
    LG_BTN_ID_LOGİN = driver.find_element(By.ID, LG_BTN_ID)
    

    U_ID.send_keys(S_U )
    PS_ID.send_keys(PS_S)
    

    LG_BTN_ID_LOGİN.click()
    

    item = driver.find_element(By.XPATH, f"//div[text()='{item_name}']/../../..//div[@class='pricebar']/div")
    price_text = item.text[1:]  
    price = float(price_text)

    assert price == item_price
    EKRANGORUNTUSU(driver,f"{item_name}_urun_fiyat_dogrulama.png")
    sleep (8)

#sepete ekleme
def test_sepete_ekleme(driver):
    driver.refresh()
    logout(driver)
    U_ID = driver.find_element(By.ID, ID_USER)
    PS_ID = driver.find_element(By.ID, ID_PASSWORD)
    LG_BTN_ID_LOGİN = driver.find_element(By.ID, LG_BTN_ID)

    U_ID.send_keys(S_U )
    PS_ID.send_keys(PS_S)
    LG_BTN_ID_LOGİN.click()

    item_name = "Sauce Labs Backpack"
    item = driver.find_element(By.XPATH, f"//div[@class='inventory_item_name'][text()='{item_name}']/ancestor::div[@class='inventory_item']//button")
    item.click()
    
    cart_count = driver.find_element(By.CLASS_NAME, SHP_C_B)
    assert cart_count.text == "1"

    EKRANGORUNTUSU(driver, "test_sepete_ekleme.png")

#ürün sıralaması dorğumu kontrol eder
def test_urun_siralamasi(driver):
    driver.refresh()
    logout(driver)
    U_ID = driver.find_element(By.ID, ID_USER)
    PS_ID = driver.find_element(By.ID, ID_PASSWORD)
    LG_BTN_ID_LOGİN = driver.find_element(By.ID, LG_BTN_ID)

    U_ID.send_keys(S_U )
    PS_ID.send_keys(PS_S)
    LG_BTN_ID_LOGİN.click()

    sorting_dropdown = driver.find_element(By.CLASS_NAME, PRDCT_S_C)
    sorting_options = sorting_dropdown.find_elements(By.TAG_NAME, "option")

    for option in sorting_options:
        option_value = option.get_attribute("value")
        sorting_dropdown.send_keys(option_value)

        items = driver.find_elements(By.CLASS_NAME, İNVTR_İ_N)
        item_names = [item.text for item in items]
        sorted_item_names = sorted(item_names)

        assert item_names == sorted_item_names

    EKRANGORUNTUSU(driver, "test_urun_siralamasi.png")
    
#geri tuşuna tıklayıp ardından mevcut URL’in doğru olup olmadığını kontrol etmeyi sağlar
def test_geri_tusu(driver):
    driver.refresh()
    logout(driver)
    U_ID = driver.find_element(By.ID, ID_USER)
    PS_ID = driver.find_element(By.ID, ID_PASSWORD)
    LG_BTN_ID_LOGİN = driver.find_element(By.ID, LG_BTN_ID)

    U_ID.send_keys(S_U )
    PS_ID.send_keys(PS_S)
    LG_BTN_ID_LOGİN.click()

    item_name = "Sauce Labs Bike Light"
    item = driver.find_element(By.XPATH, f"//div[text()='{item_name}']/../..//a")
    item.click()

    back_button = driver.find_element(By.CLASS_NAME, İVTY_DS_B_B)
    back_button.click()

    current_url = driver.current_url
    expected_url = EXPECTED_URL
    DURUM = current_url == expected_url

    assert DURUM

    EKRANGORUNTUSU(driver, "test_geri_tusu.png")

#ürün filtrelemesi
def test_urun_filtreleme(driver):
    driver.refresh()
    logout(driver)
    U_ID = driver.find_element(By.ID, ID_USER)
    PS_ID = driver.find_element(By.ID, ID_PASSWORD)
    LG_BTN_ID_LOGİN = driver.find_element(By.ID, LG_BTN_ID)

    U_ID.send_keys(S_U )
    PS_ID.send_keys(PS_S)
    LG_BTN_ID_LOGİN.click()

    filter_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, PRDCT_S_C)))
    sleep(2)
    filter_button.click()

    price_low_to_high = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[text()='Price (low to high)']")))
    sleep(2)
    price_low_to_high.click()

    items = driver.find_elements(By.CLASS_NAME, İNVTR_İ_P)
    expected_item_prices = sorted([float(item.text[1:]) for item in items])

    actual_item_prices = [float(item.text[1:]) for item in items]

    assert actual_item_prices == expected_item_prices

    EKRANGORUNTUSU(driver, "test_urun_filtreleme.png")    

