=================
Introduction
=================
log4python

log for python like java log4j2

use config file [log4p.py], in the application root directory.

=================
Important Update
=================
:Content:
 - support python 3.7
 - remove flume-log
 - fix some bugs
 - improve config file document

=========
Usage
=========
::

    from log4python.Log4python import log
    TestLog = log("LogDemo")
    TestLog.debug("Debug Log")
    TestLog.info("Info Log")

    out put like this:
    2015-01-20 16:18:47,692 DEBUG [Thread-3] data.LogInsert (LogInsert.py:172) - Debug Log
    2015-01-20 16:18:47,692 DEBUG [Thread-3] data.LogInsert (LogInsert.py:173) - Info Log

==================
Config Example
==================
::

    config ={
        'monitorInterval' : 10,                         # auto reload time interval [secs]
        'loggers' :{
            'LogDemo' :{
                'level': "DEBUG",
                'additivity' : False,
                'AppenderRef' : ['LogDemo']
                },
            'root' :{
                'level' : "DEBUG",
                'AppenderRef' : ['output_root']
            }
        },
        'appenders' :{
            'output_root' :{
                'type' :"file",
                'FileName' :"root_error.log",            # log file name
                'backup_count': 5,                       # files count use backup log
                'file_size_limit': 1024 * 1024 * 20,     # single log file size, default :20MB
                'PatternLayout' :"[level:%(levelname)s-file:%(filename)s-lineno:%(lineno)d] %(asctime)s %(message)s"
            },
            'LogDemo' :{
                'type' :"file",
                'FileName' :"LogDemo.log",
                'PatternLayout' :"[level:%(levelname)s-file:%(filename)s-lineno:%(lineno)d] %(asctime)s %(message)s"
            },
            'console' :{
                'type' :"console",
                'target' :"console",
                'PatternLayout' :"[%(levelname)s] %(asctime)s %(message)s"
            }
        }
    }
