import requests
from bs4 import BeautifulSoup
import mail
import asyncio
from datetime import datetime
import os
# URL of the website
URL = 'https://shop.aalborgpirates.dk/kampe'
DELAY = 900 #60 seconds/min * 15 minutes = 900 seconds
def get_html(URL = URL):
    response = requests.get(URL)

    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
    else:
        print("Failed to retrieve content. Status code:", response.status_code)
        html_content = response.status_code
    return html_content


def get_matches(require_new = True):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(get_html(), 'html.parser')
    # Find all ticket listings
    tickets = soup.find_all('div', class_='item col-xs-12 list-view')
    matches_file = open("matches.txt", "a+", encoding="utf-8")
    matches_file.seek(0)
    matches = matches_file.read().split("\n")
    new_matches = ""
    all_matches = ""
    for x, ticket in enumerate(tickets):
        game = ticket.find('h4').text.strip()
        details = ticket.find('span', class_='size').text.strip().replace('\n', '').replace("\t","-")
        link = 'https://shop.aalborgpirates.dk' + ticket.find('a')['href']

        game = f"{game}  {details}"
        all_matches += f"{game} {link} \n\n"
        if game in matches:
            continue
        new_matches += f"{game} {link} \n\n"
        matches_file.write(f"{game}\n")
    matches_file.close()

    if new_matches != "":
        return new_matches
    elif not require_new:
        return all_matches
    return False
def send_mail_multiple_receivers(receivers, body, subject):
    for receiver in receivers:
        mail.send_email(body, subject, receiver)
async def main():
    email = os.environ.get("EMAIL")
    email_password = os.environ.get("PASSWORD")
    receivers = os.environ.get("RECEIVERS")
    if not email or not email_password or not receivers:
        print("Either email or password is missing")
        exit(1)
    once_per_day = False
    day = 100
    mail.send_email("Script started", "Script started", receivers)
    print("Script started")
    while True:        
        now = datetime.now()
        if day != now.strftime("%d"):
            once_per_day = False
        day = now.strftime("%d")
        hour = now.strftime("%H")
        if int(hour) == 15 and not once_per_day:
            print("Sending daily update")
            matches = get_matches(False)
            if matches:
                body = "This is just your daily update/heartbeat, if you want to unsubscribe, tough luck! \n\n" + matches
                mail.send_email(body, "Daily update", receivers)
            once_per_day = True
        matches = get_matches()
        if matches:
            body = "New matches available! \n\n" + matches
            mail.send_email(body, "New matches", receivers)
        await asyncio.sleep(DELAY)
asyncio.run(main())