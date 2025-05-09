import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://www.languagereactor.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.languagereactor.com/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}


def base_media_getMediaDocs(keyword=None, freq95_min=0, freq95_max=100000, page_min=None, page_max=None):
    json_data = {
        'auth': None,
        'translationLang_G': 'zh-CN',
        'freq95': {
            'min': freq95_min,
            'max': freq95_max,
        },
        'lang_G': 'en',
        'filters': {
            'mediaTab': 'TAB_BOOKS',
            'searchText': keyword,
            'pageCount': {
                'min': page_min,
                'max': page_max,
            },
        },
        'pinnedDiocoPlaylistIds': [],
        'diocoPlaylistId': 't_tx_all_en',
        'forceIncludeDiocoDocId': None,
    }

    response = requests.post('https://api-cdn.dioco.io/base_media_getMediaDocs_5', headers=headers, json=json_data)

    docs_metadata_list = response.json()['data']['docs_metadata']

    # 提取指定的键并创建新的列表
    e_books_name = []
    for docs_metadata in docs_metadata_list:
        new_item = {
            "diocoDocId": docs_metadata.get("diocoDocId"),
            "diocoDocName": docs_metadata.get("diocoDocName"),
            "pageCount": docs_metadata.get("pageCount")
        }
        e_books_name.append(new_item)

    return e_books_name


print(base_media_getMediaDocs())