import requests
import hashlib
import sys

def requestData(first5):
    """""
    Checks if your password has been hacked

    :param password_checker7366:
    :return:
    """
    url = "https://api.pwnedpasswords.com/range/" + first5
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Error while fetching data: {res.status_code}. Check it again")
    return res


def getPwdHack(password):
    hashcode = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    first5,other = hashcode[:5], hashcode[5:]
    response = requestData(first5)
    return findPwdHack(response,other)

def findPwdHack(hashes,hash_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h,count in hashes:
        if h == hash_check:
            return count
    return 0

def pwd_chk(args):
    for pwd in args:
        count = getPwdHack(pwd)
        if count:
            print((f'{pwd} was found {count} times.. You should change it'))
        else:
            print(f"{pwd} was NOT found. keep it up !!")
    return 'Success'


pwd_chk(sys.argv[1:])




