import yaml
# from down_client import down_main
# from download_client import download_main
from combine_client import download_main, down_main

def load_config():
    with open("config.yaml", "r", encoding='utf-8') as file:
        return yaml.safe_load(file)


def pail_mo():
    CONFIG = load_config()
    if CONFIG['settings']['schema'] == 'v1':
        for buck_dict in CONFIG['buckets']:
            buck_name = buck_dict['name']
            if '-' in buck_name:
                print(f'桶`{buck_name}` 不支持当前v1模式! 请更换其他模式')
                return
        down_main()

    elif CONFIG['settings']['schema'] == 'v2':
        for buck_dict in CONFIG['buckets']:
            buck_name = buck_dict['name']
            if '-' not in buck_name:
                print(f'桶`{buck_name}` 不支持当前v2模式! 请更换其他模式')
                return
        download_main()


if __name__ == '__main__':
    pail_mo()
