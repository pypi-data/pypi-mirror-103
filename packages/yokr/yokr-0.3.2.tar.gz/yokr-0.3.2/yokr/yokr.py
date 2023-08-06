# -*- coding: utf-8 -*-
# adding client side aggregation
#    name="yokr",
#    version="0.3.02"
import builtins
import datetime
import functools
import hashlib
import requests
import json
import logging
import os
import re
import sqlite3
import sys
import time
import uuid
import pkg_resources


logger = logging.getLogger('yokr')
logger.setLevel(logging.DEBUG)

_runLocal = False
#_runLocal = True

_yCE = None


def _runFromIpython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


class YkrCacheEnv:
    fieldsLst = ("dataCollectorDirectory_default", "dataCollectorDb_default",
                 "cmpHashInfoKey_default", "cmpHash_default",
                 "cmpName_default",
                 "cmpNameAlias_default", "cmpDescription_default",
                 "cmpUUID_default", "cmpContactPersonId_default",
                 "cmpStartDate_default", "appHashInfoKey_default",
                 "appHash_default", "appName_default", "appHash_default",
                 "appNameAlias_default", "appDescription_default",
                 "appUUID_default", "appContactPersonId_default",
                 "appStartDate_default", "instHashInfoKey_default",
                 "instHash_default", "instName_default",
                 "instNameAlias_default",
                 "instDescription_default", "instUUID_default",
                 "instContactPersonId_default", "instStartDate_default",
                 "venv_path_default", "checkResourceFiles_P_default",
                 "checkResourceFiles_I_default", "checkResourceFiles_default",
                 "runFromIpython_default", "reportFlushNum_default",
                 "reportFlushTime_default",
                 "uploadInterval_default", "uploadIntervalMin_default",
                 "instDataRetantionDays_default",
                 "instDataLastTimeDeleted_default",
                 "reportLoc_default", "uploadLastTime_default",
                  "uploadedLastAttempt_default", 
                  "accountSecretIncorrectFlag_default",
                 "accountSecret_default", "YokarandaServer_default",
                 "max_result_size_default", "libsWithNoDetails_default",
                 "libsLoaded_default", "DirCmpFile_default",
                 "DirAppFile_default", "DirInstFile_default",
                 "dataCollectorDirectory", "dataCollectorDb", "cmpHashInfoKey",
                 "cmpHash", "cmpName", "cmpNameAlias", "cmpDescription",
                 "cmpUUID", "cmpContactPersonId", "cmpStartDate",
                 "appHashInfoKey", "appHash", "appName", "appNameAlias",
                 "appDescription", "appUUID", "appContactPersonId",
                 "appStartDate", "instHashInfoKey", "instHash",
                 "instName", "instNameAlias", "instDescription", "instUUID",
                 "instContactPersonId", "instStartDate", "venv_path",
                 "checkResourceFiles_P", "checkResourceFiles_I",
                 "checkResourceFiles", "runFromIpython", "reportFlushNum",
                 "reportFlushTime", "uploadInterval", "uploadIntervalMin",
                 "instDataRetantionDays", "instDataLastTimeDeleted",
                 "reportLoc", "uploadLastTime",
                 "accountSecret", "YokarandaServer", "max_result_size",
                 "libsLoaded", "DirCmpFile",
                 "DirAppFile", "DirInstFile",
                 "uploadedLastAttempt",
                 "accountSecretIncorrectFlag",
                 "LastUploadStatus", "LastUploadStatus_default",
                 "LocalAggFreq", "LocalAggFreq_default")

    def __init__(self):
        for z in self.fieldsLst:
            setattr(self, z, None)
        self.reportFlushNum_default = 20
        # minutes interval to flush the data  from memory to the local database
        self.reportFlushTime_default = 5
        self.uploadInterval_default = 15
        self.uploadIntervalMin_default = 2
        self.instDataRetantionDays_default = 14
        self.dataCollectorDirectory_default = \
            os.path.join(os.path.expanduser('~'),'.yokaranda_databases')
        self.dataCollectorDb_default = 'YokaDB'
        if _runLocal:
            self.YokarandaServer_default = 'http://127.0.0.1:5000/postData2'
        else:
            self.YokarandaServer_default = 'https://api.yokaranda.com/postData2'
        self.checkResourceFiles_default = True
        self.checkResourceFiles_P_default = True
        self.checkResourceFiles_I_default = False
        self.max_result_size_default = 10000

        self.cmpDescription_default =\
            "Enter a one line short description of the company"
        self.cmpContactPersonId_default = "-1"
        self.cmpName_default = "Replace with company name"
        self.cmpNameAlias_default = "Replace with company name alias"

        self.appDescription_default = \
            "Enter a one line short description of the application"
        self.appContactPersonId_default = "-1"
        self.appName_default = "Replace with application name"
        self.appNameAlias_default = "Replace with application name alias"

        self.instDescription_default =\
            "Enter a one line short description of the instance"
        self.instContactPersonId_default = "-1"
        self.instName_default = "Replace with instance name"
        self.instNameAlias_default = "Replace with instance name alias"
        self.runFromIpython_default = 1
        # Set values
        self.uploadLastTime_default = 0
        self.reportLoc_default = 0
        self.LastUploadStatus = 500
        self.LastUploadStatus_default = 500
        self.uploadedLastAttempt_default = 0
        #  4 - hourly
        self.LocalAggFreq_default  = 4 
        self.accountSecretIncorrectFlag = False
        #  end setting default values
        self.reportFlushStartTime = time.time()
        self.reportVecTime = []
        self.reportVecParam = []
        self.reportVecValue = []
        self.dbPathAndName22 = None
        self.accountSecret_default = ''
        self.runFromIpython = _runFromIpython()
        if self.runFromIpython:
            self.checkResourceFiles = self.checkResourceFiles_I
        else:
            self.checkResourceFiles = self.checkResourceFiles_P
        self.tables = [
                ('InfoCompany', 'StartDate'),
                ('InfoApp', 'StartDate'),
                ('InfoEntity', 'AddedDate'),
                ('InfoInstance', 'StartDate'),
                ('InstanceData', 'TimeStamp'),
                ('UsedEntities', 'LastDate', 'InstanceDataAgg')
            ]
        self.libsLoaded_default = set()
        self.libsWithNoDetails_default =  \
            set(['abc', 'ast', 'asyncio', 'autoreload', 'base64', 'bdb',
                 'bisect', 'bz2', 'cProfile', 'calendar', 'cmd', 'code',
                 'codecs', 'codeop', 'collections', 'concurrent',
                 'configparser', 'contextlib', 'copy', 'copyreg', 'datetime',
                 'difflib', 'dis', 'email', 'encodings', 'enum', 'filecmp',
                 'fnmatch', 'functools', 'genericpath', 'getopt', 'getpass',
                 'gettext', 'glob', 'gzip', 'hashlib', 'heapq', 'hmac', 'html',
                 'http', 'imp', 'importlib', 'inspect', 'io', 'keyword',
                 'linecache', 'locale', 'lzma', 'mimetypes', 'mtrand',
                 'multiprocessing', 'ntpath', 'ntsecuritycon', 'nturl2path',
                 'numbers', 'opcode', 'operator', 'os', 'pathlib', 'pdb',
                 'pickle', 'pkgutil', 'plistlib', 'posixpath', 'pprint',
                 'profile', 'pstats', 'pydoc', 'pydoc_data', 'pyexpat',
                 'pythoncom', 'pywintypes', 'queue', 'quopri', 'random',
                 'readline', 'reprlib', 'runpy', 'select', 'selectors',
                 'shlex', 'shutil', 'signal', 'site', 'socket',
                 'sphinxcontrib', 'spydercustomize', 'sqlite3', 'sre_compile',
                 'sre_constants', 'sre_parse', 'ssl', 'stat', 'storemagic',
                 'string', 'struct', 'subprocess', 'sysconfig', 'tempfile',
                 'textwrap', 'threading', 'timeit', 'tkinter', 'token',
                 'tokenize', 'traceback', 'turtle', 'types', 'typing',
                 'unicodedata', 'unittest', 'urllib', 'uu', 'uuid', 'warnings',
                 'weakref', 'win32api', 'win32com', 'win32security', 'xml',
                 'zipfile'])


def _ykrUpdate(df=None, upload=True, removeHistory=True, forceUpload=False):
    if df is not None:
        _ykrUpdateInfo(df=df)
    minFromLastUpload = (time.time() - _yCE.uploadLastTime) / 60.0
    minFromLastUploadAttempt = (time.time() - _yCE.uploadedLastAttempt) / 60.0
    logger.debug("Intervals %s, time since last call %s, last call %s" %
                 (_yCE.uploadInterval, minFromLastUpload,
                  _yCE.uploadLastTime))
    if (((_yCE.accountSecret != '') and 
         (not _yCE.accountSecretIncorrectFlag) and 
         (minFromLastUploadAttempt > 1)) and
        ((forceUpload  and minFromLastUpload > _yCE.uploadIntervalMin) or
         (upload and (minFromLastUpload >= _yCE.uploadInterval))
         )):
        _ykrUpload(tables=_yCE.tables)
    if removeHistory:
        _params_RemoveHistory()


def _reloadConfigFiles():
    logger.debug("populating company")
    _ykrConfigCompanyInfo()
    logger.debug("populating App")
    _ykrConfigAppInfo()
    logger.debug("populating Inst")
    _ykrConfigInstInfo()

def _ykrStartup():
    """ Internal function used for initializing the library """
    logger.debug("_yCE populating _yCE")
    _yCEPopulate()
    _reloadConfigFiles()
    _yCE.checkResourceFiles = _yCE.checkResourceFiles_I if \
        _yCE.runFromIpython else _yCE.checkResourceFiles_P
    _ykrCreateCollectorDBIfNeeded(dbPathAndName22=_yCE.dbPathAndName22)


def _onAttach():
    # Do nothing in onAttach()
    pass


def postfix_function(function, postfunction):
    @functools.wraps(function)
    def run(*args, **kwargs):
        result = function(*args, **kwargs)
        postfunction(result)
        return result
    return run


def _custom_import(name, *args, **kwargs):
        m = original_import(name, *args, **kwargs)
        if _yCE is not None:
            _after_module_load(m)
        return m



if not ('original_import' in locals() or 'original_import' in globals()):
    if (callable(builtins.__import__) and 
        builtins.__import__.__name__ == '__import__') :
        original_import = builtins.__import__
        builtins.__import__ = _custom_import


# End -  needed to catch imports done trough the import statement
def _print_libs(info=None):
    for inf in info:
        logger.debug("loaded - %s, %s, %s, %s" %
                     (inf.Entity, inf.Version, inf.Build, inf.License[0:50]))


def _onLoad():
    _ykrStartup()
    df = _ykrGetLibsInfo()
    _print_libs(info=df)
    _ykrUpdate(df=df, forceUpload=True)
    logger.info("Yokaranda Loaded")


def _ykrGetConfigFileLoc(fName=None, level=1):
    """
    Finds the location of the file @fname,
    the search starts at the working directory,
    If @level > 1,the next level to be checked is
        the parent directory of the working directory
    If @level > 2, the next level to be checked
        is the parent of the parent directory
    If @level > 3, then the next level to be checked is
        the directory in env["USERPROFILE"]
    """
    dirPrefix = '.yokaranda'
    useDir = None
    testDir = os.path.abspath(os.getcwd())
    dirpath = os.path.join(testDir, dirPrefix)
    fallback = os.path.join(os.path.expanduser('~'),dirPrefix)
    filepath = os.path.join(dirpath, fName)
    if os.path.exists(filepath):
        useDir = dirpath
    if useDir is None and level > 1:
        testDir = os.path.abspath(os.path.join(testDir, os.pardir))
        dirpath = os.path.join(testDir, dirPrefix)
        filepath = os.path.join(dirpath, fName)
        if os.path.exists(filepath):
            useDir = dirpath
    if useDir is None and level > 2:
        testDir = os.path.abspath(os.path.join(testDir, os.pardir))
        dirpath = os.path.join(testDir, dirPrefix)
        filepath = os.path.join(dirpath, fName)
        if os.path.exists(filepath):
            useDir = dirpath
    if useDir is None and level > 3:
        testDir = os.environ.get('USERPROFILE')
        if testDir:
            dirpath = os.path.join(testDir, dirPrefix)
            filepath = os.path.join(dirpath, fName)
            if os.path.exists(filepath):
                useDir = dirpath
    if useDir is None:
        useDir = fallback
    return useDir


def _yCEPopulate():
    """
    Creates and initializes variables in '.ykrCacheEnv' environment
    """
    global _yCE
    _yCE = YkrCacheEnv()
    fields = (x for x in _yCE.fieldsLst if not ("_default" in x))
    for field in fields:
        setattr(_yCE, field, getattr(_yCE, field + "_default"))
    pkg_resources_filepath = sys.modules['pkg_resources'].__file__
    if os.path.sep == '/':
        sep = os.path.sep
    else:
        sep = re.escape(os.path.sep)
    expr = r'^(.*)' + sep + r'lib' + r'(?:' + sep + 'python(?:[0-9.]*))?' + \
           sep + r'(?:site|dist)-packages' + sep + r'pkg_resources' + sep + \
           r'__init__.pyc?$'
    m = re.match(expr, pkg_resources_filepath)
    if m:
        _yCE.venv_path = m.group(1)


def _read_dcf(filepath):
    result = {}
    with open(filepath) as f:
        for line in f:
            clean_line = line.strip()
            if clean_line:
                parts = clean_line.split(':', 1)
#               Ignore lines without values
                if len(parts) == 2 and parts[1].strip() != "":
                    result[parts[0].strip()] = parts[1].strip()
    return result


def _write_dcf(a_dict, filepath):
    with open(filepath, 'w') as f:
        for k, v in a_dict.items():
            f.write('%s: %s\n' % (k, v))


def _writeNewConfigCompanyInfoFile(companyFile=None):
    cmpUUID = str(uuid.uuid4())
    dfCompany = dict(
        cmpName=_yCE.cmpName_default,
        cmpNameAlias=_yCE.cmpNameAlias_default,
        cmpUUID=cmpUUID,
        cmpDescription=_yCE.cmpDescription_default,
        cmpHash=hashlib.sha1(cmpUUID.encode('ASCII')).hexdigest(),
        cmpStartDate=_format_datetime_utc(with_tz_name=' GMT'),
        cmpContactPersonId=_yCE.cmpContactPersonId_default,
        reportFlushNum=_yCE.reportFlushNum_default,
        reportFlushTime=_yCE.reportFlushTime_default,
        uploadInterval=_yCE.uploadInterval_default,
        instDataRetantionDays=_yCE.instDataRetantionDays_default,
        dataCollectorDirectory=_yCE.dataCollectorDirectory_default,
        dataCollectorDb=_yCE.dataCollectorDb_default,
        YokarandaServer=_yCE.YokarandaServer_default,
        checkResourceFiles_P=_yCE.checkResourceFiles_P_default,
        checkResourceFiles_I=_yCE.checkResourceFiles_I_default,
        max_result_size=_yCE.max_result_size_default,
        accountSecret=_yCE.accountSecret_default
    )
    _write_dcf(dfCompany, companyFile)
    return(dfCompany)


def _rewriteConfigCompanyInfoFile(companyFile=None, dfCompany=None):
    # rewrites the company info file - creates  new cmpUUID and new cmpHash
    cmpUUID = str(uuid.uuid4())
    secret = dfCompany.get('accountSecret') or " "
    dfCompanyNew = dict(
        cmpName=dfCompany.get('cmpName'),
        cmpNameAlias=dfCompany.get('cmpNameAlias'),
        cmpUUID=cmpUUID,
        cmpDescription=dfCompany.get('cmpDescription'),
        cmpHash=hashlib.sha1(cmpUUID.encode('ASCII')).hexdigest(),
        cmpStartDate=_format_datetime_utc(with_tz_name=' GMT'),
        cmpContactPersonId=dfCompany.get('cmpContactPersonId'),
        reportFlushNum=dfCompany.get('reportFlushNum'),
        reportFlushTime=dfCompany.get('reportFlushTime'),
        uploadInterval=dfCompany.get('uploadInterval'),
        instDataRetantionDays=dfCompany.get('instDataRetantionDays'),
        dataCollectorDirectory=dfCompany.get('dataCollectorDirectory'),
        dataCollectorDb=dfCompany.get('dataCollectorDb'),
        YokarandaServer=dfCompany.get('YokarandaServer'),
        checkResourceFiles_P=dfCompany.get('checkResourceFiles_P'),
        checkResourceFiles_I=dfCompany.get('checkResourceFiles_I'),
        max_result_size=dfCompany.get('max_result_size'),
        accountSecret=secret
    )
    _write_dcf(dfCompanyNew, companyFile)
    return(dfCompanyNew)


def _isIntRangeOK(val, min_val, max_val, field, entity):
    if val < min_val or val > max_val:
        new_val = getattr(_yCE, field+"_default")
        logger.warning(".%sDCF.txt file, field %s range expected (%d,%d)" %
                       (entity, field, min_val, max_val))
        logger.warning("value found %d, replaced with default value %d)" %
                       (val, new_val))
    return val


def _fixVal(entity=None, infoDict=None, field=None):
    val = infoDict[field]
    if (type(val) != str):
        return val
    if field in {"dataCollectorDirectory", "dataCollectorDb",
                 "YokarandaServer", "accountSecret"}:
        return val
    if field in {"checkResourceFiles_P", "checkResourceFiles_I"}:
        if val.lower() == "true":
            return True
        else:
            return False
    if (field in {"cmpName", "cmpNameAlias", "cmpUUID", "cmpDescription",
                  "cmpHash", "cmpStartDate", "cmpContactPersonId"} and
            entity == "company"):
            return val
    if (field in {"appName", "appNameAlias", "appUUID", "appHash",
                  "appDescription", "appStartDate", "appContactPersonId"}
            and entity == "application"):
        return val
    if (field in {"instName", "instNameAlias", "instUUID", "instHash",
                  "instDescription", "instStartDate",
                  "instContactPersonId"} and entity == "instance"):
        return val
    if field in {"reportFlushNum", "reportFlushTime",
                 "uploadInterval", "instDataRetantionDays",
                 "max_result_size"}:
        try:
            val = int(val)
            if (field == "reportFlushNum"):
                val = _isIntRangeOK(val, 1, 1000, field, entity)
            elif (field == "reportFlushTime"):
                val = _isIntRangeOK(val, 1, 300, field, entity)
#            elif (field == "reportSendTime"):
#                val = _isIntRangeOK(val, 1, 1000, field, entity)
            elif (field == "uploadInterval"):
                val = _isIntRangeOK(val, 10, 1440, field, entity)
            elif (field == "instDataRetantionDays"):
                val = _isIntRangeOK(val, 2, 30, field, entity)
            elif (field == "max_result_size"):
                val = _isIntRangeOK(val, 1000, 10000, field, entity)
        except ValueError:
            logger.error(".%sDCF.txt file, field %s integer expected found %s"
                         % (entity, field, val))
            val = None
    return val


def _ykrConfigCompanyInfo():
    """
    Get/Set the company information.
    If company info already exists in the environment use it,
    otherwise create it.
    """
    global _yCE
    # set everything to its default
    _yCE.DirCmpFile = _ykrGetConfigFileLoc('.companyDCF.txt', level=3)
    if not os.path.exists(_yCE.DirCmpFile):
        os.makedirs(_yCE.DirCmpFile)
    companyFile = os.path.join(_yCE.DirCmpFile, '.companyDCF.txt')
    if os.path.exists(companyFile):
        dfCompany = _read_dcf(companyFile)
        if 'cmpUUID' not in dfCompany:
            dfCompany =  \
                _rewriteConfigCompanyInfoFile(companyFile=companyFile,
                                              dfCompany=dfCompany)
        logger.info("Yoka: company file - %s", companyFile)
    else:
        dfCompany = _writeNewConfigCompanyInfoFile(companyFile=companyFile)
        logger.info("Yoka:  new company file written - %s", companyFile)
    # chgnge dfaults according to info in the companyDCF file
    fields = (x for x in _yCE.fieldsLst if
              not (("_default" in x) or ("app" in x) or ("inst" in x)))
    for field in fields:
        if (field in dfCompany):
            val = _fixVal("company", dfCompany, field)
            if val is not None:
                setattr(_yCE, field, val)
    s = '@'.join([
        _yCE.cmpContactPersonId, _yCE.cmpDescription,
        _yCE.cmpHash, _yCE.cmpName, _yCE.cmpNameAlias])
    s = s.encode('UTF-8')
    _yCE.cmpHashInfoKey = hashlib.sha1(s).hexdigest()
    if _yCE.accountSecret == '':
        logger.warning("acountSecret not found or empty in " +
                       _yCE.DirCmpFile + "\\.companyDCF.txt",)
        logger.warning("without a valid acountSecret no data will be " +
                       "uploaded to Yokaranda server'")
        logger.warning("to get a new account sectret go to www.yokaranda.com'")


def _writeNewConfigAppInfoFile(appFile=None):
    appUUID = str(uuid.uuid4())
    dfApp = dict(
        appName=_yCE.appName_default,
        appNameAlias=_yCE.appNameAlias_default,
        appUUID=appUUID,
        appHash=hashlib.sha1(appUUID.encode('ASCII')).hexdigest(),
        appDescription=_yCE.appDescription_default,
        appStartDate=_format_datetime_utc(with_tz_name=' GMT'),
        appContactPersonId=_yCE.appContactPersonId_default
    )
    _write_dcf(dfApp, appFile)
#    cmpUUID = str(uuid.uuid4())
    return(dfApp)


def _rewriteConfigAppInfoFile(appFile=None, dfApp=None):
    # rewrites the sppication  info file - creates  newappUUID and new appHash
    appUUID = str(uuid.uuid4())
    dfAppNew = dict(
        appName=dfApp.get('appName'),
        appNameAlias=dfApp.get('appNameAlias'),
        appUUID=appUUID,
        appHash=hashlib.sha1(appUUID.encode('ASCII')).hexdigest(),
        appDescription=dfApp.get('appDescription'),
        appStartDate=_format_datetime_utc(with_tz_name=' GMT'),
        appContactPersonId=dfApp.get('appContactPersonId')
    )
    _write_dcf(dfAppNew, appFile)
    return(dfAppNew)


def _ykrConfigAppInfo():
    """
    Get/Set the App  information.
    If App info already exists in the environment use it, otherwise create it.
    """
    global _yCE
    _yCE.DirAppFile = _ykrGetConfigFileLoc('.appDCF.txt', level=3)
    if not os.path.exists(_yCE.DirAppFile):
        os.makedirs(_yCE.DirAppFile)
    appFile = os.path.join(_yCE.DirAppFile, '.appDCF.txt')
    if os.path.exists(appFile):
        dfApp = _read_dcf(appFile)
        logger.info("Yoka: application file - %s", appFile)
        if 'appUUID' not in dfApp:
            dfApp =  \
                _rewriteConfigAppInfoFile(appFile=appFile, dfApp=dfApp)
    else:
        dfApp = _writeNewConfigAppInfoFile(appFile=appFile)
        logger.info("Yoka:  new application file written - %s", appFile)
    fields = (x for x in _yCE.fieldsLst if
              not (("_default" in x) or ("cmp" in x) or ("inst" in x)))
    for field in fields:
        if (field in dfApp):
            val = _fixVal("application", dfApp, field)
            if val is not None:
                setattr(_yCE, field, val)
    s = '@'.join([
        _yCE.appUUID, _yCE.appDescription, _yCE.appNameAlias,
        _yCE.appName, _yCE.appContactPersonId,
        _yCE.cmpHashInfoKey])
    s = s.encode('UTF-8')
    _yCE.appHashInfoKey = hashlib.sha1(s).hexdigest()


def _writeNewConfigInstInfoFile(instFile=None):
    instUUID = str(uuid.uuid4())
    dfInst = dict(
        instName=_yCE.instName_default,
        instNameAlias=_yCE.instNameAlias_default,
        instUUID=instUUID,
        instHash=hashlib.sha1(instUUID.encode('ASCII')).hexdigest(),
        instDescription=_yCE.instDescription_default,
        instStartDate=_ykrNowF(),
        instContactPersonId=_yCE.instContactPersonId_default
    )
    _write_dcf(dfInst, instFile)
    return(dfInst)


def _rewriteConfigInstInfoFile(instFile=None, dfInst=None):
    #   rewrites the sppication  info file - creates newappUUID and new appHash
    instUUID = str(uuid.uuid4())
    dfInstNew = dict(
        instName=dfInst.get('instName'),
        instNameAlias=dfInst.get('instNameAlias'),
        instUUID=instUUID,
        instHash=hashlib.sha1(instUUID.encode('ASCII')).hexdigest(),
        instDescription=dfInst.get('instDescription'),
        instStartDate=_ykrNowF(),
        instContactPersonId=dfInst.get('instContactPersonId')
    )
    _write_dcf(dfInstNew, instFile)
    return(dfInstNew)


def _ykrConfigInstInfo():
    """
    Get/Set the Instance information.
    If Instance info already exists in the environment use it,
    otherwise create it.
    """
    global _yCE
    _yCE.DirInstFile = _ykrGetConfigFileLoc('.instDCF.txt', level=3)
    if not os.path.exists(_yCE.DirInstFile):
        os.makedirs(_yCE.DirInstFile)
    instFile = os.path.join(_yCE.DirInstFile, '.instDCF.txt')
    if os.path.exists(instFile):
        dfInst = _read_dcf(instFile)
        if 'instUUID' not in dfInst:
            dfInst =  \
                _rewriteConfigInstInfoFile(instFile=instFile, dfInst=dfInst)
        logger.info("Yoka: Instance file - %s", instFile)
    else:
        dfInst = _writeNewConfigInstInfoFile(instFile=instFile)
        logger.info("Yoka: new Instance file written - %s", instFile)
    fields = (x for x in _yCE.fieldsLst if
              not (("_default" in x) or ("app" in x) or ("cmp" in x)))
    for field in fields:
        if (field in dfInst):
            val = _fixVal("instance", dfInst, field)
            if val is not None:
                setattr(_yCE, field, val)
    s = '@'.join([
        _yCE.instName, _yCE.instNameAlias, _yCE.instUUID,
        _yCE.instDescription, _yCE.instContactPersonId,
        _yCE.appHashInfoKey])
    s = s.encode('UTF-8')
    _yCE.instHashInfoKey = hashlib.sha1(s).hexdigest()
    filename = '%s_%s.db' % (_yCE.dataCollectorDb, _yCE.instUUID)
    try:
        dbPathAndName22 = os.path.join(_yCE.dataCollectorDirectory, filename)
        x=dbPathAndName22
        y=x
        _yCE.dbPathAndName22 = y
        logger.info("Internal DB %s", dbPathAndName22)
    except Exception as err:
        logger.error(err)


def _flush_report():
    #   puts into the interanl datbase all the instance data cached
    #   and cleans the cash
    try:
        con_open = False
        if len(_yCE.reportVecTime) > 0:
                con = sqlite3.connect(_yCE.dbPathAndName22)
                con_open = True
                rows = [
                    (_yCE.instHashInfoKey,
                     _yCE.reportVecTime[i],
                     _yCE.reportVecParam[i],
                     _yCE.reportVecValue[i],
                     0)
                    for i in range(len(_yCE.reportVecTime))
                ]
                sql = """ INSERT INTO InstanceData (InstHashInfoKey, TimeStamp,
                          ParamName, Value, Uploaded) VALUES (?,?,?,?,?)"""
                c = con.cursor()
                c.executemany(sql, rows)
                con.commit()
                _yCE.reportFlushStartTime = time.time()
                _yCE.reportLoc = 0
                _yCE.reportVecTime = []
                _yCE.reportVecParam = []
                _yCE.reportVecValue = []
    except Exception:
        logger.exception("exception in _flush_report")
    finally:
        if con_open:
            con.close()


def _params_RemoveHistory():
    #   cleans from the "internal" database old instance data
    try:
        con_open = False
        sysTime = time.time()
        if ((_yCE.instDataLastTimeDeleted is None) or
                ((sysTime - _yCE.instDataLastTimeDeleted) / (24 * 3600) >= 1)):
                logger.debug("Hi removing history")
                con = sqliteConnect(_yCE.dbPathAndName22)
                con_open = True
                query = """
                    DELETE FROM InstanceData WHERE
                    julianday('now') - julianday(substr(Timestamp, 1, 10)) > ?
                    """
                args = (_yCE.instDataRetantionDays,)
                c = con.cursor()
                c.execute(query, args)
                con.commit()
                query = """
                    DELETE FROM InstanceDataAgg WHERE
                    julianday('now') - julianday(substr(Timestamp, 1, 10)) > ?
                    """
                args = (_yCE.instDataRetantionDays,)
                c = con.cursor()
                c.execute(query, args)
                con.commit()
                _yCE.instDataLastTimeDeleted = time.time()
    except Exception:
        logger.exception("exception in _params_RemoveHistory")
    finally:
        if con_open:
            con.close()

def  sqliteConnect(dbPathAndName22):
    _ykrCreateCollectorDBIfNeeded(dbPathAndName22)
    return sqlite3.connect(dbPathAndName22)

def _ykrCreateCollectorDBIfNeeded(dbPathAndName22):
    """
    Checks if a SQLite file @dbPathAndName22 already exists
    If it does not exist it is created, and all its needed internal
    tables are also created.
    """
    if os.path.exists(dbPathAndName22):
        return
    con_open = False
    try:
        sql_file_path = \
            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'create_tables.sql')
        with open(sql_file_path) as f:
            sql = f.read()
        dbPath = os.path.dirname(dbPathAndName22)
        if not os.path.exists(dbPath):
            os.makedirs(dbPath)
        con = sqlite3.connect(dbPathAndName22)
        con_open = True
        c = con.cursor()
        c.executescript(sql)
        sql = 'INSERT INTO Uploads (Date, Status) VALUES (?, ?)'
        args = ('2000-08-21 13:17:14', 'OK')
        c.execute(sql, args)
        con.commit()
    finally:
        if con_open:
            con.close()


def _updateInstanceDataSentToDB(con=None, cursor=None, rowIds=[]):
        sql = 'UPDATE InstanceDataAgg SET Uploaded = 1 WHERE rowid IN (%s)'
        sql = sql % ','.join('?' * len(rowIds))
        cursor.execute(sql, rowIds)
        con.commit()


def _uploadToDb(con=None, cursor=None, data=None, rowIds=[]):
    jsonString = json.dumps(data)
    d = dict()
    d["client"] = "Python0002"
    d["data"] = data
    jsonString = json.dumps(d, ensure_ascii=False).encode('UTF-8')
    status = _ykrUpload_postToServer(body=jsonString)
    if status == 769434:
        _yCE.accountSecretIncorrectFlag = True
    if (_yCE.LastUploadStatus == 200 or _yCE.LastUploadStatus == 0):
        _yCE.LastUploadStatus = status
    if (status == 200) and ("InstanceDataAgg" in data): #1234
        _updateInstanceDataSentToDB(con=con, cursor=cursor,
                                    rowIds=rowIds)




def _sendTable(con=None, cursor=None, query=None, args=None,
               data=None, tableName=None, rowIds=[]):
    if (args is not None):
        cursor.execute(query, args)
    else:
        cursor.execute(query)
    chunk = cursor.fetchmany(size=_yCE.max_result_size)
    total_size = 0
    if chunk is not None and len(chunk) > 0:
        logger.debug("_sendTable() - %s" % tableName)
        di = chunk[0].keys()
        cols_num = len(di)
        total_size += cols_num
        while chunk is not None and len(chunk) > 0:
            lsts = [[] for i in range(cols_num)]
            for col in chunk:
                for i in range(cols_num):
                    if isinstance(col[i], str):
                        lsts[i].append(col[i][0:150])
                    else:
                        lsts[i].append(col[i])
            d = dict()
            for i in range(cols_num):
                d[di[i]] = lsts[i]
#            TODO Check
#            chunk = cursor.fetchmany(size=_yCE.max_result_size)
            rowIds += d.pop("rowid", [])
            data[tableName] = d
            if len(chunk) >= _yCE.max_result_size:
                _uploadToDb(con=con, cursor=cursor, data=data, rowIds=rowIds)
                data = dict()
                rowIds = []
            chunk = cursor.fetchmany(size=_yCE.max_result_size)
    return(data, rowIds)


def _getLastUploadTime(cursor=None):
    sql = """ SELECT Date FROM Uploads WHERE Status = 'OK' """
    cursor.execute(sql)
    row = cursor.fetchone()
    lastSucssefulUpateDate = row['Date']
    return lastSucssefulUpateDate

##### TODO  expose timeout as parameter and add to config files
def _ykrUpload_postToServer(body=None):
    """
    # POST to REST API server using the url @restServerURL and the @body
    # Returns the status  returned by the REST API server
    """
    status = -1
    retVal = 0
    target = _yCE.YokarandaServer + "/Python1"
    try:
        rep = requests.post(target, data=body,
                          auth=(_yCE.instUUID, _yCE.accountSecret),
                          timeout=4)
        status = rep.status_code
        retVal = rep.json()
        if status == 200:
            if retVal['status'] == 1:
                logger.debug("Data posted to %s HTTP code %d" %
                             (target, status))
            else:
                status = retVal['errId']
                logger.warning("Failed to post data to %s, HTTP failure code %d msg - %s" %
                           (target, retVal['errId'],retVal['val']))
        else:
            logger.warning("Failed to post data to %s, HTTP failure code %d" %
                           (target, status))
    except Exception as err:
        logger.error("exception in yokr _ykrUpload_postToServer: URL = %s" %
                     target)
        logger.error(err)
    finally:
        return status


def _createSQLite3connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn



def _createAggInLocalDB(conn = None, maxRowid = None):
    sql = """
        INSERT INTO InstanceDataAgg
        SELECT A.InstHashInfoKey,
            :TimeStamp TimeStamp,
            A.ParamName ParamName,
            substr(A.TimeStamp,1,15) || '0:00 UTC' StartTime,
            substr(A.TimeStamp,1,15) || '9:59 UTC' EndTime,
            COUNT(A.Value) ValNum, SUM(A.Value) ValSum,
            MAX(A.Value) ValMax, MIN(A.Value) ValMin,   
            AVG(A.Value) ValAvg,
            AVG((A.Value-B.mean)*(A.Value-B.mean)) ValVar, 
            0 uploaded
        FROM InstanceData A, 
            (SELECT AVG(Value) mean, InstHashInfoKey, 
                 ParamName, substr(TimeStamp,1,15) SubTimeStamp
             FROM InstanceData
             WHERE Uploaded = 0 AND rowid <= :maxRowid
             GROUP BY InstHashInfoKey, ParamName, substr(TimeStamp,1,15)
             ) B 
            WHERE A.Uploaded = 0 
                AND A.rowid <= :maxRowid 
                AND A.ParamName = B.ParamName
                AND A.InstHashInfoKey = B.InstHashInfoKey
                AND substr(A.TimeStamp,1,15) = B.SubTimeStamp
            GROUP BY  A.InstHashInfoKey, A.ParamName, substr(A.TimeStamp,1,15)
        """
    try: 
        cur = conn.cursor()
        cur.execute(sql, {'maxRowid': maxRowid, 'TimeStamp' : _ykrNowF()})
        return True
    except sqlite3.Error as e:
        print(e)
        return False


def _fromData2AggLocalDB():
    conn = None
    try:
        conn = _createSQLite3connection(_yCE.dbPathAndName22)
        sql =  ''' SELECT MAX(rowid) from InstanceData WHERE  Uploaded = 0'''
        cur = conn.cursor()
        cur.execute(sql)
        val = cur.fetchone()[0]
        if val != None:
            #Add to aggregation table
            if (_createAggInLocalDB(conn = conn,maxRowid = val)) :
                #Mark instance data as processed 
                sql = """
                    UPDATE InstanceData
                    SET Uploaded = 1
                    WHERE Uploaded = 0 AND rowid <= :val
                    """
                cur.execute(sql, {'val': val})
                conn.commit()
        else:
            print('')
    except sqlite3.Error as e:
        print(e)
    finally: 
        if not conn is None:
            conn.close()
####################### HERE
def _ykrUpload(tables=None):
    con_open = False
    now = time.time()
    try:
        _yCE.LastUploadStatus = 0
        timeStamp = _ykrNowF()
        con = sqliteConnect(_yCE.dbPathAndName22)
        con_open = True
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        lastSucssefulUpateDate = _getLastUploadTime(cursor=cursor)
        data = dict()
        rowIds = []
        for tab in tables:
            logger.debug("_ykrUpload() - table = %s" % tab[0])
            if tab[0] == 'InstanceData':
                tmpLst = list(tab)
                tmpLst[0] = 'InstanceDataAgg'
                tab = tuple(tmpLst)
                _fromData2AggLocalDB()
                query = 'SELECT rowid,* FROM %s WHERE Uploaded = ?' % tab[0]
                args = (0,)
            elif tab[0] == 'UsedEntities':
                query = """
                    SELECT  InstHashInfoKey, EntityHashKey, StartDate, LastDate
                    FROM UsedEntities WHERE LastDate >= datetime(?)"""
                args = (lastSucssefulUpateDate,)
            elif tab[0] == 'InfoEntity':
                query = 'SELECT * FROM %s WHERE %s >= datetime(?)' % (
                    tab[0], tab[1])
                args = (lastSucssefulUpateDate,)
            else :
                query = """
                    SELECT %s.* from %s inner join
                    (SELECT MAX(rowid) as rid
                     from %s
                     GROUP BY  UUID) b on b.rid = %s.rowid
                """ % (tab[0], tab[0], tab[0], tab[0])
                args = None
            # START OLD - deleted LIMIT 1 
                # elif tab[0] == 'InfoEntity':
                #     query = 'SELECT * FROM %s WHERE %s >= datetime(?)' % (
                #         tab[0], tab[1])
                #     args = (lastSucssefulUpateDate,)
                # else:
                #     query = """ SELECT * FROM %s WHERE %s >= datetime(?)
                #                 ORDER BY rowid DESC """ % (tab[0], tab[1])
                #     # START OLD - deleted LIMIT 1
                #     # query = """SELECT * FROM %s WHERE %s >= datetime(?)
                #     #    ORDER BY rowid DESC LIMIT 1
                #     # """ % (tab[0], tab[1])
                #     # END OLD - deleted LIMIT 1
                #     args = (lastSucssefulUpateDate,)
            # END OLD - deleted LIMIT 1
            data, rowIds = _sendTable(con=con, cursor=cursor, query=query,
                                      args=args, data=data, tableName=tab[0],
                                      rowIds=rowIds)
        if len(data) > 0:
            _uploadToDb(con=con, cursor=cursor, data=data, rowIds=rowIds)
        if _yCE.LastUploadStatus == 200:
            sql = 'UPDATE Uploads SET Date = ?'
            args = (timeStamp,)
            cursor.execute(sql, args)
            con.commit()
            logger.info("Params values and used entities (libraries)" +
                        " data uploaded to Yokaranda")

            _yCE.uploadLastTime = now
    except Exception as err:
        logger.error("exception in yokr - _ykrUpload() : %s", err)
    finally:
        _yCE.uploadedLastAttempt = now
        if con_open:
            con.close()


def _format_datetime_utc(dt=None, with_tz_name=True):
    if dt is None:
        dt = datetime.datetime.now(tz=datetime.timezone.utc)
    elif type(dt) in (int, float):
        dt = datetime.datetime.utcfromtimestamp(dt)
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    result = dt.strftime('%Y-%m-%d %H:%M:%S')
    if with_tz_name is True:
        result += ' UTC'
    elif type(with_tz_name) == str:
        result += with_tz_name
    return result


def _ykrNowF():
    """
    returns the actual UTC date-time in format "%Y-%m-%d %H:%M:%S"
    """
    return _format_datetime_utc(dt=None, with_tz_name=False)


def _ykdGenLibInfoHashKey(EntityType=None, Entity=None,
                          Version=None, License=None):
    try:
        s = '@@@'.join([EntityType, Entity, Version, License, ])
    except Exception:
        logger.error("P51 lib_info.Entity =%s type = %s" %
                     (Entity, type(Entity)))
        logger.error("P61 lib_info.Version  =%s type = %s" %
                     (Version, type(Version)))
        logger.error("P71 lib_info.License  =%s type = %s" %
                     (License, type(License)))
    s = s.encode('UTF-8')
    HashKey = hashlib.sha1(s).hexdigest()
    return HashKey


def _ykdGenLibVerHashKey(EntityType=None, Entity=None, Version=None,
                         License=None, Build=None, PublicationDate=None,
                         Title=None, Description=None):
    s = '@@@'.join([
        EntityType, Entity, Version, License, Build, PublicationDate,
        Title, Description,
    ])
    s = s.encode('UTF-8')
    HashKey = hashlib.sha1(s).hexdigest()
    return HashKey


def _ykdGenInstEntVerHashKey(InstHashInfoKey=None, EntityHashKey=None):
    s = '@@@'.join([InstHashInfoKey, EntityHashKey])
    s = s.encode('UTF-8')
    HashKey = hashlib.sha1(s).hexdigest()
    return HashKey


class LibInfo:
    ENTITY_PYTHON_LIB = 'PythonLib'
    SUPPORTED_ENTITIES = ('Sensor', 'OS', 'OSLib', '3rdParty', 'JavaLib',
                          'RLib', 'PythonLib')
    __slots__ = (
        'HashKey', 'LibVerHashKey', 'EntityType', 'Entity', 'Version',
        'Title', 'Description', 'License', 'Url', 'BugReports', 'Build',
        'PublicationDate', 'AddedDate'
    )

    def __init__(self):
        self.HashKey = ''
        self.LibVerHashKey = ''
        self.EntityType = ''
        self.Entity = ''
        self.Version = ''
        self.Title = ''
        self.Description = ''
        self.License = ''
        self.Url = ''
        self.BugReports = ''
        self.Build = ''
        self.PublicationDate = ''
        self.AddedDate = ''

    @staticmethod
    def from_module(module, name=None, now=None):
        global _yCE
        if name is None:
            name = module.__name__
        if now is None:
            now = _ykrNowF()
        version = getattr(module, '__version__', None)
        title = getattr(module, '__description__', None)
        description = getattr(module, '__doc__', None)
        license_ = getattr(module, '__license__', None)
        url = getattr(module, '__url__', None)
        if (_yCE.checkResourceFiles and
                (version is None or license_ is None) and
                (name not in _yCE.libsWithNoDetails_default)):
            # Using pkg_resources can give extra info but is relativlly slow
            package = None
            try:
                package = pkg_resources.get_distribution(name)
            except (pkg_resources.DistributionNotFound,
                    pkg_resources.RequirementParseError):
                pass
            if package:
                # override with package metadata if available
                version = package.version
                package_info = getattr(package, '_parsed_pkg_info', None)
                if package_info:
                    package_info = package._parsed_pkg_info
                    title = package_info['Summary']
                    license_ = package_info['License']
                    url = package_info['Home-page']
                    # default to __doc__ if available
                    description = description or package_info._payload
        lib_info = LibInfo()
        lib_info.EntityType = 'PythonLib'
        lib_info.Entity = name
        lib_info.Version = version \
            if (version is not None and isinstance(version, str)) else ''
        lib_info.Title = title or ''
        lib_info.Description = description or ''
        lib_info.License = license_ or ''
        lib_info.Url = url
        lib_info.BugReports = ''
        lib_info.Build = ''
        lib_info.PublicationDate = ''
        lib_info.AddedDate = now
        lib_info.HashKey =  \
            _ykdGenLibInfoHashKey(EntityType=lib_info.EntityType,
                                  Entity=lib_info.Entity,
                                  Version=lib_info.Version,
                                  License=lib_info.License)
        lib_info.LibVerHashKey =  \
            _ykdGenLibVerHashKey(EntityType=lib_info.EntityType,
                                 Entity=lib_info.Entity,
                                 Version=lib_info.Version,
                                 License=lib_info.License,
                                 Build=lib_info.Build,
                                 PublicationDate=lib_info.PublicationDate,
                                 Title=lib_info.Title,
                                 Description=lib_info.Description)
        return lib_info


def _ykrGetLibsInfo():
    """
    Returns a list of LibInfo instances with information about loaded libraries
    """
    now = _ykrNowF()
    if _yCE.venv_path is not None:
        packages = {}
        for name, module in sys.modules.items():
            package_name = name.split('.', 1)[0]
            if name == package_name or package_name not in packages:
                packages[package_name] = module
                _yCE.libsLoaded.add(package_name)
        packages = [
            (name, module) for name, module in packages.items()
            if name != 'pkg_resources' and
            not name.startswith('_') and
            hasattr(module, '__file__') and
            module.__file__ is not None and 
            module.__file__.startswith(_yCE.venv_path)
        ]
    else:
        packages = []
    packages_info = [
        LibInfo.from_module(module, name=name, now=now)
        for name, module in packages
    ]
    return packages_info


def _after_module_load(module):
    global _yCE
    if _yCE is None or _yCE.dbPathAndName22 is None:
        # to protect from soem iPython and debuggers behaviours
        return
    if not hasattr(module, '__name__'):
        logger.debug("yokr::_after_module_load - message 111111100")
        return
    name = module.__name__
    if name in _yCE.libsLoaded:
        return
    package_name = name.split('.', 1)[0]
    if (name != package_name):
        # package is likely a subpakage - and there is no info about it
        version = getattr(module, '__version__', None)
        if (version is None) or (version == ""):
            return
    if (package_name not in sys.modules):
        logger.debug("""yokr::_after_module_load -  message 111111111a
                      pakage_name %s name %s""" % (package_name, name))
        return
    if not hasattr(module, '__file__'):
        logger.debug("""yokr::_after_module_load -  message 111111112
               pakage_name %s name %s""" % (package_name, name))
        return
    if _yCE.venv_path is None:
        logger.debug("yokr::_after_module_load - message 111111113")
        return
    if not module.__file__.startswith(_yCE.venv_path):
        logger.debug("yokr::_after_module_load - message 111111113")
        return
    df = [LibInfo.from_module(module)]
    _ykrUpdate(df=df)
    _yCE.libsLoaded.add(name)


def _ykrUpdateLibsInfo(db, df, now, instHashInfoKey):
    use = []
    for lib_info in df:
        u = dict(
            InstHashInfoKey=instHashInfoKey,
            EntityHashKey=lib_info.LibVerHashKey,
            StartDate=now,
            LastDate=now,
        )
        u['HashInfoKey'] = _ykdGenInstEntVerHashKey(
                InstHashInfoKey=u['InstHashInfoKey'],
                EntityHashKey=u['EntityHashKey'])
        use.append(u)
    sql = 'SELECT HashInfoKey FROM UsedEntities WHERE InstHashInfoKey = ?'
    args = (instHashInfoKey,)
    c = db.cursor()
    c.execute(sql, args)
    useInDB = c.fetchall()
    if len(useInDB) == 0:
        rows_to_insert = [
            (u['HashInfoKey'], u['InstHashInfoKey'], u['EntityHashKey'],
             u['StartDate'], u['LastDate'])
            for u in use]
        sql = '''INSERT INTO UsedEntities (HashInfoKey, InstHashInfoKey,
                             EntityHashKey, StartDate, LastDate)
                 VALUES (?,?,?,?,?)'''
        c.executemany(sql, rows_to_insert)
        db.commit()
        return "new"
    else:
        useInDBKeys = set([row['HashInfoKey'] for row in useInDB])
        rows_to_insert = []
        keys_to_update = []
        for u in use:
            if u['HashInfoKey'] in useInDBKeys:
                keys_to_update.append(u['HashInfoKey'])
            else:
                rows_to_insert.append(u)
        if rows_to_insert:
            rows_to_insert = [
                (u['HashInfoKey'], u['InstHashInfoKey'], u['EntityHashKey'],
                 u['StartDate'], u['LastDate'])
                for u in rows_to_insert]
            sql = '''INSERT INTO UsedEntities (HashInfoKey, InstHashInfoKey,
                            EntityHashKey, StartDate, LastDate)
                     VALUES (?,?,?,?,?)'''
            c.executemany(sql, rows_to_insert)
        if keys_to_update:
            # code assumes UsedEntities will not exceed 1000 rows
            sql = '''UPDATE UsedEntities SET LastDate = ?
                     WHERE HashInfoKey IN (%s)'''
            sql = sql % ','.join('?' * len(keys_to_update))
            args = [now] + list(keys_to_update)
            c.execute(sql, args)
        db.commit()
        return "existing"

def _ykrUpdateHirarchy (db=None,sqlExists=None,argsExits=None,
                        sqlAdd=None,argsAdd=None):
    cursor = db.cursor()
    cursor.execute(sqlExists, argsExits)
    row = cursor.fetchone()
    num = row['num']
    if num  == 0:
        cursor.execute(sqlAdd, argsAdd)
        db.commit()


def _ykrUpdateGeneralInfo(db,cFlag=False,aFlag=False,iFlag=False):
    now = _ykrNowF()
    if cFlag:
        _ykrUpdateHirarchy(db=db,
                        sqlExists='SELECT COUNT(*) num FROM InfoCompany WHERE HashInfoKey = ?',
                        argsExits=(_yCE.cmpHashInfoKey,),
                        sqlAdd='''
                            INSERT INTO InfoCompany (HashInfoKey, HashKey, Name,
                                                     NameAlias, Description, UUID, ContactPersonId,
                                                     StartDate) 
                            VALUES (?,?,?,?, ?,?,?,?)''',
                        argsAdd=(_yCE.cmpHashInfoKey, _yCE.cmpHash,
                                 _yCE.cmpName, _yCE.cmpNameAlias,
                                 _yCE.cmpDescription, _yCE.cmpUUID,
                                 _yCE.cmpContactPersonId, now))
    if aFlag:
        _ykrUpdateHirarchy(db=db,
                        sqlExists='SELECT COUNT(*) num FROM InfoApp WHERE HashInfoKey = ?',
                        argsExits=(_yCE.appHashInfoKey,),
                        sqlAdd='''
                            INSERT INTO InfoApp (HashInfoKey, HashKey, CompanyHashInfoKey,
                                                 Name, NameAlias, Description, UUID, ContactPersonId,
                                                 StartDate) 
                            VALUES (?,?,?,?,?, ?,?,?,?)''',
                        argsAdd=(_yCE.appHashInfoKey, _yCE.appHash,
                                 _yCE.cmpHashInfoKey,
                                 _yCE.appName, _yCE.appNameAlias,
                                 _yCE.appDescription, _yCE.appUUID,
                                 _yCE.appContactPersonId, now))
    if iFlag:
        _ykrUpdateHirarchy(db=db,
                        sqlExists='SELECT COUNT(*) num FROM InfoInstance WHERE HashInfoKey = ?',
                        argsExits=(_yCE.instHashInfoKey,),
                        sqlAdd='''
                            INSERT INTO InfoInstance (HashInfoKey, HashKey,
                                                      AppHashInfoKey, Name, NameAlias, Description, UUID,
                                                      ContactPersonId, StartDate)
                            VALUES (?,?,?,?,?, ?,?,?,?)''',
                        argsAdd=(_yCE.instHashInfoKey, _yCE.instHash,
                                 _yCE.appHashInfoKey,
                                 _yCE.instName, _yCE.instNameAlias,
                                 _yCE.instDescription, _yCE.instUUID,
                                 _yCE.instContactPersonId, now))



def _ykrUpdateInfo(df):
    # code assumes InfoEntity will not exceed 1000 rows
    try:
        con_open = False
        sql = '''SELECT DISTINCT LibVerHashKey keys FROM InfoEntity
                 WHERE LibVerHashKey IN (%s)'''
        args = [lib_info.LibVerHashKey for lib_info in df]
        sql = sql % ','.join('?' * len(args))
        db = sqlite3.connect(_yCE.dbPathAndName22)
        con_open = True
        db.row_factory = sqlite3.Row
        c = db.cursor()
        c.execute(sql, args)
        rows = c.fetchall()
        present_keys = set((row['keys'] for row in rows))
        rows_to_insert = []
        for lib_info in df:
            if lib_info.LibVerHashKey not in present_keys:
                rows_to_insert.append(
                    (lib_info.HashKey, lib_info.LibVerHashKey,
                     lib_info.EntityType, lib_info.Entity, lib_info.Version,
                     lib_info.Title, lib_info.Description, lib_info.License,
                     lib_info.Url, lib_info.BugReports, lib_info.Build,
                     lib_info.PublicationDate, lib_info.AddedDate))
        if rows_to_insert:
            sql = '''INSERT INTO InfoEntity (
                        HashKey, LibVerHashKey, EntityType, Entity, Version,
                        Title, Description, License, Url, BugReports, Build,
                        PublicationDate, AddedDate)
                    VALUES (?,?,?,?,?,?,?, ?,?,?,?,?,?)'''
            c.executemany(sql, rows_to_insert)
            db.commit()
        now = _ykrNowF()
        _ykrUpdateLibsInfo(db=db, df=df, now=now,
                           instHashInfoKey=_yCE.instHashInfoKey)
        _ykrUpdateGeneralInfo(db=db,cFlag=True,aFlag=True,iFlag=True)
    finally:
        if con_open:
            db.close()

# START EXPORT FUNCTIONS


def libs_in_use():
    """
    Returns a list of LibInfo instances with information about
    the loaded libraries
    """
    try:
        result = _ykrGetLibsInfo()
        for lib_info in result:
            lib_info.HashKey = None
            lib_info.LibVerHashKey = None
        return result
    except Exception as err:
        logger.error("exception in yokr - libs_in_use() : %s", err)
        return None


def report_val(param, value, flush=False, report_time=None):
    """
    used to report the @value of @param at @report_time
    @param - string
    @value - float
    @flush - boolean
    @report_time - POSIX time as int or float
    If @report_time is None then current time is used
    if @flush is True the value is stored in an internal persistent database
    (typically SQLite).
    If @flush is False, the value is stored in volatile memory,
    and will be flushed next time any that reported value is flushed.
    """
    try:
        status = True

        try:
            value = float(value)
        except ValueError:
            status = False
            logger.error("yokr::report_val value - number expected," +
                         " received %s", type(value))
        try:
            param = str(param)
        except ValueError:
            status = False
            logger.error("yokr::report_val param - string expected," +
                         " received %s", type(param))
        sys_time = time.time()
        if report_time is None:
            report_time = sys_time
        else:
            try:
                report_time = float(report_time)
            except ValueError:
                status = False
                logger.error("yokr::report_val report_time - unix timestamp" +
                             " expected, received %s", type(report_time))

        if type(flush) != bool:
            status = False
            logger.error("yokr::report_val flush - boolean expected," +
                         "received %s", type(flush))

        if status:
            # Store values in memory
            _yCE.reportLoc += 1
            _yCE.reportVecTime.append(
                    _format_datetime_utc(dt=report_time, with_tz_name=True))
            _yCE.reportVecParam.append(param)
            _yCE.reportVecValue.append(value)
            # Flush if need
            if flush or (_yCE.reportLoc >= _yCE.reportFlushNum) or \
                    (((time.time() - _yCE.reportFlushStartTime) / 60) >=
                        _yCE.reportFlushTime):
                _flush_report()
                _ykrUpdate(df=None, upload=True, removeHistory=False)
        return status
    except Exception as err:
        logger.error("exception in yokr - report_entity_used() : %s", err)
        return False


def report_entity_used(EntityType='', Entity='', Version='', Title='',
                       Description='', License='', Url='',
                       BugReports='', Build='', publication_date=''):
    """
    used to report an entity used that is not automatically detected
    by yokr package
    @EntityType – string one of,
        "Sensor", "OS", "OSLib", "3rdParty", "JavaLib", "RLib",
        "PythonLib", @Entity, @Version, @Title, @Description, @License, @Url,
    @BugReports, @Build, @PublicationDate – all of type string,
        default value “”
    """
    try:
        status = True
        if (type(EntityType) != str or type(Entity) != str or
            type(Version) != str or type(Title) != str or
            type(Description) != str or type(License) != str or
            type(Url) != str or type(BugReports) != str or
                type(Build) != str or type(publication_date) != str):
                status = False
                logger.error("yokr::report_entity_used All the parameters" +
                             "of report_entity_used should be strings")

        entities_supported = LibInfo.SUPPORTED_ENTITIES
        if status and EntityType not in entities_supported:
            status = False
            logger.error("yokr::report_entity_used Unsupported entity" +
                         (" type reported - %s. " % EntityType) +
                         "The following types are supported: " +
                         ", ".join(entities_supported))
        if status:
            lib_info = LibInfo()
            lib_info.HashKey = None
            lib_info.LibVerHashKey = None
            lib_info.EntityType = EntityType
            lib_info.Entity = Entity
            lib_info.Version = Version
            lib_info.Title = Title
            lib_info.Description = Description
            lib_info.License = License
            lib_info.Url = Url
            lib_info.BugReports = BugReports
            lib_info.Build = Build
            lib_info.AddedDate = _ykrNowF()
            lib_info.HashKey =  \
                _ykdGenLibInfoHashKey(EntityType=lib_info.EntityType,
                                      Entity=lib_info.Entity,
                                      Version=lib_info.Version,
                                      License=lib_info.License)
            lib_info.LibVerHashKey =  \
                _ykdGenLibVerHashKey(EntityType=lib_info.EntityType,
                                     Entity=lib_info.Entity,
                                     Version=lib_info.Version,
                                     License=lib_info.License,
                                     Build=lib_info.Build,
                                     PublicationDate=lib_info.PublicationDate,
                                     Title=lib_info.Title,
                                     Description=lib_info.Description)
            _ykrUpdate(df=[lib_info])
    except Exception as err:
        logger.error("exception in yokr - report_val() : %s", err)


def flush_cache(forceUpload=True):
    try:
        _flush_report()
        _ykrUpdate(df=None, upload=True, removeHistory=False,
                   forceUpload=forceUpload)
    except Exception as err:
        logger.error("exception in yokr - flush_cache() : %s", err)


def clean_env():
    """cleans and restarts yokr internal environment and cache"""
    try:
        flush_cache()
        _reloadConfigFiles()
        _ykrCreateCollectorDBIfNeeded(dbPathAndName22=_yCE.dbPathAndName22)
    except Exception as err:
        logger.error("exception in yokr - clean_env() : %s", err)

################   START NEW CODE 2020120

def _ykrQuickUpdateGeneralInfo(cFlag=False,aFlag=False,iFlag=False):
    try:
        con_open = False
        db = sqlite3.connect(_yCE.dbPathAndName22)
        con_open = True
        db.row_factory = sqlite3.Row
        _ykrUpdateGeneralInfo(db=db,cFlag=cFlag,aFlag=aFlag,iFlag=iFlag)
    finally:
        if con_open:
            db.close()

def set_cmp_parms(cmpHashInfoKey=None, cmpHash=None, cmpName=None,
                 cmpNameAlias=None, cmpDescription=None, cmpUUID=None,
                 cmpContactPersonId=None): 
    global _yCE
    try:
        _flush_report()
        if cmpHashInfoKey is not None:
            _yCE.cmpHashInfoKey = cmpHashInfoKey
        if cmpHash is not None:
            _yCE.cmpHash = cmpHash
        if cmpName is not None:
            _yCE. cmpName = cmpName
        if cmpNameAlias is not None:
            _yCE.cmpNameAlias = cmpNameAlias
        if cmpDescription is not None:
            _yCE.cmpDescription = cmpDescription
        if cmpUUID  is not None:
            _yCE.cmpUUID = cmpUUID 
        if cmpContactPersonId is not None:
            _yCE.cmpContactPersonId = cmpContactPersonId
        _ykrQuickUpdateGeneralInfo(cFlag=True)
    except Exception as err:
        logger.error("exception in yokr - set_cmp_params: %s", err)


def set_app_parms(appHashInfoKey=None, appHash=None, appName=None,
                 appNameAlias=None, appDescription=None, appUUID=None,
                 appContactPersonId=None): 
    global _yCE
    try:
        _flush_report()
        if appHashInfoKey is not None:
            _yCE.appHashInfoKey = appHashInfoKey
        if appHash is not None:
            _yCE.appHash = appHash
        if appName is not None:
            _yCE. appName = appName
        if appNameAlias is not None:
            _yCE.appNameAlias = appNameAlias
        if appDescription is not None:
            _yCE.appDescription = appDescription
        if appUUID  is not None:
            _yCE.appUUID = appUUID 
        if appContactPersonId is not None:
            _yCE.appContactPersonId = appContactPersonId
        _ykrQuickUpdateGeneralInfo(aFlag=True)
    except Exception as err:
        logger.error("exception in yokr - set_app_params: %s", err)


def set_inst_parms(instHashInfoKey=None, instHash=None, instName=None,
                 instNameAlias=None, instDescription=None, instUUID=None,
                 instContactPersonId=None): 
    global _yCE
    try:
        _flush_report()
        if instHashInfoKey is not None:
            _yCE.instHashInfoKey = instHashInfoKey
        if instHash is not None:
            _yCE.instHash = instHash
        if instName is not None:
            _yCE. instName = instName
        if instNameAlias is not None:
            _yCE.instNameAlias = instNameAlias
        if instDescription is not None:
            _yCE.instDescription = instDescription
        if instUUID  is not None:
            _yCE.instUUID = instUUID 
        if instContactPersonId is not None:
            _yCE.instContactPersonId = instContactPersonId
        _ykrQuickUpdateGeneralInfo(iFlag=True)
    except Exception as err:
        logger.error("exception in yokr - set_app_params: %s", err)


################   END NEW CODE 2020120

#### TODO add account secret to data in get_status()
def get_status():
    """returns a dictionary with info about the sctaus of the library"""
    ykrInfo = {}
    try:
        style = "%m/%d/%Y, %H:%M:%S"
        ykrInfo = {
                "internalDB": _yCE.dbPathAndName22,
                "companyFile": _yCE.DirCmpFile + "\\.companyDCF.txt",
                "applicationFile": _yCE.DirAppFile + "\\.appDCF.txt",
                "instanceFile": _yCE.DirInstFile + "\\.instDCF.txt",
                "companyUUID": _yCE.cmpUUID,
                "applicationUUID": _yCE.appUUID,
                "instanceUUID": _yCE.instUUID,
                "yokarandaServer API": _yCE.YokarandaServer,
                "local data max retention (days)": _yCE.instDataRetantionDays,
                "upload interval (minutes)": _yCE.uploadInterval,
                "minimal upload interval (including force)":
                    _yCE.uploadIntervalMin,
                "last flush to local repository":
                        datetime.datetime.utcfromtimestamp(_yCE.reportFlushStartTime).strftime(style),
                "Last successful upload to Yokaranda":
                        datetime.datetime.utcfromtimestamp(_yCE.uploadLastTime).strftime(style)
                }
    except Exception as err:
        logger.error("exception in yokr - get_ykr_status() : %s", err)
    finally:
        return(ykrInfo)

_onLoad()

