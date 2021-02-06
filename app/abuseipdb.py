import configparser  # https://docs.python.org/3/library/configparser.html
import requests  # https://developers.virustotal.com/v2.0/reference#file-scan
import socket
import time
from datetime import datetime
import app.cfg

config = configparser.ConfigParser()
config.read('icarus.config')
abuseip = config['AbuseIPDB']['IPDBEnable']
apikey = config['AbuseIPDB']['IPDBKey']
hostname = config['ADDRESSES']['HOSTNAME']

def report_smtp(sessionpeer, mailfrom, mailto):
    message = f'SMTP attack triggered by {sessionpeer} ({hostname})'
    headers = {'Key': apikey, 'Accept': 'application/json', }
    data = {'categories': '11, 15', 'ip': sessionpeer, 'comment': message}
    # this is the API. https://docs.abuseipdb.com/#report-endpoint

    if abuseip != "no":  # checking if abuseipdb is enabled. Disabled by default.
        url = "https://api.abuseipdb.com/api/v2/report"

        if apikey != "PUT API KEY HERE":
            abusepost = requests.post(url, headers=headers, data=data)


def report(ip, port, type):
    message = f'{type} attack on port {port} triggered by {ip} ({hostname})'
    headers = {'Key': apikey, 'Accept': 'application/json', }
    data = {'categories': '15, 14', 'ip': ip, 'comment': message}
    # this is the API. https://docs.abuseipdb.com/#report-endpoint

    if abuseip != "no":  # checking if abuseipdb is enabled. Disabled by default.
        url = "https://api.abuseipdb.com/api/v2/report"

        if apikey != "PUT API KEY HERE":
            abusepost = requests.post(url, headers=headers, data=data)


def prereport(addr, port, type):
    day_of_year = datetime.now().timetuple().tm_yday
    # If we already have the address but no attack today. Report.
    if addr in app.cfg.attackdb:
        if app.cfg.attackdb[addr] != day_of_year:
            report(addr)
            app.cfg.largfeedqueue.append(addr)
    # If we don't have the address at all. Report.
    else:
        report(addr, port, type)
        app.cfg.largfeedqueue.append(addr)
    app.cfg.attackdb[addr] = day_of_year


def largfeed():
    config = configparser.ConfigParser()
    config.read('icarus.config')
    largfeedserver = config['LARGFEED']['Server']
    largfeedport = config['LARGFEED']['Port']
    # very straight forward open socket and send bytes data.

    while True:
        try:
            HOST = largfeedserver
            PORT = int(largfeedport)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                if len(app.cfg.largfeedqueue) >= 1:
                    sock.connect((HOST, PORT))
                    addr = app.cfg.largfeedqueue.pop()
                    sock.sendall(bytes(addr + "\n", "utf-8"))
            time.sleep(5)
        except socket.timeout:
            time.sleep(60)

        except socket.error:
            time.sleep(60)
