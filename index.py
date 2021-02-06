from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import click
from clint.textui import puts, colored, indent
import time

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.set_window_position(0, 0)
browser.set_window_size(1020, 1020)

url = 'https://chilebabedulceria.com'


@click.command()
@click.option('--email', prompt='what is the email of the account you wish to log in to?')
@click.option('--pwd', prompt='what is the password for this account?', hide_input=True)
@click.option('--product', prompt='what is the name of the product you wish to search for?')
def main(email, pwd, product):
    puts(colored.blue('email: ' + email))
    puts(colored.blue('password: ' + pwd))
    puts(colored.blue('product: ' + product))
    # open the website
    browser.get(url)

    # login
    browser.find_element_by_id('customer_login_link').click()

    # get the page url for match later on
    prev_url = browser.current_url
    puts(colored.green('prev url: ' + prev_url))

    # find the email field
    browser.find_element_by_id('customer_email').send_keys(email)

    # find the password field
    browser.find_element_by_id('customer_password').send_keys(pwd)

    # find the sign in button and click
    browser.find_element_by_xpath(
        '//*[@id="customer_login"]/p[2]/input').click()

    # verify login
    if (browser.current_url == prev_url):
        puts(colored.red('Login failed!'))
        return

    # enter product into search bar
    browser.find_element_by_xpath(
        '//*[@id="shopify-section-header"]/header/div/div/div[2]/form/input[2]').send_keys(product)

    # search
    browser.find_element_by_xpath(
        '//*[@id="shopify-section-header"]/header/div/div/div[2]/form/button').click()

    # click on the first hit
    browser.find_element_by_class_name('product-grid-item').click()

    # add to cart
    browser.find_element_by_xpath(
        '//*[@id="addToCart-product-template"]').click()

    # check out
    browser.find_element_by_xpath(
        '//*[@id="shopify-section-header"]/header/div/div/div[2]/a').click()

    # delay so dynamic content can pop up to be clicked
    time.sleep(2)
    puts(colored.blue('sleeping for 2 seconds...'))

    browser.find_element_by_xpath(
        '//*[@id="dynamic-checkout-cart"]/div/div[2]/div/ul/li[2]/iframe').click()
    puts(colored.blue('click Paypal checkout'))

    time.sleep(2)
    puts(colored.blue('sleeping for 2 seconds...'))
    paypal()


@click.command()
@click.option('--paypal_email', prompt=True)
@click.option('--paypal_pwd', prompt=True, hide_input=True)
def paypal(paypal_email, paypal_pwd):
    puts(colored.blue('paypal email: ' + paypal_email))
    puts(colored.blue('paypal password: ' + paypal_pwd))
    browser.find_element_by_id('email').send_keys(paypal_email)
    browser.find_element_by_id('btnNext').click()


if __name__ == '__main__':
    main()
