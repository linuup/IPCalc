import sys

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QApplication, QMainWindow

from ipCalc import availableIpSize, ipMask, ipToIPBin, ipNetAddress, numToBinNum, binNumToDEC_IP
from ui_main import Ui_Form


class mainwindow(Ui_Form, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.IPcalc.clicked.connect(self.calcIpButton)
        # 内容框
        self.content = self.calcDescribe
        self.ip = ""
        # 子网掩码位数
        self.maskNumber = ""
        # 子网掩码
        self.mask = ""
        # 二进制子网掩码
        self.maskBin = ""
        self.ip1.setText("192")
        self.ip2.setText("168")
        self.ip3.setText("0")
        self.ip4.setText("1")
        self.maskNum.setText("20")
        # 限制只能输入数字
        reg = QRegExp('[0-9]+$')
        validator = QRegExpValidator()
        validator.setRegExp(reg)
        self.ip1.setValidator(validator)
        self.ip2.setValidator(validator)
        self.ip3.setValidator(validator)
        self.ip4.setValidator(validator)
        self.maskNum.setValidator(validator)

    def calcIpButton(self):
        self.calcDescribe.clear()
        ip1 = self.ip1.text()
        ip2 = self.ip2.text()
        ip3 = self.ip3.text()
        ip4 = self.ip4.text()
        self.ip = ip1 + "." + ip2 + "." + ip3 + "." + ip4
        self.content.insertPlainText("IP地址：" + str(self.ip) + "\t")
        self.maskNumber = int(self.maskNum.text())
        self.content.insertPlainText("掩码位数：" + str(self.maskNumber) + "\n")
        ipSize = availableIpSize(int(self.maskNumber))
        self.content.insertPlainText("可用地址数量:" + str(ipSize))
        self.availableIpSize.setText(str(ipSize))
        self.maskNumInput()
        self.leftIP_InfoInput()

    # 子网掩码
    def maskNumInput(self):
        info = "掩码位数" + str(self.maskNumber) + "  ->  32位二进制数ip中,前" + str(self.maskNumber) + "位为1,后" + str(
            32 - self.maskNumber) + "位为0\n"
        self.content.insertPlainText("\n\n子网掩码================================\n\n")
        self.content.insertPlainText(info)
        # print("掩码位数%s->32位二进制数ip中,前"+str(self.maskNumber)+"位为1,后"+str(32-self.maskNumber)+"位为0\n")

        mask, maskBin = ipMask(self.maskNumber)
        self.mask = mask
        self.maskBin = maskBin
        self.content.insertPlainText(maskBin)
        self.content.insertPlainText("\n↓\n")
        self.content.insertPlainText(mask)
        self.content.insertPlainText("\n二进制IP转为10进制后就是子网掩码:" + mask)
        maskList = mask.split(".")
        self.maskNum1.setText(maskList[0])
        self.maskNum2.setText(maskList[1])
        self.maskNum3.setText(maskList[2])
        self.maskNum4.setText(maskList[3])

    # 网络地址、广播地址、第一个可用地址、最后一个可用地址
    def leftIP_InfoInput(self):
        self.content.insertPlainText("\n\n网络地址================================\n\n")
        self.content.insertPlainText("\n网络地址是指ip地址的主机位全为0\n")
        self.content.insertPlainText("\n首先将ip的二进制形式与子网掩码的二进制形式进行与运算：\n")
        self.content.insertPlainText("运算规则：\n0&0=0;  0&1=0;   1&0=0;    1&1=1;\n即：两位同时为“1”，结果才为“1”，否则为0\n")
        self.content.insertPlainText(self.ip + "的二进制形式为：\n")
        self.content.insertPlainText(str(self.maskNumber) + "的二进制形式为：\n")

        ipBin = ipToIPBin(self.ip)
        self.content.insertPlainText(ipBin)
        self.content.insertPlainText("\n↓  进行与运算 &(与运算符号) \n")

        self.content.insertPlainText(self.maskBin)
        binNum = numToBinNum(eval('0b' + self.maskBin) & eval('0b' + ipBin))
        if len(binNum) != 32:
            for index in range(0, 32 - len(binNum)):
                binNum = "0" + str(binNum)
        self.content.insertPlainText("\n=\n" + binNum)
        self.content.insertPlainText("\n将上方结果转为10进制IP形式就是网络地址\n")
        info = binNumToDEC_IP(list(binNum))
        self.content.insertPlainText(info)
        maskNum, maskBinNum = ipMask(self.maskNumber)
        netAddress, broadcastAddress, firstIp, lastIp = ipNetAddress(ipBin, maskBinNum, self.maskNumber)
        maskList = netAddress.split(".")
        self.netaddr1.setText(maskList[0])
        self.netaddr2.setText(maskList[1])
        self.netaddr3.setText(maskList[2])
        self.netaddr4.setText(maskList[3])
        self.content.insertPlainText("\n\n广播地址================================\n")
        self.content.insertPlainText("\n广播地址是指ip地址的主机位全为1\n")
        self.content.insertPlainText("\n")
        self.content.insertPlainText(info + "的二进制形式为:\n" + ipToIPBin(info))
        self.content.insertPlainText("\n↓  将后" + str(32 - self.maskNumber) + "位全部设置为1\n")
        info = list(ipToIPBin(info))
        for index in range(0, 32):
            if index >= self.maskNumber:
                info[index] = '1'
        self.content.insertPlainText(''.join(info))
        self.content.insertPlainText("\n转为10进制IP就是广播地址：" + broadcastAddress)

        broadcastAddressList = broadcastAddress.split(".")
        self.guangbo1.setText(broadcastAddressList[0])
        self.guangbo2.setText(broadcastAddressList[1])
        self.guangbo3.setText(broadcastAddressList[2])
        self.guangbo4.setText(broadcastAddressList[3])
        self.content.insertPlainText("\n\n第一个可用地址================================\n\n")
        self.content.insertPlainText("第一个可用地址等于网络地址+1\n")
        self.content.insertPlainText("网络地址：\n" + netAddress + "\n")
        self.content.insertPlainText(ipToIPBin(netAddress))
        self.content.insertPlainText("\n↓  +1\n")
        self.content.insertPlainText(ipToIPBin(firstIp))
        self.content.insertPlainText("\n第一个可用地址：" + firstIp)
        firstIpList = firstIp.split(".")
        self.firstIP1.setText(firstIpList[0])
        self.firstIP2.setText(firstIpList[1])
        self.firstIP3.setText(firstIpList[2])
        self.firstIP4.setText(firstIpList[3])
        self.content.insertPlainText("\n\n最后一个可用IP地址================================\n\n")
        self.content.insertPlainText("第一个可用地址等于广播地址-1\n")
        self.content.insertPlainText("广播地址：\n" + broadcastAddress + "\n")
        self.content.insertPlainText(ipToIPBin(broadcastAddress))
        self.content.insertPlainText("\n↓  -1\n")
        self.content.insertPlainText(ipToIPBin(lastIp))
        self.content.insertPlainText("\n最后一个可用地址：" + lastIp)
        lastIpList = lastIp.split(".")
        self.lastIP1.setText(lastIpList[0])
        self.lastIP2.setText(lastIpList[1])
        self.lastIP3.setText(lastIpList[2])
        self.lastIP4.setText(lastIpList[3])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainwindow()
    sys.exit(app.exec_())
