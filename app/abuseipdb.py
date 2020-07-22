import configparser  # https://docs.python.org/3/library/configparser.html
import requests  # https://developers.virustotal.com/v2.0/reference#file-scan
import socket
from datetime import datetime
import app.cfg


def abuseipdb(sessionpeer, mailfrom, mailto):
    config = configparser.ConfigParser()
    config.read('icarus.config')
    abuseip = config['IPDBAPI']['AbuseIPDB']
    apikey = config['IPDBAPI']['IPDBAPI']
    # using configparser to pull the apikey details for abuseipdb.
    headers = {'Key': apikey, 'Accept': 'application/json', }
    data = {'categories': '11', 'ip': sessionpeer, 'comment': 'Icarus Smtp honeypot github'}
    # this is the API. https://docs.abuseipdb.com/#report-endpoint

    if abuseip != "no":  # checking if abuseipdb is enabled. Disabled by default.
        url = "https://api.abuseipdb.com/api/v2/report"

        if apikey != "PUT API KEY HERE":
            abusepost = requests.post(url, headers=headers, data=data)


def report(ip):
    config = configparser.ConfigParser()
    config.read('icarus.config')
    abuseip = config['IPDBAPI']['AbuseIPDB']
    apikey = config['IPDBAPI']['IPDBAPI']
    # using configparser to pull the apikey details for abuseipdb.
    headers = {'Key': apikey, 'Accept': 'application/json', }
    data = {'categories': '15', 'ip': ip, 'comment': 'Icarus honeypot on github'}
    # this is the API. https://docs.abuseipdb.com/#report-endpoint

    if abuseip != "no":  # checking if abuseipdb is enabled. Disabled by default.
        url = "https://api.abuseipdb.com/api/v2/report"

        if apikey != "PUT API KEY HERE":
            abusepost = requests.post(url, headers=headers, data=data)


def prereport(addr):

    day_of_year = datetime.now().timetuple().tm_yday

    db = app.cfg.attackdb
    if addr in db:
        if db[addr] != day_of_year:
            report(addr)
            largfeed(addr)
    db[addr] = day_of_year


def largfeed(addr):
    config = configparser.ConfigParser()
    config.read('icarus.config')
    largfeedon = config['LARGFEED']['Largfeed']
    largfeedserver = config['LARGFEED']['Server']
    largfeedport = config['LARGFEED']['Port']
    # very straight forward open socket and send bytes data.
    if largfeedon != "no":
        HOST = largfeedserver
        PORT = int(largfeedport)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(bytes(addr + "\n", "utf-8"))





