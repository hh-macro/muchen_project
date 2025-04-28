# -- coding: utf-8 --
# @Author: 胡H
# @File: duration_gain.py
# @Created: 2025/4/8 14:27
# @LastModified:
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:

import random
import time

import requests
import pandas as pd


def particular_dict(video_id, mold):
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Origin": "https://www.hulu.com",
        "Pragma": "no-cache",
        "Referer": "https://www.hulu.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    cookies = {
        "utag_main_v_id": "01960f330c9b0020a884c2525d6c0506f00b306700978",
        "utag_main_vapi_domain": "hulu.com",
        "s_fid": "50F7438D5864B2BB-3DEABEFBDCDD2D80",
        "_gcl_au": "1.1.1679973076.1744011727",
        "_scid": "wq-7AmYaPbNnaRi03EWJKQC0d4Byi5M1",
        "_ScCbts": "%5B%5D",
        "omg_meta_pixel_id": "undefined",
        "omg_tiktok_pixel_id": "",
        "omg_google_ads_advertiser_id": "",
        "s_cc": "true",
        "IR_gbd": "hulu.com",
        "_h_csrf_id": "ad8cd74d68e7db6c3d97ffd177d434cb34a250bf42d69f486f630d4514a47ee2",
        "_hulu_uid": "308800269",
        "_hulu_e_id": "5NyrQviwKj5OBKhx-t-okA",
        "_hulu_bluekai_hashed_uid": "da1a717b22f49272768f12c35c557a25",
        "_hulu_assignments": "eyJ2MSI6W3siZSI6MTg3NywidCI6NTk5MSwibiI6Imh1bHVfMjk3Nzlfd2VsY29tZXRvYXN0ZXJfY29udHJvbCJ9XX0%3D",
        "_hulu_dt": "HpQL_w7cb3HU0sfRkz%2FLK7PD6s8-ZncNentzS8Dsqi0QHIoJig--Ntqr_HAAp2wwED7a658ghaFkIDd3SiFFL4_P9MRXaH_lipdrpo2cji2HqbDBdjG8WPvfVvB0CcMHab7th%2FoW2dUlENw8YmNMQLW9w0fI0k7UaOgPbNy6qX0xe9MmWOdJlZXR3Nv3kiaaMrgBwekHZvG3BoDPPIW1DJc4ZbQsY%2FZDJwzri1r74J3d8gqj3PkHGpPCrUFYpv0Rd86P%2FTnoq%2FoVWnzoQhs0efpvEVMsnJQtBU4HEyO%2FvlfpNEDVcqwfm3V_48_BFsblBYjsyRyPAHLSI1tLP14oA3bTzZYYm58U5aSYedBHaoI%2FzpMn42bMpHH7SH3nInr8rGs8%2FkY8o%2F_zbb9j4B0tGTPAu9BD4HazIC6b6s1fHxrQlwUx1HT02SHtvIy0261687pRj6gFfmPd3j_qnsX5RUq5zuGwH3NLCAp1_h9Xco2LziKrFIrxUVoVdQrhoOCUlj4_70iLjW2AMAJGi3c%2FzrCQ8n64Dr8X11et3myyuo7jeVvo0GLbOh%2FPdun54TO7AhEBOKD5egtcPTsXpLGlUUAOTkOVl9byNm5TPJ8ENhbPq%2FWKQUbG0fvXHZcNTBZQAgq_9%2F%2Fz1d3c6PzgUBwnw2Kwq7TiaSueD4K6R9i3eAQkwcVHgwW9BRWE__rIwsgLMxBSDQb3BZZEaFIcl2%2F3k2BmVlyUMYgXMEZ3MZYm8br0ww88k8m28qrKvc1a%2FAVH1z62z5R2vOhdHcN_fkug1oJOn1BSsbndAkqD7p6ZboPwkOUxQv9uyCxUrAC8DNnegwFEBG3yy88JNbVLN5pDL72%2FDxv%2FtsVEsJ8ly%2FjdhXG8_8bUfMn9%2FB81F2SC1XMSewMFntLQmZJbEphUHoXTB%2FwQLZJtjqsEkiasOqMFd9MFV0shbxlmp02mbiccFOVECAgFUPGTsuJHp3_keHtCfWzg6we1TiQ0Dc4w9_5QRuipZXX_D_pYKkK%2FisUH6YOlgdPe9PTXmle6lDgeyB_Wx_Bo_sg63_LupK2Tf2oZFxjx7QA%2FLMMe9C%2FHl5RXCFWbAja5SLBB7fpwXHMxG4VFJnNnrfHENyI5Ca7C70yBZwPK%2FC7wozvY",
        "_hulu_pid": "308800269",
        "_hulu_pname": "jdgjf",
        "_hulu_is_p_kids": "0",
        "_hulu_pprotect": "1744085403470",
        "_persisted_HEM": "2eceeeea63a90a490806bf022d93cefbfdcc3cd925068f549859526f55fbc17e",
        "_customer_type": "",
        "guid": "4FF91FB79E7F8BF38C9945A390CE415B",
        "AMCVS_0A19F13A598372E90A495D62%40AdobeOrg": "1",
        "s_sq": "%5B%5BB%5D%5D",
        "_hulu_plid": "3146728",
        "_csrf_id": "85bcc5043a1257a0b25d1ae984f8e41c71494fba0e74462cd7665338cf8e478a",
        "_hulu_hbc": "1744100688282",
        "_hulu_pgid": "327163907",
        "_hulu_session": "1sPwBxXxgTfFp%2FetKupS7sNtKp0-%2FU8VcVJPATTt9%2FJOoxhV%2FA--K46dTafMlcW3KF1gVT5hSBLJPXjtWT28Z2RBFFAIr%2FFFNQL2WsfxmDj9ehV3KbGe8Bu7J2Xwi%2FHHqQEh%2F%2FdJEVQU_H1fJnlWf8KKxfoH5sCaH4lbDVFv6tvSMHXjBF0orzVAMbsw2YRgxveJyaJylENM9ffuTgT5Q5O72_6xVCpxRrkYRCY7MgYhlDPkpjN7tD_kY1LaPZFT03p6pd2w5Pajsf_UL%2F6fnZMHgKR%2FZrsNztB1T3oDgALH8bJgStmNmdRZv4SwzGpSS0toAG6_tbj50qvb0NlT28h%2FLIaz0OZswhobkyBWz81JbNWXcg2snPbExAYae6afzZHAfaXT8DF1eWrlXpQXw1BzzGeCqdiVGKbmjBQgGxsAYl0hRFuGExBDiyEdbL1oWJs3yRHGwcVat72rcxka6XWguFPEnvtMB4WTO%2F_HBs9d8OhBjCQ6dEZKyaudojOKePMzc8S7YjcIVi7sOF78INTM06MRFsBI0pIxphQkGFeTYq2zhuFIm_izBz4oIt9%2Fv6ca7SaksWE50YK9DX3h_lWNmSRY7MDPgR98H%2FW7lCNq%2FS1Cw0k2piM2ylsfA4BG32k%2FMTIZRg9v%2FfrrusgRqmkx4aMWCK5HdE42HhrVrQPhIuSVwY16aPegVHcUpP9H5%2FAcDwzeMi%2FdfQ4zdSxMvpxwJiJ2BqafrYD_x5SDmGu42NmvjvbHXzKxjSnlj9F3e1R%2FAcI_X%2FhnN1BrU7klq338zq0VhqIHriAJUSXLkyHS4ECv_RFg2BZoBvN5i3v711E0n_LBYC242_BbGvP6U%2FuIN8iLzvkNDbu6iLZcZckFTNX7fFqWkn7Ze8aaIacVCxaNMYQnvSwHRpgwstavbWEW30FO_hV7_oT3nQOJCnLcmZFxQStdAteYSl0wxcxDwIk2FRcM8EAcHuVZVWuzX4ElNs6Nzv70sP_G0iUiC1z85b2Y6F7IPID6ix_bgWSI98jp14fOt6V0zAFNhM%2FNcVrTxF4LcS7UhZmc53kykmDIv5QcQxEQhqk9FFc3RKeGC9e1qm1bO7McPCIhEekcWjQuHOT90a_5bWJ0Q3OJyOA7w3wYmEvKhCcMZtWMMBJ8m5JxudHDQ23%2FLsQPgDG2r1AIBONVnDkludCHKynU4g9bdvuCIGoVN5QliUgzoiTDF5n0W3JGAxCupF8AxWxUik%2Fb9zi9x%2FYeN4396Zd4vshXInAfP7f3Ot64NOUGkcJ8sQHGD05rPFNjQd%2FNszS8d%2Fesfu0fGNA%2FJSKvcKkDlPgoWt1zslBwZYE24sr_wTSYiWBvyjVJQtjrD9kncRPFwUnL92a6Uss-",
        "utag_main__sn": "4",
        "utag_main_ses_id": "1744100690648%3Bexp-session",
        "utag_main_trial_duration": "undefined%3Bexp-session",
        "utag_main_program_id": "undefined%3Bexp-session",
        "utag_main_hhid": "7c2ef8f2276ecf2f567526c78e4caf61289a7f952d203c3b9c668c791bbb0eb4%3Bexp-session",
        "utag_main_hpid": "7c2ef8f2276ecf2f567526c78e4caf61289a7f952d203c3b9c668c791bbb0eb4%3Bexp-session",
        "utag_main_g_sync_ran": "1%3Bexp-session",
        "utag_main_dc_visit": "4",
        "utag_main_dc_region": "ap-northeast-1%3Bexp-session",
        "utag_main__ss": "0%3Bexp-session",
        "utag_main__pn": "2%3Bexp-session",
        "utag_main_dc_event": "3%3Bexp-session",
        "_scid_r": "0y-7AmYaPbNnaRi03EWJKQC0d4Byi5M1lz2WnQ",
        "IR_9358": "1744100701867%7C0%7C1744100701867%7C%7C",
        "IR_PI": "7af6faca-142f-11f0-9435-5ffbfd75dfb6%7C1744100701867",
        "AMCV_0A19F13A598372E90A495D62%40AdobeOrg": "-408604571%7CMCIDTS%7C20187%7CMCMID%7C83656439723147414441464613219877569485%7CMCAAMLH-1744705502%7C11%7CMCAAMB-1744705502%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCCIDH%7C-1230288301%7CMCOPTOUT-1744107902s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.6.0",
        "utag_main__se": "12%3Bexp-session",
        "utag_main__st": "1744102760524%3Bexp-session",
        "utag_main__prevpage": "/watch/88673de7-17f4-4b53-b575-d444846dcfe8%3Bexp-1744104560546",
        "_hulu_metrics_context_v1_": "%7B%22cookie_session_guid%22%3A%222105e0778bf471da835ebe9fc62335fc%22%2C%22referrer_url%22%3A%22https%3A%2F%2Fwww.hulu.com%2Fhub%22%2C%22curr_page_uri%22%3A%221493c0af-32cd-4073-921d-3eebf29b132e%22%2C%22primary_ref_page_uri%22%3A%22app%3Awatch%22%2C%22secondary_ref_page_uri%22%3A%221493c0af-32cd-4073-921d-3eebf29b132e%22%2C%22curr_page_type%22%3A%22movie%22%2C%22primary_ref_page_type%22%3A%22watch%22%2C%22secondary_ref_page_type%22%3A%22movie%22%2C%22secondary_ref_click%22%3Anull%2C%22primary_ref_click%22%3A%22Pok%C3%A9mon%3A%20Zoroark%3A%20Master%20of%20Illusions%22%2C%22primary_ref_collection%22%3A%22vod_items%22%2C%22secondary_ref_collection%22%3Anull%2C%22primary_ref_collection_source%22%3A%22heimdall%22%2C%22secondary_ref_collection_source%22%3Anull%2C%22ref_collection_position%22%3A0%7D",
        "metrics_tracker_session_manager": "%7B%22session_id%22%3A%224FF91FB79E7F8BF38C9945A390CE415B-b20b03b7-74e1-4eaf-8861-8ced0d52c010%22%2C%22creation_time%22%3A1744100688271%2C%22visit_count%22%3A1%2C%22session_seq%22%3A146%2C%22idle_time%22%3A1744102264577%7D",
        "ak_bmsc": "1A5C81A63BDC8D3F1A43C8306F0323DD~000000000000000000000000000000~YAAQI05DF1A7bQuWAQAAHI+YFBsATzW/Vm5s8ckde9Y4xOSWnF8yAqj4XmLNUwKdX8z+ElPJtaFU9g2eP5zCEne6hUrVpS3zS7qc6tP8lRDoWuvQQSfFpx2XUruibsWmuWIFJOZKHD731kdtxwLuqVPgtmPHzf3BQ6X7LPnOEBrRULNZMINugeMvUspLro9Cy6YTjNrcs5kTRC+a2/YeyiGoCKlwzEYCiDTZZQMPSuqZT+a8GxlxDos93aMy4AvVHfRwk2PlgRU3krLLW/kHyxU8BeLxcEu2W16lCSOc0zF+EvtIIwFs8L2WDCFagqLjXi5gQ3NlAcqjbGxjxOiX/EIealNdaBlUMEBm4uwLneq3yGruOheDDloHmyI2wlNMJsqY2AJwgzmmfXvIjieK00Y4hntr5nqcf9Z4MCNgkVb/oTTsxprTZ5joEon45LZPb39Rd0DiJECliy3j",
        "bm_sv": "6CA14DAC615B134D91C1070D7D5A4DB3~YAAQI05DF1E7bQuWAQAAHI+YFBsscjEOc9v1FKYiF8YHt/0xT3qtOCDaprIWrkP/V19U+GSrKVuV9/cYFVXoa61E4I8HB9VFIWy6l97zfy2r9dt8ItouiBO2dkG/8fmORlcHQWYJeAllppU7BwMasVoACdVF8M264XTQ5Hlt+Pw3Y/tcHZ5upertpAgon2DE5VWJrDCi2mkP1Fhf94M1cV+vOgM4dvV6yEHsAQ95ZxpOpjd4T2EKY+mcqraYCEE=~1",
        "OptanonConsent": "isGpcEnabled=0&datestamp=Tue+Apr+08+2025+16%3A51%3A05+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202305.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=5b2387e2-903b-4d97-8f8f-298927dd5f24&interactionCount=1&landingPath=NotLandingPage&groups=SPD_BG%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false",
        "XSRF-TOKEN": "6c5ee853-7313-4a35-b6b7-0be9c079ba8f"
    }
    url = f"https://discover.hulu.com/content/v5/hubs/{mold}/{video_id}"
    params = {
        "schema": "1",
        "limit": "1999",
        "device_info": "web:4.14.0",
        "referralHost": "production",
        "cacheKey": "0.8213768414809826"
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    # print(response.status_code)
    # print(response.json())

    deta_di = response.json()

    # vod_items = details['vod_items']['focus']['entity']
    vod_items = deta_di.get('details', {}).get('vod_items', {}).get('focus', {}).get('entity', {})
    bundle = vod_items['bundle']
    components = deta_di.get('components', [])[0]

    if mold == 'series':
        collect_list = []  # 每一集的信息
        for ite_nums in components['items']:
            collect_list.extend(ite_nums['items'])
        all_duration = 0  # 总时长
        for collect_ in collect_list:
            duration = collect_['bundle']['duration']  # 每一集的时长
            all_duration += duration
        premiere_date = vod_items['premiere_date']  # 上映时间
        genre_names = vod_items['genre_names']  # 类型
        duration = bundle['duration']  # 平均时长

        print(duration, all_duration)
        duration = round(int(duration) / 60, 2)
        all_duration = round(int(all_duration) / 60, 2)
        return {
            'a': video_id,  # 视频id
            'premiere_date': premiere_date,  # 上映时间
            'duration': duration,  # 平均时长
            'all_duration': all_duration,  # 总时长
            'collect_len': len(collect_list),  # 总集数
            'genre_names': ','.join(genre_names),  # 类型
        }

    elif mold == 'movie':
        premiere_date = vod_items['premiere_date']  # 上映时间
        genre_names = vod_items['genre_names']  # 类型
        duration = bundle['duration']  # 平均时长
        print(duration)
        duration = round(int(duration) / 60, 2)
        return {
            'a': video_id,  # 视频id
            'premiere_date': premiere_date,  # 上映时间
            'duration': duration,  # 平均时长
            'all_duration': duration,  # 总时长
            'collect_len': 1,  # 总集数
            'genre_names': ','.join(genre_names),  # 类型
        }


def excel_new_table(new_tabe, mold):
    df = pd.read_excel(f'compilations/{new_tabe}')

    new_rows = []

    for index, row in df.iterrows():
        aria_label = row['aria_label']  # 视频名
        href = row['href']  # 视频链接
        video_id = href[href.rfind('/') + 1:]
        try:
            content_dict = particular_dict(video_id, mold)  #
            print(f'视频 {aria_label}\t--------修改成功')
        except Exception as e:
            print(f'当前视频{aria_label}\t 出现错误\t----{e}')
            content_dict = {
                'a': '',  # 视频id
                'premiere_date': '',  # 上映时间
                'duration': '',  # 平均时长
                'all_duration': '',  # 总时长
                'collect_len': '',  # 总集数
                'genre_names': '',  # 类型
            }

        time.sleep(random.uniform(0.65, 3.2))

        premiere_date = content_dict['premiere_date']  # 上映时间
        duration = content_dict['duration']  # 时长
        all_duration = content_dict['all_duration']  # 总时长
        collect_len = content_dict['collect_len']  # 总集数
        genre_names = content_dict['genre_names']  # 类型
        a = content_dict['a']  # 类型
        # 将内容添加到新表格找哦给你

        new_rows.append({
            'id': video_id,  # 视频id
            'url': href,  # 链接
            '名称': aria_label,  # 视频名
            '总时长/分': all_duration,  # 总时长
            '平均时长/分': duration,  # 平均时长
            '类型': genre_names,  # 类型
            '总集数(多季)': collect_len,  # 总集数
            '上映时间': premiere_date,  # 上映时间
        })
        # print(f'视频 {aria_label}\t----修改成功')

    # 将列表转换为DataFrame
    new_df = pd.DataFrame(new_rows)
    new_df.to_excel(f'compilations/新_{new_tabe}', index=False)
    print("新表保存成功！")


if __name__ == '__main__':
    # series --> 表四电视
    # movie  --> 表示电影
    excel_new_table(new_tabe='动漫电影-A-Z视图.xlsx', mold='movie')
