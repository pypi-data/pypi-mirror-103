# -*- coding: utf-8 -*-
"""
Created on 2021/4/25 10:22 上午
---------
@summary: 将浏览器的cookie转为request的cookie
---------
@author: Boris
@email: boris_liu@foxmail.com
"""

false = False
true = True
a = [
{
    "domain": ".baidu.com",
    "expirationDate": 1620209619.268637,
    "hostOnly": false,
    "httpOnly": true,
    "name": "__yjs_duid",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1_87ea49fb1c266d733b91501dc6ca2f3e1617617619197",
    "id": 1
},
{
    "domain": ".baidu.com",
    "expirationDate": 1618819341,
    "hostOnly": false,
    "httpOnly": false,
    "name": "BA_HECTOR",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "0180a08k05a42124in1g7qanu0r",
    "id": 2
},
{
    "domain": ".baidu.com",
    "expirationDate": 1649077348.94786,
    "hostOnly": false,
    "httpOnly": false,
    "name": "BAIDUID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "451C45AEDA6E3B41B6DA8573B2FB3257:FG=1",
    "id": 3
},
{
    "domain": ".baidu.com",
    "expirationDate": 1650351743.216723,
    "hostOnly": false,
    "httpOnly": false,
    "name": "BAIDUID_BFESS",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "451C45AEDA6E3B41B6DA8573B2FB3257:FG=1",
    "id": 4
},
{
    "domain": ".baidu.com",
    "expirationDate": 1618900455.212587,
    "hostOnly": false,
    "httpOnly": false,
    "name": "BDORZ",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "B490B5EBF6F3CD402E515D22BCDA1598",
    "id": 5
},
{
    "domain": ".baidu.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "BDRCVFR[feWj1Vr5u3D]",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "I67x6TjHwwYf0",
    "id": 6
},
{
    "domain": ".baidu.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "BDSFRCVID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "MF4OJeC62GIgNroefIhBKw38t34JdITTH6ao1Q64TMu-BMApy_bTEG0PSx8g0Ku-MSrBogKK0mOTHv8F_2uxOjjg8UtVJeC6EG0Ptf8g0f5",
    "id": 7
},
{
    "domain": ".baidu.com",
    "expirationDate": 1934171543.519111,
    "hostOnly": false,
    "httpOnly": true,
    "name": "BDSFRCVID_BFESS",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "MF4OJeC62GIgNroefIhBKw38t34JdITTH6ao1Q64TMu-BMApy_bTEG0PSx8g0Ku-MSrBogKK0mOTHv8F_2uxOjjg8UtVJeC6EG0Ptf8g0f5",
    "id": 8
},
{
    "domain": ".baidu.com",
    "expirationDate": 1934175743.21681,
    "hostOnly": false,
    "httpOnly": true,
    "name": "BDUSS_BFESS",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "lHcktiWTJieDVjTX5ad1NhN0dDZDdIeFhJflJNWUlYVHZzUmJZcldzbng3WlJnSUFBQUFBJCQAAAAAAAAAAAEAAAB20CUvxM-5rNLBt-Nub2x5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPFgbWDxYG1gRW",
    "id": 9
},
{
    "domain": ".baidu.com",
    "expirationDate": 2626913483,
    "hostOnly": false,
    "httpOnly": false,
    "name": "BIDUPSID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "451C45AEDA6E3B41F0F5F906A4D61A12",
    "id": 10
},
{
    "domain": ".baidu.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "delPer",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "0",
    "id": 11
},
{
    "domain": ".baidu.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "H_BDCLCKID_SF",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "JbFtVCD-JIv-jttkMJQE2tcH-UnLqMrlJgOZ0l8Ktq3zepr4hPotytkYypteqn0eJgQbaxbmWIQHDIjhj6OxXJQDL4cCbncdKHn4KKJxL-PWeIJo5DcY0nDYhUJiB5OLBan7LDnIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtnLhbRO4-TF-D5j3jM5",
    "id": 12
},
{
    "domain": ".baidu.com",
    "expirationDate": 1934171543.519145,
    "hostOnly": false,
    "httpOnly": true,
    "name": "H_BDCLCKID_SF_BFESS",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "JbFtVCD-JIv-jttkMJQE2tcH-UnLqMrlJgOZ0l8Ktq3zepr4hPotytkYypteqn0eJgQbaxbmWIQHDIjhj6OxXJQDL4cCbncdKHn4KKJxL-PWeIJo5DcY0nDYhUJiB5OLBan7LDnIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtnLhbRO4-TF-D5j3jM5",
    "id": 13
},
{
    "domain": ".baidu.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "H_PS_PSSID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "31660_33690_33848_33758_33675_33621_26350_33811",
    "id": 14
},
{
    "domain": ".baidu.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "PSINO",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "2",
    "id": 15
},
{
    "domain": ".baidu.com",
    "expirationDate": 3765024995.947836,
    "hostOnly": false,
    "httpOnly": false,
    "name": "PSTM",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1617541348",
    "id": 16
},
{
    "domain": "www.baidu.com",
    "hostOnly": true,
    "httpOnly": false,
    "name": "BD_CK_SAM",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "1",
    "id": 17
},
{
    "domain": "www.baidu.com",
    "hostOnly": true,
    "httpOnly": false,
    "name": "BD_HOME",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "1",
    "id": 18
},
{
    "domain": "www.baidu.com",
    "expirationDate": 1619679738,
    "hostOnly": true,
    "httpOnly": false,
    "name": "BD_UPN",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "123253",
    "id": 19
},
{
    "domain": "www.baidu.com",
    "expirationDate": 1650350055,
    "hostOnly": true,
    "httpOnly": false,
    "name": "COOKIE_SESSION",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "137724_2_7_8_7_0_0_0_7_0_0_0_356462_0_6_106_1618814056_1618676432_1618814050%7C9%23219267_3_1618676326%7C2",
    "id": 20
},
{
    "domain": "www.baidu.com",
    "expirationDate": 1618816641,
    "hostOnly": true,
    "httpOnly": false,
    "name": "H_PS_645EC",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "4e24lh%2FTTlqSAJbYA2iBd3g3jqZt8TCpsnJ%2BnlpjBSk1SvwtsPoB6A4VE4P9d0uMeXG2",
    "id": 21
}
]

# cookie = {}
# for data in a:
#     cookie[data.get("name")] = data.get("value")
#
# print(cookie)

def test():
    return object

request, *response = test()
print(request, response)

