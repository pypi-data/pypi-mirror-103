import asyncio
import binascii
import gzip
import hashlib
import http.cookiejar
import json
import logging
import os
import shutil
import subprocess
import time
import urllib
import random

_loggerName = 'beniutils'


def bInitLogger(loggerName=None, loggerLevel=None, logFile=None):
    LOGGER_FORMAT = '%(asctime)s %(levelname)-1s %(message)s', '%Y-%m-%d %H:%M:%S'
    LOGGER_LEVEL = loggerLevel or logging.INFO
    LOGGER_LEVEL_NAME = {
        logging.DEBUG: 'D',
        logging.INFO: '',
        logging.WARNING: 'W',
        logging.ERROR: 'E',
        logging.CRITICAL: 'C',
    }

    if loggerName:
        global _loggerName
        _loggerName = loggerName

    logger = logging.getLogger(_loggerName)
    logger.setLevel(LOGGER_LEVEL)
    for loggingLevel, value in LOGGER_LEVEL_NAME.items():
        logging.addLevelName(loggingLevel, value)

    loggerFormatter = logging.Formatter(*LOGGER_FORMAT)

    loggerHandler = logging.StreamHandler()
    loggerHandler.setFormatter(loggerFormatter)
    loggerHandler.setLevel(LOGGER_LEVEL)
    logger.addHandler(loggerHandler)

    if logFile:
        bMakeFolder(os.path.dirname(logFile))
        fileLoggerHandler = logging.FileHandler(logFile)
        fileLoggerHandler.setFormatter(loggerFormatter)
        fileLoggerHandler.setLevel(LOGGER_LEVEL)
        logger.addHandler(fileLoggerHandler)


def bDebug(msg, *args, **kwargs):
    logging.getLogger(_loggerName).debug(msg, *args, **kwargs)


def bInfo(msg, *args, **kwargs):
    logging.getLogger(_loggerName).info(msg, *args, **kwargs)


def bWarning(msg, *args, **kwargs):
    logging.getLogger(_loggerName).warning(msg, *args, **kwargs)


def bError(msg, *args, **kwargs):
    logging.getLogger(_loggerName).error(msg, *args, **kwargs)


def bCritical(msg, *args, **kwargs):
    logging.getLogger(_loggerName).critical(msg, *args, **kwargs)


def bGetPath(basePath, extendPath):
    return os.path.abspath(os.path.join(basePath, extendPath))


def bWriteFile(file, data, encoding='utf8', newline='\n'):
    bMakeFolder(os.path.dirname(file))
    with open(file, 'w', encoding=encoding, newline=newline) as f:
        f.write(data)
        f.flush()
        f.close()


def bWriteBinFile(file, data):
    bMakeFolder(os.path.dirname(file))
    with open(file, 'wb') as f:
        f.write(data)
        f.flush()
        f.close()


def bReadFile(file, encoding='utf8', newline='\n'):
    with open(file, 'r', encoding=encoding, newline=newline) as f:
        data = f.read()
        f.close()
    return data


def bReadBinFile(file):
    with open(file, 'rb') as f:
        data = f.read()
        f.close()
    return data


def bJsonDumps(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def bRemove(fileOrFolder):
    if bIsFile(fileOrFolder):
        os.remove(fileOrFolder)
    elif bIsFolder(fileOrFolder):
        shutil.rmtree(fileOrFolder)


def bMakeFolder(folder):
    if not bIsExists(folder):
        os.makedirs(folder)


def bClearFolder(*folderAry):
    for folder in folderAry:
        if bIsFolder(folder):
            for target in bGetFileAndFolderList(folder):
                bRemove(target)


def bCopy(fromFileOrFolder, toFileOrFolder):
    if bIsFile(fromFileOrFolder):
        fromFile = fromFileOrFolder
        toFile = toFileOrFolder
        bMakeFolder(bGetParentFolder(toFile))
        shutil.copyfile(fromFile, toFile)
    elif bIsFolder(fromFileOrFolder):
        fromFolder = fromFileOrFolder
        toFolder = toFileOrFolder
        bMakeFolder(bGetParentFolder(toFolder))
        shutil.copytree(fromFolder, toFolder)


def bRename(fromFileOrFolder, toFileOrFolder):
    if bIsFile(fromFileOrFolder):
        fromFile = fromFileOrFolder
        toFile = toFileOrFolder
        os.renames(fromFile, toFile)
    elif bIsFolder(fromFileOrFolder):
        fromFolder = fromFileOrFolder
        toFolder = toFileOrFolder
        os.renames(fromFolder, toFolder)


def bGetParentFolder(fileOrFolder, level=1):
    result = fileOrFolder
    while level > 0:
        level -= 1
        result = os.path.dirname(result)
    return result


def bGetFileExtName(file):
    return file[file.rfind('.') + 1:].lower()


def bIsFile(file):
    return os.path.isfile(file)


def bIsFolder(folder):
    return os.path.isdir(folder)


def bIsExists(fileOrFolder):
    return os.path.exists(fileOrFolder)


def bGetFileList(folder):
    ary = []
    for targetName in os.listdir(folder):
        target = os.path.join(folder, targetName)
        if bIsFile(target):
            ary.append(target)
    return ary


def bGetFolderList(folder):
    ary = []
    for targetName in os.listdir(folder):
        target = os.path.join(folder, targetName)
        if bIsFolder(target):
            ary.append(target)
    return ary


def bGetFileAndFolderList(folder):
    ary = []
    for targetName in os.listdir(folder):
        target = os.path.join(folder, targetName)
        ary.append(target)
    return ary


def bGetAllFileList(folder):
    ary = []
    for targetName in bGetFileAndFolderList(folder):
        target = os.path.join(folder, targetName)
        if bIsFile(target):
            ary.append(target)
        elif bIsFolder(target):
            ary.extend(bGetAllFileList(target))
    return ary


def bGetAllFolderList(folder):
    ary = []
    for targetName in bGetFileAndFolderList(folder):
        target = os.path.join(folder, targetName)
        if bIsFolder(target):
            ary.append(target)
            ary.extend(bGetAllFolderList(target))
    return ary


def bGetAllFileAndFolderList(folder):
    ary = []
    for targetName in bGetFileAndFolderList(folder):
        target = os.path.join(folder, targetName)
        if bIsFile(target):
            ary.append(target)
        elif bIsFolder(target):
            ary.append(target)
            ary.extend(bGetAllFileAndFolderList(target))
    return ary


def bGetFileMD5(file):
    data = bReadBinFile(file)
    return hashlib.md5(data).hexdigest()


def bGetFileCRC32(file):
    data = bReadBinFile(file)
    return binascii.crc32(data)


def bGetFileCRCHex(file):
    return hex(bGetFileCRC32(file))[2:].zfill(8)


def bGetContentCRCHex(content):
    return hex(binascii.crc32(content.encode()))[2:].zfill(8)


def bGetClassFullName(classItem):
    return getattr(classItem, '__module__') + '.' + getattr(classItem, '__name__')


def bExecute(*pars):
    p = subprocess.Popen(
        ' '.join(pars),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    outBytes, errBytes = p.communicate()
    p.kill()
    return p.returncode, outBytes, errBytes


def bExecuteWinScp(winscpExe, winscpKeyFile, server, commandAry):
    logFile = os.path.join(os.path.dirname(winscpExe), 'temp.log')
    bMakeFolder(os.path.dirname(logFile))
    ary = [
        'option batch abort',
        'option transfer binary',
        'open sftp://%s -privatekey=%s' % (server, winscpKeyFile),
    ]
    ary += commandAry
    ary += [
        'close',
        'exit',
    ]
    bRemove(logFile)
    # /console
    cmd = '%s /log=%s /loglevel=0 /command %s' % (
        winscpExe,
        logFile,
        ' '.join('"%s"' % x for x in ary),
    )
    bExecute(cmd)


def bZipFile(toFile, fileFolderOrAry, rename=None):
    from zipfile import ZipFile, ZIP_DEFLATED
    bMakeFolder(os.path.dirname(toFile))
    ary = fileFolderOrAry
    if type(ary) != list:
        ary = [fileFolderOrAry]
    rename = rename or (lambda x: os.path.basename(x))
    with ZipFile(toFile, 'w', ZIP_DEFLATED) as f:
        for file in sorted(ary):
            fname = rename(file)
            f.write(file, fname)


def bZipFileForFolder(toFile, folder, rename=None, filterFun=None):
    if not folder.endswith(os.path.sep):
        folder += os.path.sep
    rename = rename or (lambda x: x[len(folder):])
    ary = bGetAllFileAndFolderList(folder)
    if filterFun:
        ary = list(filter(filterFun, ary))
    bZipFile(toFile, ary, rename)


def bZipFileExtract(file, toFolder=None):
    from zipfile import ZipFile
    toFolder = toFolder or os.path.dirname(file)
    with ZipFile(file) as f:
        for subFile in sorted(f.namelist()):
            try:
                # zipfile 代码中指定了cp437，这里会导致中文乱码
                encodeSubFile = subFile.encode('cp437').decode('gbk')
            except:
                encodeSubFile = subFile
            toFile = os.path.join(toFolder, encodeSubFile)
            toFile = toFile.replace('/', os.path.sep)
            f.extract(subFile, toFolder)
            # 处理压缩包中的中文文件名在windows下乱码
            if subFile != encodeSubFile:
                bRename(os.path.join(toFolder, subFile), toFile)


def bSyncFolder(fromFolder, toFolder):
    # 删除多余目录
    toSubFolderList = sorted(bGetAllFolderList(toFolder), reverse=True)
    for toSubFolder in toSubFolderList:
        fromSubFolder = os.path.join(fromFolder, toSubFolder[len(toFolder + os.path.sep):])
        if not os.path.isdir(fromSubFolder):
            bRemove(toSubFolder)
    # 删除多余文件
    toFileList = bGetAllFileList(toFolder)
    for toFile in toFileList:
        fromFile = os.path.join(fromFolder, toFile[len(toFolder + os.path.sep):])
        if not os.path.isfile(fromFile):
            bRemove(toFile)
    # 同步文件
    fromFileList = bGetAllFileList(fromFolder)
    for fromFile in fromFileList:
        toFile = os.path.join(toFolder, fromFile[len(fromFolder + os.path.sep):])
        if os.path.isfile(toFile):
            fromData = bReadBinFile(fromFile)
            toData = bReadBinFile(toFile)
            if fromData != toData:
                bWriteBinFile(toFile, fromData)
        else:
            bRemove(toFile)
            bCopy(fromFile, toFile)
    # 添加新增目录
    fromSubFolderList = sorted(bGetAllFolderList(fromFolder), reverse=True)
    for fromSubFolder in fromSubFolderList:
        toSubFolder = os.path.join(toFolder, fromSubFolder[len(fromFolder + os.path.sep):])
        if not os.path.isdir(toSubFolder):
            bMakeFolder(toSubFolder)


def bSendMail(host, password, fromMail, toMailList, subject, content='', attachmentList=None):
    '''发送邮件 attachmentList格式为[(name, bytes), ...]'''

    from email.header import Header
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib

    message = MIMEMultipart()
    message['From'] = fromMail
    message['To'] = ','.join(toMailList)
    message['Subject'] = Header(subject, 'utf-8')
    message.attach(MIMEText(content, 'plain', 'utf-8'))

    if attachmentList:
        for item in attachmentList:
            att = MIMEText(item[1], 'base64', 'utf-8')
            att['Content-Type'] = 'application/octet-stream'
            # att['Content-Disposition'] = 'attachment; filename="file.txt"'
            att.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', item[0]))
            message.attach(att)

    smtpObj = smtplib.SMTP_SSL()
    smtpObj.connect(host)
    smtpObj.login(fromMail, password)
    smtpObj.sendmail(fromMail, toMailList, message.as_string())


_DEFAULT_FMT = '%Y-%m-%d %H:%M:%S'


def bTimestampByStr(value, fmt=None):
    fmt = fmt or _DEFAULT_FMT
    return int(time.mktime(time.strptime(value, fmt)))


def bStrByTimestamp(timestamp=None, fmt=None):
    timestamp = timestamp or time.time()
    fmt = fmt or _DEFAULT_FMT
    ary = time.localtime(timestamp)
    return time.strftime(fmt, ary)

# ---- http


_defaultHeader = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}

# Cookie
_cookie = http.cookiejar.CookieJar()
_cookieProc = urllib.request.HTTPCookieProcessor(_cookie)
_opener = urllib.request.build_opener(_cookieProc)
urllib.request.install_opener(_opener)


def _getHeaderByDefault(headers):
    result = dict(_defaultHeader)
    if headers:
        for key, value in headers.items():
            result[key] = value
    return result


def bHttpGet(url, headers=None, timeout=30, retry=3):
    method = 'GET'
    headers = _getHeaderByDefault(headers)
    result = None
    response = None
    currentTry = 0
    while currentTry < retry:
        currentTry += 1
        try:
            request = urllib.request.Request(url=url, headers=headers, method=method)
            response = urllib.request.urlopen(request, timeout=timeout)
            result = response.read()
            response.close()
            break
        except Exception:
            pass
    contentEncoding = response.headers.get('Content-Encoding')
    if contentEncoding == 'gzip':
        result = gzip.decompress(result)
    return result, response


def bHttpPost(url, data=None, headers=None, timeout=30, retry=3):
    method = 'POST'
    headers = _getHeaderByDefault(headers)
    postData = data
    if type(data) == dict:
        postData = urllib.parse.urlencode(data).encode()
    result = None
    response = None
    currentTry = 0
    while currentTry < retry:
        currentTry += 1
        try:
            request = urllib.request.Request(url=url, data=postData, headers=headers, method=method)
            response = urllib.request.urlopen(request, timeout=timeout)
            result = response.read()
            response.close()
            break
        except Exception:
            pass
    return result, response


_maxAsyncFileNum = 5000
_currentAsyncFileNum = 0
_waitAsyncFileTime = 0.5


def bSetAsyncFileMaxNum(value):
    global _maxAsyncFileNum
    _maxAsyncFileNum = value


def bToFloat(value, default):
    result = default
    try:
        result = float(value)
    except:
        pass
    return result


def bToInt(value, default):
    result = default
    try:
        result = int(value)
    except:
        pass
    return result


_xPar = "0123456789abcdefghijklmnopqrstuvwxyz"


def bIntToX(value):
    n = len(_xPar)
    return ((value == 0) and "0") or (bIntToX(value // n).lstrip("0") + _xPar[value % n])


def bXToInt(value):
    return int(value, len(_xPar))


async def bAsyncWriteFile(file, data, encoding='utf8', newline='\n'):
    import aiofiles
    bMakeFolder(os.path.dirname(file))
    global _currentAsyncFileNum
    while _currentAsyncFileNum > _maxAsyncFileNum:
        await asyncio.sleep(_waitAsyncFileTime)
    _currentAsyncFileNum += 1
    async with aiofiles.open(file, 'w', encoding=encoding, newline=newline) as f:
        await f.write(data)
        await f.flush()
        await f.close()
    _currentAsyncFileNum -= 1


async def bAsyncWriteBinFile(file, data):
    import aiofiles
    bMakeFolder(os.path.dirname(file))
    global _currentAsyncFileNum
    while _currentAsyncFileNum > _maxAsyncFileNum:
        await asyncio.sleep(_waitAsyncFileTime)
    _currentAsyncFileNum += 1
    async with aiofiles.open(file, 'wb') as f:
        await f.write(data)
        await f.flush()
        await f.close()
    _currentAsyncFileNum -= 1


async def bAsyncReadFile(file, encoding='utf8', newline='\n'):
    import aiofiles
    global _currentAsyncFileNum
    while _currentAsyncFileNum > _maxAsyncFileNum:
        await asyncio.sleep(_waitAsyncFileTime)
    _currentAsyncFileNum += 1
    async with aiofiles.open(file, 'r', encoding=encoding, newline=newline) as f:
        data = await f.read()
        await f.close()
    _currentAsyncFileNum -= 1
    return data


async def bAsyncReadBinFile(file):
    import aiofiles
    global _currentAsyncFileNum
    while _currentAsyncFileNum > _maxAsyncFileNum:
        await asyncio.sleep(_waitAsyncFileTime)
    _currentAsyncFileNum += 1
    async with aiofiles.open(file, 'rb') as f:
        data = await f.read()
        await f.close()
    _currentAsyncFileNum -= 1
    return data


async def bAsyncOpenXlsx(file):
    import xlrd
    data = await bAsyncReadBinFile(file)
    return xlrd.open_workbook(file_contents=data, formatting_info=True)
    # 只提供了异步打开xlsx的方法，没有提供异步写入xlsx的方法，因为xlwt不支持


async def bAsyncGetFileMD5(file):
    data = await bAsyncReadBinFile(file)
    return hashlib.md5(data).hexdigest()


async def bAsyncGetFileCRC32(file):
    data = await bAsyncReadBinFile(file)
    return binascii.crc32(data)


async def bAsyncGetFileCRCHex(file):
    return hex(await bAsyncGetFileCRC32(file))[2:].zfill(8)


async def bAsyncExecute(*parList):
    # 注意：针对windows，版本是3.8以下需要使用asyncio.subprocess，在执行main之前就要执行
    # 注意：在3.7如果调用对aiohttp有异常报错
    # asyncio.set_event_loop_policy(
    #    asyncio.WindowsProactorEventLoopPolicy()
    # )

    proc = await asyncio.create_subprocess_shell(
        ' '.join(parList),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return proc.returncode, stdout, stderr


_maxAsyncHttpNum = 1000
_currentAsyncHttpNum = 0
_waitAsyncHttpTime = 0.5


def bSetAsyncHttpMaxNum(value):
    global _maxAsyncHttpNum
    _maxAsyncHttpNum = value


async def bAsyncHttpGet(url, headers=None, timeout=30, retry=3):
    import aiohttp
    global _currentAsyncHttpNum
    headers = _getHeaderByDefault(headers)
    result = None
    response = None
    currentTry = 0
    while _currentAsyncHttpNum >= _maxAsyncHttpNum:
        await asyncio.sleep(_waitAsyncHttpTime)
    _currentAsyncHttpNum += 1
    while currentTry < retry:
        currentTry += 1
        try:
            response = None
            # todo: session 做close操作
            async with aiohttp.ClientSession() as session:
                response = await session.get(
                    url,
                    headers=headers,
                    timeout=timeout,
                )
                result = await response.read()
                response.close()
                await session.close()
                if not result:
                    continue
                break
        except Exception:
            if response:
                response.close()
            bWarning(f'async http get exception url={url} times={currentTry}')
    _currentAsyncHttpNum -= 1
    return result, response


async def bAsyncHttpPost(url, data=None, headers=None, timeout=30, retry=3):
    import aiohttp
    global _currentAsyncHttpNum
    headers = _getHeaderByDefault(headers)
    result = None
    response = None
    currentTry = 0
    while _currentAsyncHttpNum >= _maxAsyncHttpNum:
        await asyncio.sleep(_waitAsyncHttpTime)
    _currentAsyncHttpNum += 1
    while currentTry < retry:
        currentTry += 1
        try:
            response = None
            # todo: session 做close操作
            async with aiohttp.ClientSession() as session:
                response = await session.post(
                    url,
                    data=data,
                    headers=headers,
                    timeout=timeout,
                )
                result = await response.read()
                response.close()
                await session.close()
                if not result:
                    continue
                break
        except Exception:
            if response:
                response.close()
            bWarning(f'async http get exception url={url} times={currentTry}')
    _currentAsyncHttpNum -= 1
    return result, response


def ptScrapy(urlList, parseFun, extendSettings=None):

    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.log import get_scrapy_root_handler
    import scrapy.http

    resultList = []
    resultUrlList = urlList[:]

    class TempSpider(scrapy.Spider):

        name = str(random.random())
        start_urls = urlList

        def parse(self, response):
            itemList, urlList = parseFun(response)
            if itemList:
                resultList.extend(itemList)
            if urlList:
                for url in urlList:
                    resultUrlList.append(url)
                    yield scrapy.http.Request(url)

    settings = {
        'LOG_LEVEL': logging.INFO,
        'LOG_FORMAT': '%(asctime)s %(levelname)-1s %(message)s',
        'LOG_DATEFORMAT': '%Y-%m-%d %H:%M:%S',
        'DOWNLOAD_TIMEOUT': 5,
        'CONCURRENT_REQUESTS': 50,
        'RETRY_HTTP_CODES': [514],
        'RETRY_TIMES': 5,
        # 'ITEM_PIPELINES': {
        #    ptGetClassFullName( TempPipeline ): 300,
        # },
    }
    if extendSettings:
        for k, v in extendSettings.items():
            settings[k] = v

    process = CrawlerProcess(settings)
    process.crawl(TempSpider)
    process.start()

    rootHandler = get_scrapy_root_handler()
    if rootHandler:
        rootHandler.close()

    # 函数执行后再调用logging都会有2次显示在控制台
    logging.getLogger().handlers = []

    return resultList, resultUrlList


if __name__ == '__main__':
    pass
