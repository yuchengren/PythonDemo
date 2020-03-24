import os
from datetime import datetime

from base.utils import TimeUtils

print((TimeUtils.parseToDatetime("2020年3月23日 10:45", "%Y年%m月%d日 %H:%M") - datetime.now()).seconds)


