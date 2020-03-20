# -*- coding: utf-8 -*-
# In order to run this script the sender mail address needs to have updated google setting to allow
# less secure applications to use the account
# Also scrapy needs to be installed and this script set up as a spider
# SSL certificates need be installed (if used on MacOS)

import scrapy
import smtplib
import ssl
from datetime import datetime

COUNTRIES = ("Bulgaria",
             "Austria",
             "Netherlands")

OUTPUT_STR = """
Country: {0}
Total Cases: {1}
New Cases: {2}
===================================
"""


def parse_data(item):
    return item if item.strip() else "NONE"


def send_mail(mail_body):
    subject = "Coronavirus stats in your desired countries"
    body = "\n".join(mail_body)
    body += "Check the link: https://www.worldometers.info/coronavirus/"
    body_end = f"Data collected on {str(datetime.now())}"
    msg = f"Subject: {subject}\n\n{body}\n{body_end}"
    sender_mail = "Fill me"  # Sender email address
    sender_password = "Fill me" # Sender password
    receiver_mail = ["Fill me"] # List of receivers
    smtp_server = "smtp.gmail.com"
    ssl_port = 465
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, ssl_port, context=context) as server:
        server.login(sender_mail, sender_password)
        # Send the mail
        server.sendmail(sender_mail, receiver_mail, msg)
        print("Email has been sent!")


class CoronaAnalystSpider(scrapy.Spider):
    name = 'corona_analyst'
    allowed_domains = ['worldmeters.info']
    start_urls = ['https://www.worldometers.info/coronavirus']

    def parse(self, response):
        countries = response.css("#main_table_countries_today tbody tr").getall()
        output_data = []
        for country in countries:
            for c in COUNTRIES:
                if c in country:
                    country_data = scrapy.Selector(text=country)
                    # Extract the data within the tds
                    data = country_data.xpath('//td//text()').extract()
                    country_name = parse_data(data[0])
                    total_cases = parse_data(data[1])
                    new_cases = parse_data(data[2])
                    if not new_cases.startswith("+"):
                        new_cases = "No new cases"
                    # format the string output
                    output = OUTPUT_STR.format(country_name, total_cases, new_cases)
                    output_data.append(output)
        send_mail(output_data)
        yield None
