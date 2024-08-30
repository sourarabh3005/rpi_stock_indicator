from enum import Enum

class SystemFields(Enum):
    SYS_EXCEL_STATE   = (0, 0)
    SYS_CPU_TEMP      = (1, 1)
    SYS_CURR_DATE     = (2, 1)
    SYS_CURR_TIME     = (3, 1)
    SYS_BUY_STK_FLAG  = (0, 2)
    SYS_BUY_STK_VAL   = (1, 2)
    SYS_SELL_STK_FLAG = (0, 3)    
    SYS_SELL_STK_VAL  = (1, 3) 
    SYS_CRT_STK_FLAG  = (0, 4)
    SYS_CRT_STK_VAL   = (1, 4)