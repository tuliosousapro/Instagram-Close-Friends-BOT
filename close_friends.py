import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import USERNAME, PASSWORD  # Import credentials from config.py

# Configurações
TARGET = "TARGETED ACCOUNT" #PUT THE ACCOUNT @ THAT YOU AIM TO STEAL FOLLOWERS TO ADD TO CLOSE FRIENDS, MOST OF THE TIME IT WILL BE YOUR OWN ACCOUNT
CHALLENGE_WAIT_TIME = 300

def setup_driver():
    mobile_emulation = {"deviceName": "Pixel 2"}
    options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument("--disable-software-rasterizer")  # Added this line
    driver = webdriver.Chrome(options=options)
    return driver

def login_instagram(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    print("URL inicial:", driver.current_url)
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "username")))
        print("Campos de login encontrados.")
    except TimeoutException:
        print("Tempo esgotado para carregar a página de login.")
        return False
    
    # Preenche os campos
    try:
        user_input = driver.find_element(By.NAME, "username")
        pass_input = driver.find_element(By.NAME, "password")
        user_input.send_keys(username)
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.ENTER)
        time.sleep(5)
    except NoSuchElementException:
        print("Erro: Campos de username ou password não encontrados.")
        return False
    
    # Verifica o resultado do login
    print("URL após tentativa de login:", driver.current_url)
    print("Título da página:", driver.title)
    
    # Trata 2FA ou CAPTCHA
    try:
        challenge_input = WebDriverWait(driver, CHALLENGE_WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, "security_code"))
        )
        challenge_code = input("Insira o código de verificação enviado pelo Instagram: ")
        challenge_input.send_keys(challenge_code)
        challenge_input.send_keys(Keys.ENTER)
        time.sleep(5)
    except TimeoutException:
        pass
    
    # Trata pop-up "Salvar informações de login"
    try:
        not_now = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Agora não')]"))
        )
        not_now.click()
        time.sleep(2)
    except TimeoutException:
        pass
    
    # Verifica se o login foi bem-sucedido
    if "accounts/login" in driver.current_url:
        print("Erro: Ainda na página de login. Verifique credenciais, CAPTCHA ou 2FA.")
        print("Conteúdo da página:", driver.page_source[:1000])
        return False
    print("Login realizado com sucesso!")
    return True

def main():
    driver = setup_driver()
    if not login_instagram(driver, USERNAME, PASSWORD):
        print("Falha no login, encerrando.")
        driver.quit()
        return
    print("Login concluído, prosseguindo...")
    driver.quit()

if __name__ == "__main__":
    main()