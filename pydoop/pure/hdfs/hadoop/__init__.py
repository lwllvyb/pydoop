__author__ = 'kikkomep'

import os
import logging
import importlib

from pydoop.pure.bridge.factory import JavaWrapperFactory


logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger("pydoop.pure.hadoop")

# Hadoop ClassPath detection
HADOOP_CLASSPATH = os.environ.get("HADOOP_CLASSPATH")
if HADOOP_CLASSPATH is None:
    raise EnvironmentError(
        "HADOOP_CLASSPATH not found! Use hadoop classpath to detect it and to set it into your environment")

# Adds the HADOOP_CLASSPATH to the default Java CLASSPATH
CLASSPATH = os.environ.get("CLASSPATH", ".") + ":" + HADOOP_CLASSPATH

HADOOP_VERSION_INFO_JAVA_CLASS = "org.apache.hadoop.util.VersionInfo"

# the factory instance for creating Python wrappers of Java classes
factory = JavaWrapperFactory(classpath=CLASSPATH, java_bridge_name="JPype")
logger.debug("JavaWrapperFactory created!")


def wrap_class(fully_qualified_class_name):
    """

    :param fully_qualified_class_name:
    :return:
    """
    return factory.get_wrapper(fully_qualified_class_name)


def wrap_class_instance(fully_qualified_class_name, *args):
    """

    :param fully_qualified_class_name:
    :param args:
    :return:
    """
    return factory.get_wrapper(fully_qualified_class_name)(*args)


def get_hadoop_version():
    """
    Detects the current available Hadoop distribution
    :return:
    """
    version_info = wrap_class(HADOOP_VERSION_INFO_JAVA_CLASS)
    return version_info.getVersion()


def get_implementation_instance(class_name_prefix, *args, **kwargs):
    try:
        class_name = class_name_prefix + HADOOP_HDFS_IMPL_SUFFIX
        logger.debug("Trying to load the implementation class %s from the package %s" % (class_name, HADOOP_HDFS_WRAPPER_MODULE_NAME))
        cl = getattr(implementation_module, class_name)
        return cl(*args, **kwargs)
    except Exception, e:
        print "Unable to load the class %s" % class_name
        print e.message


def get_implementation_module():
    return implementation_module


# Loads the proper version of the hadoop hdfs wrapper
HADOOP_VERSION = get_hadoop_version()
HADOOP_HDFS_WRAPPER_MODULE_NAME = "pydoop.pure.hdfs.hadoop.hadoop_" + HADOOP_VERSION.replace(".", "_")
HADOOP_HDFS_IMPL_SUFFIX = "Impl"

logger.debug("HADOOP_HDFS_WRAPPER_MODULE: %s" % HADOOP_HDFS_WRAPPER_MODULE_NAME)

implementation_module = importlib.import_module(HADOOP_HDFS_WRAPPER_MODULE_NAME)

