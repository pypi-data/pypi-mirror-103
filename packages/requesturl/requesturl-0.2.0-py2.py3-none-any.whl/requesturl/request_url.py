"""Main module."""
# import requests
from random import choice
import urllib.request
from fp.fp import FreeProxy
from Proxy_List_Scrapper import Scrapper, Proxy, ScrapperException


def request_url(
    url: str,
    data,
    proxy: dict = None,
    timeout: float = 2.5,
):

    headers = {
        "User-Agent": "Mozilla/5.0",
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        " AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/88.0.4324.104 Safari/537.36",
    }

    if proxy is None:
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, data, timeout=timeout) as f:
            response = f.read().decode("utf-8")
    else:
        # proxy = {
        # "http": FreeProxy(anonym=True, rand=True, timeout=timeout).get(),
        # "https": FreeProxy(anonym=True, rand=True, timeout=timeout).get(),
        # }

        # req = urllib.request.Request(url, headers=headers)

        proxy_support = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(proxy_support)
        opener.addheaders = [("User-agent", "Mozilla/5.0")]

        urllib.request.install_opener(opener)

        with urllib.request.urlopen(url, data, timeout=timeout) as f:
            response = f.read().decode("utf-8")

    # s = requests.Session()
    # s.proxy = {
    #     "http": FreeProxy(anonym=True, rand=True, timeout=timeout).get(),
    #     "https": FreeProxy(anonym=True, rand=True, timeout=timeout).get(),
    # }
    # response = s.get(url).text
    # s.cookies.clear()

    return response


def get_new_proxy_1(
    oldAddress: str = None,
    anonym: bool = False,
    rand: bool = True,
    timeout: float = 2,
) -> dict:

    print("\nGetting new proxy address")
    proxyAddress = FreeProxy(anonym=anonym, rand=rand, timeout=timeout).get()

    if proxyAddress is None:
        print("No working proxy")
        get_new_proxy_1(oldAddress)
        return

    proxy = {"http": proxyAddress, "https": proxyAddress}

    print("\t", oldAddress, " ---> ")
    print("\t", proxy, "\n")

    if proxy == oldAddress:
        print("New proxy is same with old one!")
        get_new_proxy_1(oldAddress)
        return

    return proxy


def get_new_proxy_2(
    oldAddress: str = None,
    category: str = "ALL",
    rand: bool = True,
) -> dict:

    print("\nGetting new proxy address")
    scrapper = Scrapper(category=category, print_err_trace=False)
    data = scrapper.getProxies()
    if data is None:
        print("No working proxy")
        get_new_proxy_2(oldAddress)
        return

    if rand == True:
        proxy_address = choice(data)
    else:
        proxy_address = data[0]
    proxy_address_ip_port = proxy_address.ip + ":" + proxy_address.port
    proxy = {"http": proxy_address_ip_port, "https": proxy_address_ip_port}

    print("\t", oldAddress, " ---> ")
    print("\t", proxy, "\n")

    if proxy == oldAddress:
        print("New proxy is same with old one!")
        get_new_proxy_2(oldAddress)
        return

    return proxy