# ip返回二进制ip地址
def ipToIPBin(ip):
    ipBin = ""
    for content in ip.split("."):
        contentBin = numToBinNum(int(content))
        zeroSize = 8 - len(contentBin)
        for i in range(0, zeroSize):
            contentBin = "0" + contentBin
        ipBin = ipBin + contentBin
    return ipBin


# 数字转二进制形式，不带0b
def numToBinNum(num):
    return bin(num).replace('0b', '')

# 32位二进制ip转10进制ip
def binNumToDEC_IP(binNumList):
    # 掩码十进制
    maskNum = ""
    step = 8
    current = 0
    for index in range(0, 4):
        tmp = ""
        for i in range(current, step):
            tmp = tmp + binNumList[i]
        if index == 3:
            maskNum = maskNum + str(eval('0b' + tmp))
        else:
            maskNum = maskNum + str(eval('0b' + tmp)) + "."
        current = step
        step = step + 8
    return maskNum


# 根据掩码位数返回子网掩码
def ipMask(maskSize):
    # 掩码二进制
    maskBinNumber = ""
    # 网络号位数
    for netNumber in range(0, maskSize):
        maskBinNumber = "1" + maskBinNumber
    # 主机号
    suf = ""
    for userNum in range(0, 32 - maskSize):
        suf = "0" + suf
    maskBinNumber = maskBinNumber + suf
    maskNum = binNumToDEC_IP(list(maskBinNumber))
    return maskNum, maskBinNumber


# 返回网络地址、广播地址、第一个可用地址、最后一个可用地址
def ipNetAddress(ipBin, maskBin, maskNum):
    binNum = numToBinNum(eval('0b' + maskBin) & eval('0b' + ipBin))
    if len(binNum) is not 32:
        for index in range(0, 32-len(binNum)):
            binNum = "0"+str(binNum)
    # 网络地址
    ipList = list(binNum)
    # 第一个可用地址
    firstIpList = ipList.copy()
    firstIpList[31] = "1"
    # 广播地址
    broadcastAddressList = ipList.copy()
    for index in range(0, 32):
        if index >= maskNum:
            broadcastAddressList[index] = '1'
    # 最后一个可用地址
    lastIpList = broadcastAddressList.copy()
    lastIpList[31] = "0"
    return binNumToDEC_IP(ipList), binNumToDEC_IP(broadcastAddressList), binNumToDEC_IP(firstIpList), binNumToDEC_IP(lastIpList)


# 可用地址数量
def availableIpSize(maskNum):
    return 2**(32-maskNum)-2
