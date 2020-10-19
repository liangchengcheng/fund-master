import requests


# 爬取的文本信息
def get_resonse(url):
    """
    :param url: 网页URL
    :return: 爬取的文本信息
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        print('Failed to get response to url!')
        return ''