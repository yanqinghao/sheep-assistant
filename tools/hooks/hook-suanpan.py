import os
from PyInstaller.utils.hooks import collect_all, collect_system_data_files
from PyInstaller.utils.hooks import logger
import pathlib

os.environ['SP_APP_TYPE'] = 'stream'
os.environ['SP_NODE_ID'] = 'test_node_id'
datas, binaries, hiddenimports = collect_all('suanpan', include_py_files=False)

logger.info('Collecting suanpan datas: {}'.format(datas))
logger.info('Collecting suanpan hiddenimports: {}'.format(hiddenimports))
