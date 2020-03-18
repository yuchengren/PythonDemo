from enum import Enum, unique

# app的类型
@unique
class AppType(Enum):
    mockuai_star_seller = "魔筷星选商家"  # 魔筷星选商家
    mockuai_star_buyer = "魔筷星选"  # 魔筷星选
    penguin_shop_seller = "企鹅小店商家"  # 企鹅小店商家
    wudi_zhubo_seller = "无敌主播"  # 无敌主播


# 应用市场
@unique
class MarketChannel(Enum):
    mockuai = "mockuai"  # 魔筷官网
    huawei = "huawei"  # 华为
    xiaomi = "xiaomi"  # 小米
    oppo = "oppo"
    vivo = "vivo"
    tencent = "tencent"  # 腾讯





