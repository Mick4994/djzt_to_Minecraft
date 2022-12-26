import logging
import time

def log_init(fh_log_level = logging.DEBUG, ch_log_level = logging.DEBUG) -> logging.Logger: 
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Log等级总开关
    rq = time.strftime('%Y-%m-%d %H-%M', time.localtime(time.time()))
    log_path = './logs/'
    log_name = log_path + rq + '.log'
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='w', encoding='utf-8')
    ch = logging.StreamHandler()
    fh.setLevel(fh_log_level)  # 输出到文件的log等级的开关
    ch.setLevel(ch_log_level)  # 输出到控制台的log等级的开关
    formatter = logging.Formatter("%(asctime)s - %(filename)s [%(threadName)s] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

def record_start_info(args:dict, logger:logging.Logger) -> None:
    str_info = 'Start Args:\n'
    for key, value in args.items():
        for _ in range(7):
            str_info += "\t" 
        str_info += f"[{key}: {str(value)}]" + "\n"
    str_info = str_info[:-1]
    logger.info(str_info)