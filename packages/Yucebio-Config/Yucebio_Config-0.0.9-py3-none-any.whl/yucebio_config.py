# -*- coding: utf-8 -*-
"""
    Yucebio-Config
    ~~~~~~~~~~~~~~

    通用配置管理模块

    加载配置
        1. 当前目录下 config
        2. 当前目录下 .yucebioconfig
        3. HOME目录下 .yucebioconfig

    :copyright: (c) 2021 by huangqingjun@yucebio.com.
    :license: MIT, see LICENSE_FILE for more details.
"""

from typing import Any
import os
import json5
from icecream import ic


DEFAULT_CONFIG_DIR = ".yucebioconfig"
DEFAULT_USER_CONFIG_DIR = 'config'
DEFAULT_CONFIG_NAME = 'config'
DEFAULT_CONFIG_EXTENSIONS = ['json5', 'json']

class Config(object):
    def __init__(self, name: str = None, path: str= None) -> None:
        """初始化配置所在位置。 ./config/{name}.json -> ~/.yucebioconfig/default.json

        Args:
            name (str, optional): 配置文件名称. Defaults to 'default'.
            path (str, optional): 配置文件存在目录. Defaults to '~/.yucebioconfig'.
        """
        self._config: dict = None
        self.configpath, self.configfile = self.detect(name, path)

    def detect(self, name: str = None, path: str = None):
        # 若提供配置路径，直接在配置路径下查找 name | config
        if path:
            candidate_config_file = self._detect_config_file(path, name or DEFAULT_CONFIG_NAME)
            if not candidate_config_file:
                candidate_config_file = os.path.join(path, (name or DEFAULT_CONFIG_NAME) + '.json5')
            return path, candidate_config_file

        workdir = os.getcwd()
        for path, expect in [
            (os.path.join(workdir, DEFAULT_USER_CONFIG_DIR), name or DEFAULT_CONFIG_NAME),                                                   # 当前目录的config目录查找 (name or config).json
            (os.path.join(workdir, DEFAULT_CONFIG_DIR), name or DEFAULT_CONFIG_NAME),                                                        # 查找当前目录的.yucebioconfig目录
            (os.path.join(os.path.expanduser('~'), DEFAULT_CONFIG_DIR), name or os.path.dirname(os.path.abspath(workdir)).replace(' ', '_')),   # HOME目录下根据当前项目名查找配置文件
        ]:
            candidate_config_file = self._detect_config_file(path, expect)
            if candidate_config_file:
                return path, candidate_config_file

        # 若以上都无法找到，自动使用当前目录下的 name 作为配置文件，优先使用 .yucebioconfig目录
        config_path = os.path.join(workdir, DEFAULT_CONFIG_DIR)
        if os.path.exists(os.path.join(workdir, DEFAULT_USER_CONFIG_DIR)):
            config_path = os.path.join(workdir, DEFAULT_USER_CONFIG_DIR)

        return config_path, os.path.join(config_path, (name or DEFAULT_CONFIG_NAME) + '.json5')

    def _detect_config_file(self, path: str, expect_file_name: str):
        if not os.path.exists(path) or not expect_file_name:
            return
        for ext in DEFAULT_CONFIG_EXTENSIONS:
            expect_config_file = os.path.join(path, expect_file_name + '.' + ext)
            if os.path.exists(expect_config_file):
                return expect_config_file
        return None

    def load(self) -> dict:
        """从~/.yucebio中提取配置信息
        """
        if not os.path.exists(self.configfile):
            return {}
        
        with open(self.configfile, encoding='utf8') as r:
            self._config: dict= json5.load(r)
        return self._config

    def __str__(self):
        return json5.dumps(self.config, indent=2)

    @property
    def config(self) -> dict:
        if self._config is None:
            self._config = self.load()
        return self._config

    def update(self, data: dict):
        self._config.update(data)
        self.save()

    def init(self, init_data: dict):
        self._config = init_data
        self.save()

    def save(self):
        if not os.path.exists(self.configpath):
            os.makedirs(self.configpath)
        with open(self.configfile, 'w') as w:
            json5.dump(self.config, w, indent=2)

    def reload(self):
        self.save()
        self._config = self.load()

    def reset(self):
        self.load()
    
    def clear(self, key: str=None, sep: str=None):
        """清除指定key对应的配置项，嵌套字段使用sep分隔。如 clear('a.b', sep='.')会清除字段a的子字段b的配置项

        Args:
            key (str, optional): 待清除的key. Defaults to None.
            sep (str, optional): 自定义嵌套字段分隔符. Defaults to None.
        """
        if not key:
            self._config = {}
        else:
            keys = [key] if not sep else key.split(sep)
            _ref, final_key = self._config, keys[-1]
            for k in keys[:-1]:
                if k not in _ref:
                    return
                _ref = _ref[k]
            
            if final_key in _ref:
                del _ref[final_key]
        self.save()

    def __call__(self, key: str, default: Any=None) -> Any:
        return self.config.get(key, default)

    def __getitem__(self, key: str, default=None) -> Any:
        return self.config.get(key, default)

    def __contains__(self, key: str) -> bool:
        return key in self.config

    def __setitem__(self, key: str, value: Any):
        self.config[key] = value


config = Config()
if __name__ == '__main__':
    ic(config)