import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from util import Config

def test_Config():
    config = Config(file='./data/config_example')
    assert config.get('DB_HOST') == '123.234.111.1'
    assert config.get('DB_USER') == 'test'
    assert config.get('DB_PASSWORD') == 'testpwd123'