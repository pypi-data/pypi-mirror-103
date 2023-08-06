import os
import sys
import importlib

from fedflow.utils import ModuleUtils


class Config(object):

    USER_HOME = os.path.expanduser("~")
    NICO_ROOT = os.path.join(USER_HOME, "datasets", "nico")
    CIFAR_ROOT = os.path.join(USER_HOME, "datasets", "cifar")

    # Parameters that can be modified at run time
    props = {}
    # Parameters that are read from a configuration file and cannot be changed at run time
    readonly_props = {}
    # home directory

    @classmethod
    def load(cls):
        config_dict = ModuleUtils.import_config()
        if config_dict is not None:
            cls.set_config(config_dict)

    @classmethod
    def set_config(cls, d: dict):
        cls.readonly_props = d.copy()

    @classmethod
    def device(cls):
        cuda = cls.get_property("cuda")
        if cuda == "-1":
            return "cpu"
        return "cuda:%d" % cuda

    @classmethod
    def get_property(cls, key, default=None):
        """
        Get the value of readonly parameters.

        :param key: a string of the key to get the value
        """
        op_res, readonly_val = cls.__get_from_dict(cls.props,
                                                   cls.__split_key(key),
                                                   default)
        if op_res:
            return readonly_val
        return cls.__get_from_dict(cls.props,
                                   cls.__split_key(key),
                                   default)[1]

    @classmethod
    def set_property(cls, key, value):
        """
        Set parameters at run time.
        """
        k_seq = cls.__split_key(key)
        if cls.__exists_in_dict(cls.readonly_props, k_seq):
            raise ValueError("readonly key[%d] cannot be modified." % key)
        cls.__set_to_dict(cls.props, cls.__split_key(key), value)

    @classmethod
    def __split_key(cls, key: str):
        if key is None or key.strip() == "":
            raise ValueError("key cannot be none or empty.")
        return key.split(".")

    @classmethod
    def __exists_in_dict(cls, d: dict, k_seq: list):
        if k_seq is None or len(k_seq) == 0:
            return False
        for k in k_seq:
            if k in d:
                d = d[k]
            else:
                return False
        return True

    @classmethod
    def __get_from_dict(cls, d: dict, k_seq: list, default=None):
        if k_seq is None or len(k_seq) == 0:
            raise ValueError("key cannot be none or empty")
        for k in k_seq:
            if k in d:
                d = d[k]
            else:
                return False, default
        return True, d

    @classmethod
    def __set_to_dict(cls, d: dict, k_seq: list, value):
        if k_seq is None or len(k_seq) == 0:
            raise ValueError("key cannot be none or empty")
        for k in k_seq[:-1]:
            if k not in d:
                d[k] = {}
            d = d[k]
        d[k_seq[-1]] = value


Config.props = {
    "cuda": 0,
    "workdir": "",
}