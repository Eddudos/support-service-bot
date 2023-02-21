from django.test import TestCase


import logging
from fast_bitrix24 import Bitrix

logging.getLogger('fast_bitrix24').addHandler(logging.StreamHandler())

webhook = "https://b24-la4wj9.bitrix24.ru/rest/1/493x8jxfkdelqjwg/"
b = Bitrix(webhook)

leads = b.get_all('imopenlines.config.get', params={'CONFIG_ID': 4})

# leads = b.get_all('imconnector.register',
#                 params= {
#                     'ID': 3748,
#                     'NAME': 'test1',
#                     'ICON': {'DATA_IMAGE': "data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='64.712' height='71.891' viewBox='0 0 17.122 19.021'%3e%3cg transform='matrix(.49469 0 0 .49469 -50.713 -46.175)'%3e%3cpath d='M122.235 123.206l3.058 4.294-5.419.836s-.541 1.552.923 1.424c1.465-.128 3.837-.593 3.837-.593l-2.952 1.273s-.544 1.871 1.389 1.212c1.442-.492 3.097-1.814 3.097-1.814 4.34-1.315 1.367-1.414-2.069-6.795zM119.191 123.686l-2.892 4.407-3.558-4.072s-1.666-.004-1.016 1.314c.65 1.318 2.78 2.748 2.78 2.748l-3.266-1.753s-1.623.621-.307 2.184c.982 1.165 3.505 1.242 3.505 1.242 2.68 2.08 1.8.594 5.582-4.392z' fill='%23ff7f2a'/%3e%3cpath d='M113.807 93.341c-6.237 0-11.292 4.488-11.292 10.023.078 4.01 3.213 8.008 3.34 11.158 0 6.015 6.313 10.892 14.1 10.892 7.786 0 17.171-6.747 17.171-12.762 0-4.499-3.179-6.129-8.61-7.752-1.405-6.812-8.54-11.44-14.71-11.559z' fill='%23fc0'/%3e%3cpath d='M107.059 105.636c-1.873.282-3.208 5.212-3.208 5.212l5.48.267s2.538-2.005 1.737-3.742c-.802-1.737-2.25-2.002-4.01-1.737z' fill='%23ff7f2a'/%3e%3cellipse ry='1.871' rx='1.203' cy='102.83' cx='111.736' fill='%2328170b'/%3e%3cellipse cx='105.722' cy='102.696' rx='1.203' ry='1.871' fill='%2328170b'/%3e%3cpath d='M119.724 111.125s6.426-1.606 8.599-.85c2.173.755 4.914 1.795 3.496 4.346-1.417 2.552-3.685 4.442-7.843 5.67-3.445 1.018-7.087.567-7.087.567s14.836-3.402 13.513-7.182c-1.323-3.78-10.678-2.551-10.678-2.551z' fill='%23fba500'/%3e%3c/g%3e%3c/svg%3e",
#                              'COLOR': "#1900ff",
#                              'SIZE': "90%",
#                              'POSITION': "center",
#                              'PLACEMENT_HANDLER': "http://portal.bitrix24.com/rest/placement.bind/?access_token=sode3flffcmv500fuagrprhllx3soi72"
#                     },
#                     'PLACEMENT_HANDLER': "http://95.163.235.140/test_wsgi"
#                 })

print('\n',leads)
