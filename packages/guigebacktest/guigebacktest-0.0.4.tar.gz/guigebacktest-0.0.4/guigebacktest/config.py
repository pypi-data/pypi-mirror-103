
# -*- coding: utf-8 -*-
import platform

MODE = 'production'  # development: 开发模式; production: 生产模式


class BaseConfig(object):
    """
    通用配置
    """
    COMMISSION = 0.0
    OPERATION_TYPE = 'right'
    QUOTE_TYPE = 'price'
    if platform.system() == 'Windows':
        DATA_INPUT_PATH = r'D:/data/input/'     #
        DATA_OUTPUT_PATH = r'D:/data/output/'   #
    elif platform.system() == 'Linux':
        DATA_INPUT_PATH = r'/data/input/'       #
        DATA_OUTPUT_PATH = r'/data/output/'     #
    else:
        print('Unknown system')


class ProductionConfig(BaseConfig):
    """
    生产配置
    """


class DevelopConfig(BaseConfig):
    """
    开发配置
    """


if MODE == 'production':
    config = ProductionConfig
else:
    config = DevelopConfig
