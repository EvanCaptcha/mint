import requests
import time
import json
import threading
import names
from bs4 import BeautifulSoup
import cloudscraper
import random
from random import randint
import string
from discord_webhook import DiscordWebhook, DiscordEmbed
from random import randrange

webhookURL = 'https://discordapp.com/api/webhooks/644337729227980810/X2J2WAhFnK81MwC_kCfZIFxv2_oQYGMoZU-2bMkxNF_KawrV-pmDdA2ApYwLZ0cOr-k0'
global data
pid = input("What is the PID? ")
threads = input("How many threads? ")
catchall = input("What is the catchall? ")
cc_type = input("Please type: Visa if your profiles are Visa, or Master for MasterCard ")
def task():
    with open('config.json') as json_file:
        data = json.load(json_file)
    for atts in data['cards']:
        name = names.get_full_name(gender='male')
        list = name.split(' ')
        first = list[0]
        last = list[1]
        cc = atts['number']
        print(cc)
        cc_last4 = cc[12:]
        exp = atts['exp']
        splitexp = exp.split('/')
        expMo = splitexp[0]
        expYr = splitexp[1]
        cvv = atts['cvv']
        addy = atts['addy']
        city = atts['city']
        postal = atts['postal']
        state = atts['state']
        def random_with_N_digits(n):
            range_start = 10 ** (n - 1)
            range_end = (10 ** n) - 1
            return randint(range_start, range_end)
        phoneNumber = random_with_N_digits(10)
        def random_string_generator_variable_size(min_size, max_size, allowed_chars):
            return ''.join(random.choice(allowed_chars) for x in range(randint(min_size, max_size)))
        chars = string.ascii_letters
        rando = random_string_generator_variable_size(6, 12, chars)
        print(phoneNumber)
        start = time.time()
        session = requests.session()
        s = cloudscraper.create_scraper(sess=session)
        print("Attempt ATC...")
        r = s.post(f"https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-AddProduct?format=ajax&cartAction=add&pid={pid}&cgid=null&egc=null&navid=xsellhome&navid=xsellhome&Quantity=1")
        print("Validating cart limit with USMint backend...")
        r = s.get("https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-ValidateBulkLimit")
        print("Going to checkout...")
        r = s.get("https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-Show")
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        token = soup.find("form", attrs={"name": "dwfrm_cart"})['action']
        shipping = soup.find("input", attrs={"name": "dwfrm_singleshipping_securekey"})['value']
        billing = soup.find("input", attrs={"name": "dwfrm_billing_securekey"})['value']
        headers = {
        'authority': 'catalog.usmint.gov',
        'accept': 'text/html, */*; q=0.01',
        'origin': 'https://catalog.usmint.gov',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-Show',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9'
        }
        email = f'{rando}@{catchall}'
        randoAddy = random_string_generator_variable_size(3, 3, chars)
        apt = randrange(99)
        split = addy.split(" ")
        i = len(split)
        join = ' '.join(split[1: i])
        house_jigged = f'{addy[0]} {randoAddy} {join}'
        data = {
          'dwfrm_singleshipping_shippingAddress_addressFields_selectedAddressID': 'newaddress',
          'dwfrm_singleshipping_shippingAddress_addressFields_firstName': first,
          'dwfrm_singleshipping_shippingAddress_addressFields_lastName': last,
          'dwfrm_singleshipping_shippingAddress_addressFields_phone': phoneNumber,
          'dwfrm_singleshipping_shippingAddress_email': f'{rando}@{catchall}',
          'dwfrm_billing_billingAddress_emailsource': 'Website - Checkout',
          'dwfrm_singleshipping_shippingAddress_addressFields_address1': house_jigged,
          'dwfrm_singleshipping_shippingAddress_addressFields_address2': f'APT {apt}',
          'dwfrm_singleshipping_shippingAddress_addressFields_city': city,
          'dwfrm_singleshipping_shippingAddress_addressFields_states_state': state,
          'dwfrm_singleshipping_shippingAddress_addressFields_zip': postal,
          'dwfrm_singleshipping_shippingAddress_addressFields_country': 'US',
          '__avs_select': '2',
          'dwfrm_singleshipping_shippingAddress_isCreateAccountSelected': 'false',
          'dwfrm_singleshipping_createAccount_password': '',
          'dwfrm_singleshipping_createAccount_passwordconfirm': '',
          'dwfrm_singleshipping_createAccount_question': '1',
          'dwfrm_singleshipping_createAccount_answer': '',
          'dwfrm_singleshipping_securekey': shipping,
          'dwfrm_billing_securekey': billing,
          'format': 'ajax',
          'refresh': 'shipping',
          'dwfrm_singleshipping_shippingAddress_applyShippingAddress': ''
        }

        response = s.post(token, headers=headers, data=data)
        data = [
            ('dwfrm_singleshipping_shippingAddress_useAsBillingAddress', 'true'),
            ('dwfrm_billing_billingAddress_addressFields_selectedAddressID', ''),
            ('dwfrm_billing_billingAddress_addressFields_firstName', first),
            ('dwfrm_billing_billingAddress_addressFields_lastName', last),
            ('dwfrm_billing_billingAddress_addressFields_address1', house_jigged),
            ('dwfrm_billing_billingAddress_addressFields_address2', ''),
            ('dwfrm_billing_billingAddress_addressFields_city', city),
            ('dwfrm_billing_billingAddress_addressFields_states_state', state),
            ('dwfrm_billing_billingAddress_addressFields_zip', postal),
            ('dwfrm_billing_billingAddress_addressFields_country', 'US'),
            ('dwfrm_billing_billingAddress_addressFields_phone', phoneNumber),
            ('dwfrm_billing_billingAddress_email_emailAddress', f'{rando}@{catchall}'),
            ('dwfrm_billing_securekey', billing),
            ('dwfrm_billing_securekey', billing),
            ('dwfrm_singleshipping_securekey', shipping),
            ('refresh', 'payment'),
            ('format', 'ajax'),
            ('dwfrm_billing_applyBillingAndPayment', ''),
            ('dwfrm_billing_paymentMethods_selectedPaymentMethodID', 'CREDIT_CARD'),
            ('dwfrm_billing_paymentMethods_creditCard_type', cc_type),
            ('dwfrm_billing_paymentMethods_creditCard_owner', name),
            ('dwfrm_billing_paymentMethods_creditCard_number', cc),
            ('dwfrm_billing_paymentMethods_creditCard_month', expMo),
            ('dwfrm_billing_paymentMethods_creditCard_year', expYr),
            ('dwfrm_billing_paymentMethods_creditCard_cvn', cvv),
            ('dwfrm_emailsignup_phone', ''),
        ]

        response = s.post(token, headers=headers, data=data)
        data = {
            'dwfrm_billing_paymentMethods_selectedPaymentMethodID': 'CREDIT_CARD',
            'dwfrm_billing_paymentMethods_creditCard_type': cc_type,
            'dwfrm_billing_paymentMethods_creditCard_owner': name,
            'dwfrm_billing_paymentMethods_creditCard_number': f'************{cc_last4}',
            'dwfrm_billing_paymentMethods_creditCard_month': expMo,
            'dwfrm_billing_paymentMethods_creditCard_year': expYr,
            'dwfrm_billing_paymentMethods_creditCard_cvn': '***',
            'dwfrm_billing_securekey': billing,
            'dwfrm_emailsignup_phone': ''
        }

        response = s.post('https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/COSummary-Submit', headers=headers, data=data)
        end = time.time()
        total = end - start
        if not 'We are sorry, but we are unable to process your payment and submit your order this time.' in response.text:
            print(f'Succesful in {total} seconds!')
            webhook = DiscordWebhook(url=webhookURL)
            embed = DiscordEmbed(title='USMint - Success!', description=f'Succesful in {total} seconds! Email used was: {email}', color=int('009000'))
            webhook.add_embed(embed)
            webhook.execute()
        else:
            print("Failed checkout (card decline)")
            webhook = DiscordWebhook(url=webhookURL)
            embed = DiscordEmbed(title='USMint - Failure!', description=f'Failure(card decline) in {total} seconds! Email used was {email}', color=int('009000'))
            webhook.add_embed(embed)
            webhook.execute()
jobs = []
for i in range(0, int(threads)):
    jobs.append(threading.Thread(target=task))

# start  threads
for j in jobs:
    j.start()

# ensure all threads have been finished
for j in jobs:
    j.join()
