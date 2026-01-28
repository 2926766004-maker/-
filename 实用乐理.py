#基础定义
GENYIN_BIAO = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5,
    'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
}

# 定义音名
def dinyi_yinming():
    jiben_yinming = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    start_midi, end_midi = 21, 108
    piano_keys = {}
    for yingao in range(start_midi, end_midi + 1):
        yinming_id = yingao % 12
        xiabiao = (yingao // 12) - 1
        note_name = f"{jiben_yinming[yinming_id]}{xiabiao}"
        piano_keys[note_name] = yingao
    return piano_keys


#音程的定义与生成
def dingyi_yincheng():
    return {
        0: "纯一度 (Perfect Unison)", 1: "小二度 (Minor 2nd)", 2: "大二度 (Major 2nd)",
        3: "小三度 (Minor 3rd)", 4: "大三度 (Major 3rd)", 5: "纯四度 (Perfect 4th)",
        6: "增四度/减五度 (Tritone)", 7: "纯五度 (Perfect 5th)", 8: "小六度 (Minor 6th)",
        9: "大六度 (Major 6th)", 10: "小七度 (Minor 7th)", 11: "大七度 (Major 7th)",
        12: "纯八度 (Perfect Octave)"
    }
def shengcheng_yincheng(jiben_yinming1, jiben_yinming2, piano_keys, yincheng_biao):
    yingao1, yingao2 = piano_keys[jiben_yinming1], piano_keys[jiben_yinming2]
    distance = abs(yingao1 - yingao2)
    if distance in yincheng_biao:
        yincheng_xingzhi = yincheng_biao[distance]
    else:
        yincheng_xingzhi = f"超过八度 (纯八度 x {distance // 12} + {yincheng_biao.get(distance % 12, '未知')})"
    return distance, yincheng_xingzhi


# 调式的定义与生成
def dingyi_diaoshi():
    diaoshi_moban = {
        "自然大调": [0, 2, 4, 5, 7, 9, 11], "自然小调": [0, 2, 3, 5, 7, 8, 10],
        "和声大调": [0, 2, 4, 5, 7, 8, 11], "和声小调": [0, 2, 3, 5, 7, 8, 11],
        "旋律大调": [0, 2, 4, 5, 7, 8, 10], "旋律小调": [0, 2, 3, 5, 7, 9, 11]
    }
    return diaoshi_moban, GENYIN_BIAO


def shengcheng_diaoshi_yinjie(jiben_yinming, diaoshi_leixing, piano_keys, diaoshi_muban, genyin_yingao):
    zhuyin_shuju = (4 + 1) * 12 + genyin_yingao[jiben_yinming]
    zuizhou_yinjie = [zhuyin_shuju + i for i in diaoshi_muban[diaoshi_leixing]]
    reverse_keys = {v: k for k, v in piano_keys.items()}
    return [reverse_keys.get(idd, "超出范围") for idd in zuizhou_yinjie]


#  和弦
hexian_moban = {
    "大三": [0, 4, 7], "小三": [0, 3, 7], "增三": [0, 4, 8], "减三": [0, 3, 6],
    "大大七": [0, 4, 7, 11], "大小七": [0, 4, 7, 10], "小小七": [0, 3, 7, 10],
    "减小七": [0, 3, 6, 10], "减减七": [0, 3, 6, 9], "大九": [0, 4, 7, 11, 14],
    "属九": [0, 4, 7, 10, 14], "小小九": [0, 3, 7, 10, 14],
    "十一": [0, 4, 7, 10, 14, 17], "十三": [0, 4, 7, 10, 14, 17, 21]
}

#转位的定义
def zhuanwei(yuan_id_list, zhuanwei_cishu):
    xin_id_list = yuan_id_list.copy()
    for _ in range(zhuanwei_cishu):
        if xin_id_list:
            xin_id_list.append(xin_id_list.pop(0) + 12)
    return xin_id_list

def hexianshengcheng(genyin_ming, xingzhi, zhuanwei_cishu=0, piano_keys=None, reverse_piano_keys=None):
    genyin_shuju = (4 + 1) * 12 + GENYIN_BIAO[genyin_ming]
    hexian_id = [genyin_shuju + gap for gap in hexian_moban[xingzhi]]
    if zhuanwei_cishu > 0:
        hexian_id = zhuanwei(hexian_id, zhuanwei_cishu)
    hexian_ming = [reverse_piano_keys.get(m_id, "超出范围") for m_id in hexian_id]
    return hexian_id, hexian_ming

#和弦外音的定义
WAIYIN_BIAO = {
    "留": "延留音 (Suspension)",
    "倚": "倚音 (Appoggiatura)",
    "过": "经过音 (Passing Tone)",
    "助": "辅助音 (Neighbor Tone)",
    "换": "换音 (Cambiata)",
    "先": "先现音 (Anticipation)"
}

def jiance_waiyin(yin_id, hexian_id_list):
    hexian_genyin = [h_id % 12 for h_id in hexian_id_list]
    if (yin_id % 12) not in hexian_genyin:
        return True  # 是外音
    return False  # 是内音
# 逻辑分类：根据前后音关系确定外音类型
def dingyi_waiyin_leixing(pre_id, cur_id, nxt_id, hexuan_id_list):
    if not jiance_waiyin(cur_id, hexuan_id_list):
        return "内"

    # 经过音：音高方向一致，且处于级进关系
    if (pre_id < cur_id < nxt_id or pre_id > cur_id > nxt_id) and abs(nxt_id - pre_id) <= 4:
        return "过"

    # 辅助音：两端音高相同，中间音级进
    if pre_id == nxt_id and abs(cur_id - pre_id) <= 2:
        return "助"

    # 延留音：前音与当前音相同，后续下行或上行解决
    if pre_id == cur_id and cur_id != nxt_id:
        return "留"

    # 先现音：当前音与后音相同，且当前音相对于当前和弦是外音
    if cur_id == nxt_id and cur_id != pre_id:
        return "先"

    return "+"  # 默认外音标记

