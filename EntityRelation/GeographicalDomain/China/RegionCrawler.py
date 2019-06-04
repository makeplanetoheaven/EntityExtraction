# coding=utf-8

# 引入外部库

# 引入内部库

# 全局变量
# 地理区域
geographical_region = {'华东': ['上海市', '江苏省', '浙江省', '安徽省', '江西省', '山东省', '福建省', '台湾省'],
                     '华北': ['北京市', '天津市', '山西省', '河北省', '内蒙古自治区中部'],
                     '华中': ['河南省', '湖北省', '湖南省'],
                     '华南': ['广东省', '广西壮族自治区', '海南省', '香港特别行政区', '澳门特别行政区'],
                     '西南': ['重庆市', '四川省', '贵州省', '云南省', '西藏自治区'],
                     '西北': ['陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区', '内蒙古自治区西部'],
                     '东北': ['黑龙江省', '吉林省', '辽宁省', '内蒙古自治区东部']}
inner_mongolia_region = {'内蒙古自治区西部': ['包头市', '鄂尔多斯市', '乌海市', '巴彦淖尔市', '阿拉善盟'],
                         '内蒙古自治区东部': ['赤峰市', '通辽市', '兴安盟', '呼伦贝尔市'],
                         '内蒙古自治区中部': ['呼和浩特市', '乌兰察布市', '锡林郭勒盟']}
# 经济区域
economic_region = {'中部': ['山西省', '河南省', '湖北省', '湖南省', '江西省', '安徽省'],
                 '东部': ['北京市', '天津市', '河北省', '山东省', '江苏省', '上海市', '浙江省', '福建省', '广东省', '海南省'],
                 '西部': ['重庆市', '四川省', '广西壮族自治区', '贵州省', '云南省', '陕西省', '甘肃省', '内蒙古自治区西部', '宁夏回族自治区', '新疆维吾尔自治区', '青海省',
                        '西藏自治区']}


def get_region () -> [list, list]:
    """
    获取中国所有区域实体及其与各城市间关系
    实体类型：包含，属于
    :return: entity_info：实体信息列表，entity_rel：实体关系三元组列表
    """
    entity_info = []
    entity_rel = []

    index = 0
    region_list = [geographical_region, economic_region, inner_mongolia_region]
    for region_dict in region_list:
        for region in region_dict:
            city_list = region_dict[region]
            entity_info.append({'type': '区域', 'property': {'name': region, "域": "地理位置域", "id": "CNR" + str(index)}})
            for city in city_list:
                entity_rel.append([index, '包含', city])
                entity_rel.append([city, '属于', index])
            index += 1

    return entity_info, entity_rel
