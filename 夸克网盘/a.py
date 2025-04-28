import requests

cookies = {
    'b-user-id': '3963cc74-403e-73fc-fe9f-029e48125b2d',
    '__sdid': 'AARazJXMAUglGskYi1596EgMnX+jGCCE51bqANh7gUHCwr2d5y3KOANVOs4kJIHQ1Sk=',
    '_UP_A4A_11_': 'wb9c71463ba64e94b75c87558eb0870a',
    '_UP_335_2B_': '1',
    'xlly_s': '1',
    '_UP_D_': 'pc',
    '_UP_30C_6A_': 'st9c86201354ddbverp6b6aff1410hvn',
    '_UP_TS_': 'sg196268b94d7a412900c8d16e86a2d2041',
    '_UP_E37_B7_': 'sg196268b94d7a412900c8d16e86a2d2041',
    '_UP_TG_': 'st9c86201354ddbverp6b6aff1410hvn',
    '__pus': 'eecfd66337f075d573e9be2b28ab70a8AAQDjwjlQAcmDt+WFKl48m9z2LbH7adtPml8lXxnhNHXOEoBlG/j2++kJVMbyAXlzU2lYbhfCMe4qL4uSkWXE71c',
    '__kp': 'db156ed0-0ec0-11f0-a381-b528800c0cc1',
    '__kps': 'AAS69MQ6vidCfKvzYnJlzHLM',
    '__ktd': 'OcBRN2TiWpoA16YyqKvhGQ==',
    '__uid': 'AAS69MQ6vidCfKvzYnJlzHLM',
    '__puus': '57078289d7bf3596bd416590bcece18fAASgTMMQZo3TW2UUsqlLQKRbovoVtTxU2e4fospvsgSL+F8EVBNcUWfDZ+DpKW8fRsMR3iwZGwZPTT2g26mWHLaHp/mt4ZIGLMtkSWvUngCyMu9RX7AaeqyneoMWzbuhOTl2uiqkxDOworYHw+BfplAkqVN2qazPIq1g33Uc3lnllLnUvgqBW0SEbTjjwXB3vqCeIeNmuV+02ZYjUN8j1/Cp',
    'tfstk': 'gywtUSvHxwbgQHklIO1Hn1a8WSShX-EaJPrWnq0MGyUL0rhmGfmiHjas-RcmCV4Kd0nJfEGfgeiYrznbCAacHqZr8d4c_jvvbJUJndbN_o9xnx_lrTXubCkqhacDkjZW_0oSftcjhAkQsHlFtTXubltifgqCERVt1ogslxGsGkgI8cnshKO1v2ix4IT_lxsdvmmWfKi6h9TI00MjlrMfvkgEcbLhk2tsoKF5VWrbo3QG3tyKXf3vn2pvDims64ZsJa_7pOhtPlgpha5S4U0x88_h9kz81PmUkTQKF7zLHbMABUoTOuHISY1J9AE378H_eNpixvuiNSGdfOZKBVhrvbtD_AFb7-ha6nSzAAaUa4l1TwoLI8cxzXLC5kqK5bFYSwJjS7EQJb2H-LD7ayexNYsyA828Zy8oymA1vMd2gfieLMNinaDXZqnKrGBvgIlFYD3lvMd2gfiEv4jOWIRqTM5..',
    'isg': 'BL6-4BvPVYS1QIGUlsgXxwPuD9QA_4J55lnRBWjHGoH8C1_l0I5rifDjh9fHM3qR',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'origin': 'https://pan.quark.cn',
    'priority': 'u=1, i',
    'referer': 'https://pan.quark.cn/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',

    'cookie': 'b-user-id=3963cc74-403e-73fc-fe9f-029e48125b2d; __sdid=AARazJXMAUglGskYi1596EgMnX+jGCCE51bqANh7gUHCwr2d5y3KOANVOs4kJIHQ1Sk=; _UP_A4A_11_=wb9c71463ba64e94b75c87558eb0870a; _UP_335_2B_=1; xlly_s=1; _UP_D_=pc; _UP_30C_6A_=st9c86201354ddbverp6b6aff1410hvn; _UP_TS_=sg196268b94d7a412900c8d16e86a2d2041; _UP_E37_B7_=sg196268b94d7a412900c8d16e86a2d2041; _UP_TG_=st9c86201354ddbverp6b6aff1410hvn; __pus=eecfd66337f075d573e9be2b28ab70a8AAQDjwjlQAcmDt+WFKl48m9z2LbH7adtPml8lXxnhNHXOEoBlG/j2++kJVMbyAXlzU2lYbhfCMe4qL4uSkWXE71c; __kp=db156ed0-0ec0-11f0-a381-b528800c0cc1; __kps=AAS69MQ6vidCfKvzYnJlzHLM; __ktd=OcBRN2TiWpoA16YyqKvhGQ==; __uid=AAS69MQ6vidCfKvzYnJlzHLM; __puus=57078289d7bf3596bd416590bcece18fAASgTMMQZo3TW2UUsqlLQKRbovoVtTxU2e4fospvsgSL+F8EVBNcUWfDZ+DpKW8fRsMR3iwZGwZPTT2g26mWHLaHp/mt4ZIGLMtkSWvUngCyMu9RX7AaeqyneoMWzbuhOTl2uiqkxDOworYHw+BfplAkqVN2qazPIq1g33Uc3lnllLnUvgqBW0SEbTjjwXB3vqCeIeNmuV+02ZYjUN8j1/Cp; tfstk=gywtUSvHxwbgQHklIO1Hn1a8WSShX-EaJPrWnq0MGyUL0rhmGfmiHjas-RcmCV4Kd0nJfEGfgeiYrznbCAacHqZr8d4c_jvvbJUJndbN_o9xnx_lrTXubCkqhacDkjZW_0oSftcjhAkQsHlFtTXubltifgqCERVt1ogslxGsGkgI8cnshKO1v2ix4IT_lxsdvmmWfKi6h9TI00MjlrMfvkgEcbLhk2tsoKF5VWrbo3QG3tyKXf3vn2pvDims64ZsJa_7pOhtPlgpha5S4U0x88_h9kz81PmUkTQKF7zLHbMABUoTOuHISY1J9AE378H_eNpixvuiNSGdfOZKBVhrvbtD_AFb7-ha6nSzAAaUa4l1TwoLI8cxzXLC5kqK5bFYSwJjS7EQJb2H-LD7ayexNYsyA828Zy8oymA1vMd2gfieLMNinaDXZqnKrGBvgIlFYD3lvMd2gfiEv4jOWIRqTM5..; isg=BL6-4BvPVYS1QIGUlsgXxwPuD9QA_4J55lnRBWjHGoH8C1_l0I5rifDjh9fHM3qR'}

response = requests.get(
    'https://drive-pc.quark.cn/1/clouddrive/file/search?pr=ucpro&fr=pc&uc_param_str=&q=MP4&_page=1&_size=50&_fetch_total=1&_sort=file_type:desc,updated_at:desc&_is_hl=1',
    headers=headers,
)
print(response)
