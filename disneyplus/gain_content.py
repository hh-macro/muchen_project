# -- coding: utf-8 --
# @Author: 胡H
# @File: gain_content.py
# @Created: 2025/4/9 14:27
# @LastModified: 
# Copyright (c) 2025 by 胡H, All Rights Reserved.
# @desc:

import random
import time

import requests
import pandas as pd


def get_particular_list(season_id):
    headers = {
        'accept': 'application/json',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
        'authorization': 'Bearer eyJ6aXAiOiJERUYiLCJraWQiOiJ0Vy10M2ZQUTJEN2Q0YlBWTU1rSkd4dkJlZ0ZXQkdXek5KcFFtOGRJMWYwIiwiY3R5IjoiSldUIiwiZW5jIjoiQzIwUCIsImFsZyI6ImRpciJ9..lbMIhreyVyzC9q2K.fA7PIBZnc1TtlzQm-tlEven-U5inachp-pN93esD_xAdkujC1QJ24zJa7Jhos2oPRLxnuQNWu9d4wLVYcptjZcughH_puyXqnj2P_1aWDZh6z0g9XGXDjyM1IhwMfUmHECJGjnM5UZB1J-sKaIb6B9PUPq_OnTdBwzHv4o6_JuMackErIOmut-57mjnCJPrs0YaiJvKsk0p1mSAytjxQW8I4LftA01whdG1hcmMzfmCNiawrqshiQIh8Sq-WidXQNiirI0VaS6ah5PtQ_zCK7igxqioYUaUfHTErZpB4Q79x0LzGksb8v23_p2MKHF8rp3U7bq5nV2EUgbaqO1LWWuu3jHuu0iid2gYOgfFP0uMfRdlVadlwwcrygCUUg8c-qUaPb1QOKKZwLnzpSGOtaOuadi-KdofqI5_id9KYXv9S7e5xGCbfHp6AexJdYZ3-0dp8QkSqvZuGkIz2nMS20DgfpyASUoLGl_Z3OfbkW221j7KAVPzTEDf57d6StAqjHPkG2og590YtsdcO4Rz53FQwmOaRHSpoPch11Hjjkb1PZvac1Kk2SODQ1RD9vJfdTAnRqetxlU9WuVsXb8D0VFEUBF1p1p82RkboUhHJXgf76ZfCirG99oaFfMaqAweG1l6lncqBsm5W9RAsKGYuFApdi9wkQf7UvMjdOg7vKquJMLUl-69x-yjzNohBuB08c6K9_WT3CuQUVh5mheWfWQ9MeicSIkV2IMhMQRiV-DecS-pkZdSA2HfPHktbs1lXO4OrGCUtjfxmlFoFUnz4cNK7RlKPa7hPv4jrJOKEOMourYyHyQsov_bm1R8eAApz4tQS9MvQWLWODFrUxeFsZu0tODiYnPFrty7JPwqY9R6wMCKmFe8a6CT65s8CFrBubo4NaE3i6CpYejBLsYNBnSlWPnDtoXAioiHDewpS43_77nOo1zo4HpiJLMIsv9gMJ2TL6Ww6EJ-gRfzd0nbpzYqa-1Suk-Yorki0mXvSNZgHPUwdyZSVxTQhj9T503RaWNKwbdFbAdPk99awOhFewhH4pWEFbRxKeYoGtWIOGx4Lr9NtxDNsel6q3ylMuV61maewBK1zflOwaMNizVNVIGppxXJNgdPzMKKFi2rQkZc15ClSgd_biJ_PRZIVXRayLSmZSGp0PR1lxT5CElDz3vS1td92wuL7hM3EuBjOIk2qB6oZ9sj5DHHkuMKEETVdQnjT65N5sY2sgE0Na3h2UdxupqsvLGy0PhgozVhEgyN3Z1kvKYs64ZTlR5BmTMV-p8JxFIHyR9oV8x9KUKvBOVOM2wah1vP2mTASeo6n67vvt4PFd5RYrhcKzeL0QBK414qkeoHPiZydvRlLWIRjljM0Aeqwm0c1Y7sxmHxkBt-X3D79rS_Xu-C6wJlSX4_ScsLr_8O7DkwJqP4yJTMg-9Kit1Ad-C-BgdIROYdeg6cTziJqr1rM_Vs5BTMPvBwM3ifELFIB5715bKNZFpwmni6UofT2-qQu0hRgX8Rz9VCJEfHAcsx0pyZfkdTiNEWfmfWf04Vhm45-nbSbrrX4qNi_FCjTFXvjcQDWjwWB6VVXb_H8ar6kw0ZgnQfzgtLxlDqBiv60Tl-ydF1aHW8NV1T7fJbmKtZaMcBe5n3IYidKVr-QdBXkoAUQo_oiA1lfUS_t3kqPQI9_x4brxm5hMJZJrTGz_m_0Q70IqhXzaSQNC3oXuAEXVHv7GeHZdL7hnRXnPhnd7V9MxFbaamIrfXSnvDm0ZbqdgKtEZbqFcSRymgtYOODV4tBT2Zaa96h6IvhYZfDbz0-yhvpy2XABMTQF4xTkuCAMXnt_Pyp7mzBwII8IgKxjrPTjm3Gt0ocChuMH-GO5t_CfNHVMZ86SKzT_TJ8zbMi8F_AK_jSEDHjJKs26ZeP5x514m5R5_MR-UjCsUz6zEIJlRBmc9NntBNLDceYXVLmMHWvDP745mBkw0sCCAhSs2S5MeaCrLNnBjdz9GCCjnEfJJrnUjXoRM_9LnLmP1XVaeeV5jXVlgvEnnvMHcvJ1w7sru83fVfSVnAcaG9R_3i_wItcGem0kbfi08BGw_J-aghZiTwO5P_Tndiqv4JILIp9_hHruPYxbeTPQQSx6Okt1f2ywmCggxVT6DqlSvRiL-NRY7nz0AVIDN-nQE1XID3Dbvw7lWqta1jW6YN3od8FgAHFpsrg25WAXmdRUlxl97Uciy2jX50YLxAix8z3q1qJ0ToTjnu3MA4PtOgfZW0OoB5jJzbWczZi3OAn6n4Bf_Ae9bwlFQjgL5SohvbLK8HWaeb2u_89pKho5XwsiQ5ZcgUZVKMpQtX0onysIEzrDtqkNjR0imaEkKC_h6yGDfP2xj9l3AnkrII5oYjJ97y9q5k0ybzp7rJQ_MkwcoQRB3IUIci60yLOMbQgRf9pkWlFGeiV_Vosqe2xUNHUnyu6k4Z4OZXXHFzDrtTGaWySP52gm_3cXiDo6ZBT9OhqraIgYWYGfR12G8qk4YqzvIqIrXJFBfEcxqpFRBAeUPOIOlyHm9GE-XrhBNDAnUckBHoJt1u_18wZsDphfkgio2um28_qklnTho1IPtJxak-WOFlnxKiDWePY0tHR8A_G2ORrnkoeuoxj7j90__kuGSul4PPXQMk_VUS3_1rJb89-uLaYH49rlj-AtqtBUvKrSXLJrwQORjGb9883tArLi631IULw2D7mlT662UQBtXqeiILvPMSLroQ2olOWmqq7-pwnAWq5UdfpnvtmIn_xRiuoUhPJfIv8QrXAHLccswsDhqEiSfHWGetLuoYSdcXk2I3Vu1AAI2ypslXn4tT5WU58GO9YIVR8gCp0wCmylWybhs_uwzeaqcLKV11BQSX_15e_KZUwnKu2ogoTgPyk-sgd5uBq6yuQfFqq7w7LjxnX0c2v_xy8DWi4-GXnrBttIkQL2LLYLI-1L9Nko_bVolEskroTkcvHgd4JHo-Bs_FEe4SHxaqBrWR8PcO9YVABV_7Ol9K7hCHuFgLnMBPpkm5d2AMtSJsFE2niYXSS3jzwFYC4RWSvCB0ka-WDNqE5jXtBTRSqNmBR0A-5ljiOy81eE9Vi-zLa1xatLF68IiqNoeLrGQF0S2-jomNWir01Fp9eadSLKr8Ihjo1FTgGp_YHLznA36dO6bTb420E-AV90cf6yglwE0p4bewWgRRnmacpCs4EMFiej1DuiFCjmtU9NdqDjGZEov2XDwuj7WBiWtz2DZyA8fDkN3aWnx0VMBvcoRxE_IPdHjmvWPhW10XdWog18QOrz6JS-RyBZXnPw-5H5YepqPDaNkwoIWlfEOtQS7j2eYkIpCSdRaoOHXOFPd14CZN-q7vOQnvIZVnUM0vpR-gcZXXmuXI0qTVYqcotmTaxx7-qCgLFeY_ZU8yJjGie_5uNUWS0jZwQeYxjAGwJNR6v8S0eKRylYeiR28SWPL9dBT2uCBIHDecloHUPdXyRPLTgadX8j-qpRq_-SiuneuBibBtnQw9hZNWDd_99UB9kH1GAhdZsi-gR6QsdGI0hT1BzQd9FCB_CCzdFxMfeNeZt-66cBCeQWfvG48RrRmyeqeHLMxk3hpv4oGvCs3XEPMrIKN0CW6uOvVHX17Kg7-jbSCVji_hoIvtLnAbupB032kaJ5OYY0k8UTd9izD2Ri-iZYt_JQ4pGWjYlv-rOM6AgCErGivuUAwsjA8eKt7Wt7iuo4KOetmwKFjUapsrJNWJOcUUctjM7jynJL0Aipkhcnl_TFp0xooc7jT281lhkhLmJlCv0WetJ7rOscsaIphzipf4cu_jstMHL_XvLoPuc27D-aM2NbIXOC9NtS4RxfJdVorrsT0pmtjFEClLU_j4ExJUUaKIN5r_5SoDemO-bRVZPiNbqFmg2sy-cLIFIbxqU6TOJYw3uoRj6Ka32NbOi6PE-UnmEC2zPLC8Up8ohZlMXe-kV72PGx63HLKZrFwMS-CGnI5w8gIxJfyuaRqQJ2hy6zattAbbczGlCbWwGvl-RWoLbGwg1iuvMEDZZN9oYJMXkfG9Bs07JmvvgH5AG139ScDpM5VYgIF5HaF-utBrpvKHUujafnijm2tyMzGLukYMZn2oa57w389GPiZPD7HOuks1ggmQGZmXC-pXUKvxeXg1uj39WUhY76LMm7Nlvq2qMvwbrPSeT7jc1KGitEkSHpQ3jWIZIJtPrMbAVmx7nREz2l5BOKIYbXDLhMskrSfSN1_n0KsLOqrR4FttBrAd4zsC0Td7T8K_3hBuxH4IJEp18YqN4TP7N1O_4vU_k20Wu8yU8QynOvQZGIfHK7rLgoFpzPzr9Wo1c-T2dVLEEOg_914uDeFREhOOjkKdgpUkhvQo-ooUwsWsesarF7g9aHmIPNOcbm9mi7NSPjBKNTbgZq-p3Ac7cwBxdOxsS38Q1pfO6T0tn-Fiu1yb7aEJUL6BRAVdPcUcdrPxyOp-5y3JYy5DaRDEiQAf4O277--rub9Gt-7db4aSunI0SDpgeRtXB4zlJyBU83_i_uefRMDKut00Tw02ZckP8inagNP0b0ZCI08Cl738gdAq82X7IAqq8FfBqqIKG-50LDADaiJpD538lY9JcPxUthlAKcdMaJOmHYcktcaYIq1usU8Xv9Dn9tZIv1K5yTk7_493CpaB31wJxJgLGAe9j1d-VgSmHDh5io7o37I6XzNXRalkLIcE5ThbZ12g6v1NjjIVvytG2mYN3sMuOLff14hwJqLMTe4X6f4F24_U2gJSqwn4H3ELGr4WTvx8jckNqfrg31A_g7sDd0YajbupGJNG30dR6f7U6CRL3dZCNqcAPUG8igWLBH5ftnQaq14tw-Uo_4PvlKyLRlBFN22xhpi7ighl50.46ELiF4ltU1EoLIcfjXJpQ',
        'cache-control': 'no-cache',
        'origin': 'https://www.disneyplus.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.disneyplus.com/',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'x-application-version': '1.1.2',
        'x-bamsdk-client-id': 'disney-svod-3d9324fc',
        'x-bamsdk-platform': 'javascript/windows/chrome',
        'x-bamsdk-version': '32.5',
        'x-dss-edge-accept': 'vnd.dss.edge+json; version=2',
        'x-request-id': '17b9afca-8e30-4173-9c0a-48782f8e0a64',
    }

    params = {
        'limit': '15',
        'offset': '0',
    }

    response = requests.get(
        f'https://disney.api.edge.bamgrid.com/explore/v1.9/season/{season_id}',
        params=params,
        headers=headers,
    )
    # print(f'https://disney.api.edge.bamgrid.com/explore/v1.9/season/{season_id}')
    data_dc = response.json()
    # print(data_dc)
    season_items = data_dc['data']['season']['items']
    return season_items


def particular_dict(video_id, mold):
    headers = {
        "accept": "application/json",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
        "authorization": "Bearer eyJ6aXAiOiJERUYiLCJraWQiOiJ0Vy10M2ZQUTJEN2Q0YlBWTU1rSkd4dkJlZ0ZXQkdXek5KcFFtOGRJMWYwIiwiY3R5IjoiSldUIiwiZW5jIjoiQzIwUCIsImFsZyI6ImRpciJ9..iazOH5UG2c7oyxtB.p00iUeTs1MR3Z0vmMNMu0P96vTEMBDSa6-gysnvg-5ACWYDcyEDfgI_ZxTaFmRgSnWDRFP-tvZ-C5qFHkDR3YQJESGuUG17ldscEmjULxozpz1j0CoaISpTmR12xPbRPfoSnn7ZXA2_FGbvCDxcDeab1_M5wADN2_FoklXVQOOrOA85-F-RrU3R6-FTbj_B5smU7_ZCjqCne52QQXgtI_TFKXKUTlCGdgKhnFj8ILaXH8XUuObokguoi5qzugcypPB9rbj_Lw8UepdWYrFSx4W7au5-c8va4j_uHpSp5hmRqHZTTvGOSb4c4IF0mVn6HUv8U2wyzOsSfUU4X1yZTViwhgWGKxt4jFrr01Oh4K8gp7zzfb9EAr7Itkhq0sCVTD-EKj2igC7w81IJVleSttEVIvBfZZAXPnFq1FQvlcjuJkdtVvNNDW06K7aNrPS9zl7QkXyTf-rPfP5cSEq2saFd6sSmTLbtqBfyRhlEfrIP4LWUD5pZpytJN2D_fxje2UHbzlBGkuAVg07rTY84jsWOOanuipeUOR54oc6iIK898Sz7Zc3iEt8dZLvvaGreBKGpjLo6ep4MyTwDPTCosonOdCAYMIIjGaubrG0u5wSu5hmcd_QlCC1Fhea-AjT3URFCw7aj1tHPzCU8p9bX5cNrWh1UQ8QV3Qm3QuTJhsarViv0FsxzuOH1taDSlVm80kWGRDJzBtTwxrxjYKda8TY4VtVfxxEsDMv0JAjmFouW1dwzHT5NNvlSOZ4C7pmgZG3NLUag3HLYDj5p9QBjmp33MBF24xS2NaCHaSuYj4Ae0inKcFgtbIQUCXtdSrM_06CqdUu8Xo5pPgVuv-2khky6jkoC3nzpRQSIcqYC_Ct2XHg9ydOP8YTJMbcD1ApFf6yKUHQWWHG5MVqliBx-AE1QZ4jc3fCswl7rGJfPUORAoTExz1ELeQedPX-_tJl6lJ-Ev4vCReMp-qX1pLifKCKI9WyfZmcFaAyZ_UkIyCYI2LpyavlmZF_wt1WaQ5RttD9BmBtWlbJJdwHpSR9X-JO0brP2SbD78tvxOybxMgjkNTczmY-mnJbNuAdcgb58OoH_ni5-KDAv32J977bikTdJe1QoMmBs6VUiJpfZcciZ4q6BTHXsg8GtBb07GuWwIe8DZrCbagf2y0wj7LgwBz3DxIlhPcyl3fCSX9aBnTZgJ-ZCySFtPHu0BXe1-Pk7HYP2SNqdBk0hMeKL0FVpOzhZpmI56PX7QvqqL29y7ec9BlIdoYM9tm3kxL68_IWsgQoNv15o7zLTzLrz6yVay0AyIR5tgo9htRmy0SKc_lmouh9_8S7T60nAQIgf_u4ejz1UmLBGFBU1BgXNLJ8dfPvYN0-hxB_eRjh16DFNzIVB2aDXD-8dZzaq2SwdKuFCy357D4Rn1yu2YtZjLdODiecairK9DmK-3HUBeFTh3Tx_FOOkU2U_7izOqikLoRHriSJyFyc2otqySca6xv-ciE5YoGeiOXjPRtsCD0dB9MbKkDPhMDJ4T_8u1tKPPwKQtZ1WhUaTnYVFogo7FbkQ46bbIFnYWp746V-Zob81_omP3D0C-ZTqWkLz2SMKCLznDtffK5Nl50bQrIzClUZDSVAUNBHdDeVo48XmzPuNZ9faTgryYgu281WxLx92kVXgtwKQaUQMDh8vGvd8_Kofgr6ick2kWca-RLAURJniegnFQvCJR0821PIK5XSD4X7caD9gwlFw9u_S_Zc3pNZTky1f_7J-lxTjRz-FxPYrZgPvjUzQfrKTFAS1014xRp_aM6roho5IebAx5vdkjbM4zbXw1p9srf5lMEKUhyPPFifSuKe2Gdf-tssueyNa8zJ9rvpb6I3n5Vb_GkJFKmBQ7gPPpBdDZxUcxZu13Lr71texZKH-atjgZ9YTj3dICmb5j3XIAPTPOewTMs1h8RUGVYXQZI_V0LfCigtLX7sdhAB6qCFj4AfgyjuilesxuKB7uCKDpuA5g3GVOpqymBXrA6hSyJu-Hj-k_Ff-Vw6qYx6HeNmk1RTjX3lqMf-iEFzRVs3R0-Y0qTo7Je_D9COlbnWjHRMEIfJ3j9hGAw1fkiTTHsfCvsqBOEJm-ifEEP8peFbcFF9vKZQbRX3Dy9bvNZakYTlMk0-vrsvrw7GNtPOSfeQt5f7jLct8jQcYpoI7KBX1TneIsesHt3NAvenpma_BsM5Fn6--JnLGuNFawCsU0P6thkVhOQYnJc0N-x_v3EyaI2e2JFQYJXRuu89SkoXGj6tPSZV3LZhCdjt4yG-viA_aeZXd77jpGPOZrzTxufsXePXjUpGlsablgkvCQ-TOZkUhsc_ld3NzPCU7Q1pFYxrhqcRpREbELgqPbjB1qyOpsJNLUR71S6sAjb5ygw2hmXE5Bj2Vm38eWfAyyG08IfWBVbfSd3IBjppuFqaoj1y9MsSlqgLmPDXqWUgHKU9dTBgJ_1vjFpJoJiSrAzLEmAN1B-qPvXYEBeKMhOcJXmgX-QthNVSVDa8h_zlBocWxDqch1zcoxtGi8nXvUUi0NVdQrdHcGONSQ3GKOLByeZymZo0XQtiv3kkx-oEmCTZm1QJtQNLFyeLNsVzdgRKwtbueC7VIGM4sC3R6Sib8K0-OZlik6ycYupI8ozBAp3vJOZ-F9wFQ-5Pm1VuzdJdmCmsONL5f36E0LaTarbD6UO9dLo2D3PDlNYrL6g9NOKBzSGW_iSZ3Y1iD86kRKzBs0Cl1SWL_3rp7mtYMnVcu8AtI-GZ1n28MtytOmE7M9mPAW4tKxUhtSr1aE8288WLgLmNtlX-cnJjhc9dO3YYS1KQxnKu-L3Ek46REOq26T1uoIA-MGa3bcOd7JdGeEzI2pfQiM7lthrmtljDYazY__h6h2et5S2yD6wVkRkcZ7RlLWH2ci0Yl3E86SY7nD_YkJs40tW5tuOdLPIGeHffU56SmxHoW9Z10N9x3ViwYMSYb7b9CcxIarrkUPzE59KmoHHt3jcwYIgJxZS__QWjDPdMKEV3cUMexjkuQRRFmg9m1NhqMgreHrUHlVfJ7g3jV0tEPaqU5kG20TiEvXeIkZWO4I4BkVxRntbC337eXCXP1B4p-uvV4wutFno7yVWeKPuCLNCNn-7Iw8c30yohemfM4MW3L0JzlWOe_OvrxVGsBLz_cZLFEp0gFilJRuRmRb-slaR-2PlIsxT6nmoimRr8jv0Y6xna0eYbpNHiN5OwXudReLNXpNr0GYg3XQc1cSrv4cLUIZu6-J5pUT1YFa6PGooP5YipLgxbwm3jRRy9mjIcom6DElVfceddjAJ0i0qfnJPLfxhtiEIf4Bcy3yjwPzx_pU54K7y_cCJprZ1pirx6pMAMebwCXo4M9XkClr_U_KJoDCqrpf-9lCXE6mfGFfN_5Y6HIdFInFq1yA2-aZLWE4BI4w8Hbu2TV7tIYbyIL0ARskd2ae8vcToQ7-ozs6il6mabz0BLp6dGLvdbwMNHUIAfoEnhjdukp2qwoLOUCShYUa0mp-5U_lTHC96Lw3aQxCvK_QzZktMrszH5fVIQtQdyEvr_QkUOCogENQCW7FWQgLswnyfMuh2pKUax9-9DQoEARCRESyaaItIC5Vu6LTKal8L10bbVaIRdI3HKxiDmIz4KnD6IEuQzVVreX_lHchwvkLf7LjEchHsN7VJWAFg2cvQcNkBYR5vFDygsF6gigxj5AdCp_wAIaJ1saogy7cbvH82CPtHFfTz2sQdeC1bLHppoA8Tstxm6CfVC9u99V55TAajdRtTQfJwMbiNIMyfujzSi5T5xJ8MuBwae9TQbUwiWbz-MkDfQhPWgmqGfVUt4rjsGUpID-BtRdmiYwcY_dja19LndsOOOWrVKo00U2i8djKv_8zJGD9jd6LNtbEvBLETPIMQ_lOtk-oad_1pR2TINrQAUeOeLbqMVFRAKEJZKFoc4PwzlTiCTWM-zY9-3VE5Od4lWxB6mzdpeBCyGdYyrGJKFabxUlnRf2_333XEbASoVhd3SRrD8lg7KthE3aZVCX8bBWqG1OfqV_4G8ncDRxfKPHMGY-oNFDWtV1FZN-XV9aYZ8DYBYUiY20rtMqL1Gzaggu1VkFcxQpRZyr31Y6MWg_Wv54C5yAHNgydXEuDQcwhPJ2DXtklDX3xWhYP-SJgZ6FiK77m7U_TZZxHE4hp6Yyj45KTO_VOlEMj4Fl_aaSK6JuOgBnhIT5qFXTUYh8xIvlVTSY4nfbRUjN5PR8jgs539M2B12Sg4OAR7xPHH4VlWep9RuEs1Vyns85hlHVCDU3mMC5WwF1MorCMYQYXymYshklqyhLmGqjCfJuBiEFTB0hmEpmaT1FoCGKEU-nhhdxbAhFB-qk8G1FVwTimaLX3NQgIphHZjemcMUcyHYOVKO2jTy780YFLn5udyJKSJRcIFpHm1LRqytXdTNCWSig2ktH-MomquTn6Lj6u_zXgJ-ySMTFNCEI-fuLZzR5LD88O4R1IBwIAqyn5jk6LLWZTuZsRglJR8Qg9OnQ4OWMLfDWiFLltlT4fluWUV1m9MxyNKGFOCxKuk6gkpKjY-1LQJedmRz5JVIujpAMSiVGQVTAGfvbQ-g1dYZceYOX2GrYr8roop9jPBqlk-3liGH2f9FC9phEgN6XS4HlpKDOME6iVIMjCI2XhTZmyJ-6ZAqx_PV_zwv-6DHViD5sF3vwgPyTD-22yUujnbGC2ND9k30xgt3yqbXFfGrjbVGoG8sbBqSLyPPiktE1NSci_-z32mYbQ58euXdOCzimgGAGy0pw3xkegIKApCeIRqWdq1_aJEqb2dB-TilhoHBx5nXJ1sEFStICsM_vrhGMNFlWb-cNDCP7543cp9EVCZLYRlRKt24Fo1w.pbBAPr_c1fsSvwhJUL5Pdw",
        "cache-control": "no-cache",
        "origin": "https://www.disneyplus.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.disneyplus.com/",
        "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "x-application-version": "1.1.2",
        "x-bamsdk-client-id": "disney-svod-3d9324fc",
        "x-bamsdk-platform": "javascript/windows/chrome",
        "x-bamsdk-version": "32.5",
        "x-dss-edge-accept": "vnd.dss.edge+json; version=2",
        "x-request-id": "0496024c-b570-43d2-97f5-0e15f0af0f24"
    }

    params = {
        'disableSmartFocus': 'true',
        'enhancedContainersLimit': '15',
        'limit': '15',
    }

    response = requests.get(
        f"https://disney.api.edge.bamgrid.com/explore/v1.9/page/{video_id}",
        params=params,
        headers=headers,
    )

    deta_di = response.json()
    # print(deta_di)

    # vod_items = details['vod_items']['focus']['entity']
    containers = deta_di.get('data', {}).get('page', {}).get('containers', [])
    visuals = containers[-1]['visuals']

    startYear = visuals['releaseYearRange']['startYear']  # 发布日期,上映时间
    genres_values = visuals['genres']['values']  # 类型
    if mold == 'series':
        collect_list = []  # 每一集的信息
        seasons_list = containers[0]  # 每一季 列表
        # print('seasons_list:\t', seasons_list)
        for index, seasons in enumerate(seasons_list['seasons'], start=1):
            time.sleep(random.uniform(0.5, 2))
            print(f'当前第{index}季......')
            seasons_id = seasons['id']  # 季 id
            seasons_li = get_particular_list(seasons_id)
            # print(seasons_li)
            collect_list.extend(seasons_li)

        all_duration = 0  # 总时长
        for collect_ in collect_list:
            durati = collect_['visuals']['metastringParts']['runtime']['runtimeMs']  # 每一集的时长
            all_duration += durati

        collect_len = len(collect_list)  # 总集数

        duration = all_duration / collect_len  # 平均时长

        print(duration, all_duration)
        duration = round(int(duration) / 60000, 2)
        all_duration = round(int(all_duration) / 60000, 2)
        return {
            'a': video_id,  # 视频id
            'premiere_date': startYear,  # 上映时间
            'duration': duration,  # 平均时长
            'all_duration': all_duration,  # 总时长
            'collect_len': len(collect_list),  # 总集数
            'genre_names': ','.join(genres_values),  # 类型
        }

    elif mold == 'movie':
        duration = visuals['duration']['runtimeMs']  # 时长
        duration = round(int(duration) / 60000, 2)
        return {
            'a': video_id,  # 视频id
            'premiere_date': startYear,  # 上映时间
            'duration': duration,  # 平均时长
            'all_duration': duration,  # 总时长
            'collect_len': 1,  # 总集数
            'genre_names': ','.join(genres_values),  # 类型
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
            print('-' * 40)
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
    excel_new_table(new_tabe='补充.xlsx', mold='series')
