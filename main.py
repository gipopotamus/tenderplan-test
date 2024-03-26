from tasks import fetch_links

if __name__ == '__main__':
    fetch_links.delay(1)
    fetch_links.delay(2)
