import requests

def fetch_and_save_html(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")


if __name__=="__main__":
    url = 'https://www.imsnsit.org/imsnsit/notifications.php'
    html_file = 'notices.html'
    fetch_and_save_html(url, html_file)
