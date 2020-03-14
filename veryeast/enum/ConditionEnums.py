from enum import Enum, unique


# 首页第一级菜单
class HomeFirstMenu(Enum):
    advert_manage = 0  # 广告管理
    crm_system = 1  # CRM系统
    oa_system = 2  # OA系统
    performance_system = 3  # 绩效系统
    finance_system = 4  # 报销系统
    help_center = 5  # 帮助中心


# CRM系统子菜单
class CRMSystemChildMenu(Enum):
    company_console = 0  # 公司工作台
    personal_console = 1  # 个人工作台
    statement_center = 2  # 报表中心


# 个人工作台子菜单
class PersonalConsoleChildMenu(Enum):
    my_clue = 0  # 我的线索
    my_public_sea = 1  # 我的公海
    my_customer = 2  # 我的客户
    my_business_chance = 3  # 我的商机
    my_contract = 4  # 我的合同
    customer_duplicate_checking = 5  # 客户查重
    cooperate_customer = 6  # 协同客户


# 所属公海
@unique
class PublicSeaEnum(Enum):
    fourth_part_high_quantity_customer = 0  # 四部区域优质客户公海
    recruit_fourth_part_prepare = 1  # 招聘四部筹备公海
    ve_marketing_center_building = 2  # VE营销中心房产公海
    ve_marketing_center = 3  # VE营销中心公海
    recruit_fourth_part = 4  # 招聘四部d公海
    recruit_third_part = 5  # 招聘三部公海


# 客户来源
@unique
class CustomerSource(Enum):
    not_limit = 0
    very_east_register = 1  # 最佳东方注册



