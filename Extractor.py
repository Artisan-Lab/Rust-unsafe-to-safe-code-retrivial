import time


#代码块node,node of code block
class Node (object):
    def __init__(self, index,Range,layer,data):
        """链表中节点结构，只有data和next，多跳转情况下需调整
            :param data:
            :return:
        """
        self.index = index#每个node的唯一编号。编号顺序按深度优先
        self.Range = Range#该代码块在原字符串中坐标范围
        self.data = data
        self.title = None#代码块的(左括号前&上一条语句之后的)语句
        self.label = []#用于存储该代码块的控制语句，由于嵌套可能存在，故将label定义为数组.其值为[(index,condition),...]
        self.layer =layer#相对于程序入口，该代码块的嵌套层数
        self.findScope = None  # 代码块中寻找标签的源代码中的范围
        self.kind = (self.layer,self.title) #kind标记了这个node的属性，是一个元组(层数，类型）如(0,fn)(1,if)(1,else)
        self.next = []
        self.pre = []#Node中节点上下连接Node的index存放在next和pre数组中

    def getKindCondition(self):
        #得到kind中第二个元素
        return self.kind[1]
    def getKindLayer(self):
        #得到kind中第1个元素
        return self.kind[0]

    def getIthLabel(self,i):
        """得到该node的label中第i个元素中的第二个元素，即label字符串"""
        str = ""
        if i<0 or i>len(self.label):
            print("ERROR:i<0 or i>len(self.label)")
        else:
            str = self.label[i][1]
        return str

    def getIthLabelIndex(self,i):
        """得到该node的label中第i个元素中的第1个元素，即该label对应节点的index"""
        str = None
        if i<0 or i>len(self.label):
            print("ERROR:i<0 or i>len(self.label)")
        else:
            str = self.label[i][0]
        return str

    def show(self):
        print("--layer:\t\t{}".format(self.layer))
        print("--index:\t\t{}".format(self.index))
        print("--findScope:\t{}".format(self.findScope))
        print("--title:\t\t{}".format(self.title))
        print("--kind:\t\t{}".format(self.kind))
        print("--Range:\t\t{}".format(self.Range))
        print("--data:\t\t{}".format(self.data))
        print("--label:\t\t{}".format(self.label))

    def showPartly(self):
        print("--index:\t\t{}".format(self.index))
        print("--layer:\t\t{}".format(self.layer))
        print("--title:\t\t{}".format(self.title))
        print("--kind:\t\t{}".format(self.kind))
        print("--label:\t\t{}".format(self.label))
#用于管理一份代码的所有codeBlock（即node）
class codeBlockList(object):
    def __init__(self):
        self.nodelist = []
        self.length = 0

    def append(self,node):
        self.nodelist.append(node)
        self.getLength()

    def getLength(self):
        self.length = len(self.nodelist)
        return self.length

    def getNodeByIndex(self,i):
        if i<0 or i>= self.length:
            print("ERROR:index out of range")
            return None
        else:
            return self.nodelist[i]

    def calFindScope(self, content):
        #确定各个节点的label计算范围，并赋值title以及kind
        #range index of content
        start = 0
        showFlag = False#控制是否输出中间工程
        end = len(content)-1
        #遍历nodelist，确定各个节点寻找关键字的范围。被遍历的nodelist应是被sortByBraceOrder排序过的
        for i in range(len(self.nodelist)):#i是node的index
            #这里默认输入代码块是一个函数，或者最外层是被一对大括号包括起来的代码块
            #关键字范围对应该代码块左括号之前的第一条语句
            if showFlag:
                print("--------findScope of node %d------------" % i)
            if i == 0:
                r = self.nodelist[i].Range
                self.nodelist[i].findScope = (start,r[0])#寻找范围不包括本代码块的括号
                if showFlag:
                    print("findScope is \n\t{}".format(self.nodelist[i].findScope))
                    print("the string of findScope in sorce code is \n\t{}".format(content[start:r[0]]))
                self.nodelist[i].title = content[start:r[0]]
                self.changeKind(i)#title赋值完，给kind赋值
                start = r[0]#下次搜索的起始寻找范围不包括本代码块的括号
            else:
                r = self.nodelist[i].Range
                tempscope = (start, r[0])#上个代码块开始的地方，到这个代码块开始的地方
                # print("tempscope is \n\t{}".format(tempscope))
                # print("tempscope is \n\t{}".format(content[start:r[0]]))
                for j in range(r[0]-1,start,-1):#range是左闭右开，所以不包含本代码块的括号
                    #在这个范围内寻找;{}进一步缩小范围，且不包含这些符号
                    if content[j] == ';' or content[j] == '{' or content[j] == '}':
                        start = j+1
                        break
                self.nodelist[i].findScope = (start,r[0])
                if showFlag:
                    print("findScope is \n\t{}".format(self.nodelist[i].findScope))
                    print("the string of findScope in sorce code is \n\t{}".format(content[start:r[0]]))
                self.nodelist[i].title = content[start:r[0]]
                self.changeKind(i)  # title赋值完，给kind赋值
                start = r[0]

            pass
        return

    def changeKind(self,index):
        #通过title为改节点的kind赋值
        #---------------todo 以后可能在这里创建关键字列表（字典）------------------
        temp = self.nodelist[index].title
        layer = self.nodelist[index].layer#kind = (layer,string)
        #else if 关键字比较特殊，优先查找else if，如果找到了，则return
        dic0 = ["else if"]
        for string in dic0:
            pos = -1
            pos = temp.find(string)
            if pos >= 0:
                self.nodelist[index].kind = (layer, string)
                return
            else:
                continue


        #todo 未考虑判读语句中带有字符串的情形，如if str == "if else else if"
        dic1 = ["if","else","fn"]
        for string in dic1:
            pos = -1
            pos = temp.find(string)
            if pos>=0:
                self.nodelist[index].kind = (layer,string)
                break
            else:
                continue


        return

    def changeLabel(self,tempnode):
        """将tempnode中对应label写入cbList中对应label中"""
        self.nodelist[tempnode.index].label = tempnode.label
        return

    def labelTransform(self):
        """将自身中节点得到的label进行整理，并且可以由label得到cfg"""
        print("-----------in labelTransform--------------")
        lnodeList = self.getLength()
        #todo
        for i in range(lnodeList):
            lLabel = len(self.nodelist[i].label)
            tempNode = self.nodelist[i]
            #else块最后一个标签必为else
            if tempNode.title == "else":
                #tempLayer = tempNode.layer
                start = -1#找出同层if,由于label数组中只存了节点index，无layer信息，故找不到同层if；则逆序找到相邻最近if即可
                for j in range(lLabel-1,-1,-1):
                    id = tempNode.label[j][0]
                    print("id is %d"% id)
                    print("self.nodelist[id].getKindCondition is\n{}".format(self.nodelist[id].getKindCondition()))
                    if self.nodelist[id].getKindCondition() == "if":
                        start = j
                        break
                    else:
                        continue
                if start == -1:
                    print("ERROR:there is no label 'if' in the label list")
                #将标签组合，并生成新的label数组
                newLabel = []
                lastLabel = tempNode.label[lLabel-1]#取最后一个节点，即else节点
                print("start is %d" % start)
                #遇到templabel之前的label照搬，遇到同层if之后开始合并
                for k in range(lLabel-1):#不包含最后一个else节点
                    print("k is %d" % k)
                    if k<start:
                        newLabel.append(tempNode.label[k])
                        print("k label is {}".format(tempNode.label[k]))

                    if k>=start:
                        string = lastLabel[1]#取最后一个label的字符串部分
                        index = tempNode.label[k][0]
                        index = str(index)
                        condition = tempNode.label[k][1]
                        string = string+"-Index:"+index+",Condition:"+condition
                        lastLabel = (lastLabel[0],string)

                newLabel.append(lastLabel)
                self.nodelist[i].label = newLabel

            else:
                #不为else的节点无需处理
                pass

            pass
        return

    def clearTitleString(self):
        """用于清除条件语句中的空格、回车符等无效字符"""

        #todo 暂未考虑判断条件中有字符串的情况
        l = self.getLength()
        # todo
        for i in range(l):
            t = self.nodelist[i].title
            if t == None:
                print("ERROR: title is None")
                continue
            else:
                #去掉回车与\t
                t = t.replace("\n","")
                t = t.replace("\t","")
                t = t.replace("\r", "")
                #t = t.replace(" ", "")
                #去除空格
                start = -1
                flag1 = False#如果前方一直是空格，到i处不为空格，则flag1=True，start = i-1
                end = -1
                flag2 = False
                l = len(t)
                for j in range(l):
                    if flag1:
                        start = j - 1
                        break
                    if t[j] == " ":
                        flag1 = False
                    else:
                        flag1 = True
                #逆序循环，range（起始，终止，-1表示逆序）左闭右开
                for k in range(l-1,-1,-1):
                    if flag2:
                        end = k + 1
                        break
                    if t[k] == " ":
                        flag2 = False
                    else:
                        flag2 = True
                if start > -1 and end > -1:
                    t = t[start:end+1]#切片左闭右开，所以end+1
                else:
                    print("ERROR: in clearTitleString")
                self.nodelist[i].title = t
                print("title of node %d is :" % i)
                print("---{}---".format(self.nodelist[i].title))


        return

    def show(self):
        for j in range(len(self.nodelist)):
            print("-----------codeBlock%d---------------" % j)
            self.nodelist[j].show()
            print("------------------------------------")

    def showPartly(self):
        for j in range(len(self.nodelist)):
            print("-----------codeBlock%d---------------" % j)
            self.nodelist[j].showPartly()
            print("------------------------------------")

    #各代码块顺序按在文件中的顺序排列,并改变index
    def sortByBraceOrder(self):
        self.nodelist.sort(key=self.takeNodeBrace)
        for j in range(len(self.nodelist)):
            # print("-----------codeBlock%d---------------" % j)
            self.nodelist[j].index = j
            # print("---------------------------")

    def takeNodeBrace(self,elem):
        return elem.Range[0]

#用于生成node的label的数据结构
class LabelNode(object):
    def __init__(self,layer):
        self.value = []#用于存储该代码块的控制语句，由于嵌套可能存在，故将value定义为数组.其值为[(condition，index),...]
        #由于是深度优先，所以当有深层嵌套时，next必有值
        self.top = -1#初始时栈指针指向栈底
        self.layer = layer#label是第几层嵌套的label，一层对应一个labelnode

        self.next = None

    def show(self):
        print("value of this LabelNode is {}".format(self.value))
        print("layer of this LabelNode is {}".format(self.layer))

    def push(self):
        return
#动态单链表，用于labelnode生成为每个代码块node生成label
class LabelLinklist(object):

    def __init__(self):
        # 初始化空表
        self.head = None

    def __len__(self)->int:
        # 获取当前表长
        pre = self.head
        length = 0
        while pre:
            length += 1
            pre = pre.next
        return length

    def show(self):
        pre = self.head
        while pre:
            pre.show()
            pre = pre.next
        return

    def append(self,labelnode):
        """
            追加节点，需要新建节点（多跳转情况下需调整）\n
            1.head 为none :head-->node\n
            2.tail.next-->node\n
            :param data:
            :return:
        """
        new_node = labelnode

        #若为空表，则新节点为表头
        if self.head == None:
            self.head = new_node
        #若不为空表，则向最后节点的next指向新节点
        else:
            pre = self.head
            while pre.next:
                pre = pre.next
            pre.next = new_node
        return

    def get(self, index):
        """目前仅适合单链表，根据索引返回节点，多跳转情况下需调整
        :param index:
        :return: node or None
        """
        index = index if index >= 0 else len(self) + index
        #index为负数则为从后往前数
        #index = index if index >= 0 else size + index

        if len(self) < index or index < 0:
            return None
        pre = self.head
        while index:
            pre = pre.nex
            index -= 1
        return pre

    def set(self, index, data):
        """根据index更新节点data
        """
        node = self.get(index)
        if node:
            node.data = data
        return node
#生成label可以利用之前的codeBlockList加上栈可以解决
class LabeStack(object):
    def __init__(self,nodelist):
        self.nodelist = nodelist
        self.length = 0
        self.top = -1
        self.stack = []
        self.nodelistIsEmpty = False#标记进栈队列是否为空，若元素全部进栈，该字段为true

    def isEmpty(self)->bool:
        if self.top == -1:
            return True
        elif self.top > -1:
            return False
        else:
            print("ERROR: 栈底指针异常，top<-1")
            return False

    def getTopItem(self):
        if self.top>-1:
            return self.stack[self.top]
        else:
            print("ERROR: the stack is empty")
            return False

    def getItem(self,index):
        """get item by index"""
        if index>-1:
            return self.stack[index]
        else:
            print("ERROR: the stack is empty")
            return False

    def push(self,node):
        #进栈时若栈内空间不够，则调用append函数
        #若空间足够，则将下一空间节点置为node
        if len(self.stack)<=self.length:
            self.stack.append(node)
            self.length+=1
            self.top+=1
        else:
            self.stack[self.top+1] = node
            self.length+=1
            self.top+=1

    def pop(self):
        #出栈时改变cbList中label值
        tempnode = self.stack[self.top]
        templabel = []
        #出栈时生成label，label等于栈内升序title组成的数组
        for i in range(self.top+1):
            temp = (self.stack[i].index,self.stack[i].title)
            templabel.append(temp)
        #todo,出栈的时候生成label
        tempnode.label = templabel
        self.stack[self.top] = None
        self.top-=1
        self.length-=1

        #tempIndex = tempnode.index
        print("------in pop()-----------")
        tempnode.show()

        return tempnode

    def check(self,listIsEmpty)->list:
        #进栈之后根据匹配规则生成出栈序列poplist，主要检测情况1,3
        #todo
        print("----------in check function------------")
        poplist = []
        #检测顺序应该是先检测往下一层，再检测网上一层，最后检测同层，即
        #若进站前检测，则无区别
        # 1.检测往下一层<=>self.layerDeltaCheck() == 1
        # 2.检测往上一层<=>self.layerDeltaCheck() < -1
        # 3.检测同层<=>self.layerDeltaCheck() == 0
        if not listIsEmpty:
            #进栈队列不为空，即进栈尚未完成
            if self.layerDeltaCheck() == 1:
                #1.进入下层嵌套中，pass,直接进栈，不pop，即poplist为空
                poplist = []
            elif self.layerDeltaCheck() <= -1:
                #2.检测往上一层或上n层，直接出栈元素至层数与top元素层数相等即可
                topItem = self.getTopItem()
                topLayer = topItem.layer
                index = self.top - 1
                start = -1
                while index > -1:
                    print("in check while 1 , index is %d"% index)
                    #time.sleep(1)
                    preNode = self.getItem(index)
                    if topLayer == preNode.layer :
                        start = index
                        break
                    else:
                        index -=1
                        continue
                if start > -1:
                    poplist.append(self.top - start)
                else:
                    print("ERROR: can not find equal layer ")

            elif self.layerDeltaCheck() == 0:
                #3.同层代码块，检测是否出栈
                topItem = self.getTopItem()

                if topItem.getKindCondition() == "else":
                    #else 的情况往前找到同层 if ，依序pop
                    topLayer = topItem.layer
                    index = self.top - 1
                    start = -1#start标记if位置
                    # else 的情况往前找到同层 if ，poplist放入要pop节点的数量，从后往前pop
                    while index>-1 :
                        print("in check while 2 , index is %d" % index)
                        #time.sleep(2)
                        preNode = self.getItem(index)
                        if topLayer == preNode.layer and preNode.getKindCondition() == "if":
                            start = index
                            break
                        else:
                            index -=1
                            continue

                    if start > -1:
                        #-----check得到poplist应该包含if处位置-------
                        poplist.append(self.top - start+1)
                    else:
                        print("ERROR: can not find 'if' ")
                else:
                    #除去else的情况，else if直接进栈即可
                    poplist = []
            else:
                print("ERROR11: 出现了layerDelta大于1的异常情况")


        else:#进栈完毕
            if self.top == 0:
                #只剩最后一个元素
                poplist.append(1)
            else:
                num = self.top+1
                poplist.append(num)
                print("进栈完毕后，栈内不止一个元素")

        return poplist

    def checkBefore(self,tempnode)->list:
        #执行进栈前检测，返回poplist
        #进栈前检测，主要检测情况2.检测往上一层<=>self.layerDeltaCheck() < -1
        #todo
        poplist = []

        print("---in checkBefore-----")
        print("layerDelta is {}".format(self.layerDeltaCheckTop(tempnode)))

        if self.layerDeltaCheckTop(tempnode) == 1 or self.layerDeltaCheckTop(tempnode) == 0:
            # 1.进入下层嵌套中，pass,直接进栈，不pop，即poplist为空;或者同层并列，进栈
            poplist = []
        elif self.layerDeltaCheckTop(tempnode) <= -1:
            # 2.检测往上一层或上n层，直接出栈元素至层数与tempnode层数相等即可
            tempLayer = tempnode.layer
            index = self.top - 1
            start = -1
            while index > -1:
                preNode = self.getItem(index)
                if tempLayer == preNode.layer:
                    start = index
                    break
                else:
                    index -=1
                    continue
            if start > -1:
                #此处检测到返回上层，值pop当前层的元素，不包含上层元素
                poplist.append(self.top - start)
            else:
                print("ERROR: can not find equal layer ")

        # elif self.layerDeltaCheckTop(tempnode) == 0:
        #     # 3.同层代码块，检测是否出栈
        #     topItem = self.getTopItem()
        #
        #     if topItem.getKindCondition() == "else":
        #         # else 的情况往前找到同层 if ，依序pop
        #         tempLayer = tempnode.layer
        #         index = self.top - 1
        #         start = -1
        #         # else 的情况往前找到同层 if ，poplist放入要pop节点的数量，从后往前pop
        #         while index > -1:
        #             preNode = self.getItem(index)
        #             if topLayer == preNode.layer and preNode.getKindCondition() == "if":
        #                 start = index
        #                 break
        #             else:
        #                 continue
        #         if start > -1:
        #             poplist.append(self.top - start)
        #         else:
        #             print("ERROR: can not find 'if' ")
        #     else:
        #         # 除去else的情况，else if直接进栈即可
        #         poplist = []
        else:
            print("ERROR21: 出现了layerDelta大于1的异常情况")

        return poplist


    def layerDeltaCheck(self):
        """check top node & pre node"""
        if self.top>0:
            #返回当前和上一层layer之间的差值
            return self.getTopItem().layer-self.getItem(self.top-1).layer
        else:
            print("ERROR: the stack is empty or just one item")
            return False

    def layerDeltaCheckTop(self,tempnode):
        """check top node & temp node"""
        if self.top>=0:
            #返回当前tempnode和topnode layer之间的差值
            return tempnode.layer-self.getTopItem().layer
        else:
            print("ERROR: the stack is empty")
            return False


    def popall(self,poplist):
        #根据poplist进行出栈
        #todo
        result = []
        if len(poplist) == 0:
            return result
        else:
            num = poplist[0]
            for i in range(num):
                print("------in popall---------")
                print("执行第{}遍".format(i))
                result.append(self.pop())

        return result




#--------------1读取数据转为字符串-----------------
def readFileToStr(filename)->str:
    try:
        f = open(filename, "r")
        print("__read file__")
        print("filename : \n\t{}".format(filename))
        try:
            count = 0

            while True:
                content = f.readlines()

                count = count + 1
                #print("------count is {}-------\n".format(count))
                #print(content)
                if len(content) == 0:
                    break
                else:
                    resultStr = ""
                    for i in range(len(content)):
                        resultStr+=content[i]
                    print("content of file is:\n\t{}".format(resultStr))
                time.sleep(0.5)
                #print("content of file is:\n\t{}".format(content))
        finally:
            f.close()
            print("__close file__")

    except Exception as result:
        print("产生错误了{}".format(result))

    return resultStr

#在字符串中返回子串所在位置的list
def find(string,subString)->list:
    """
    返回子串所在位置的list
    :param string:
    :param subString:
    :return:
    """
    #string.find()函数如果未找到则返回-1
    search = subString
    start = 0
    result = []
    while True:
        index = string.find(search, start)
        # if search string not found, find() returns -1
        # search is complete, break out of the while loop
        if index == -1:
            break
        #print("%s found at index %d" % (search, index))
        result.append(index)
        # move to next possible start position
        start = index + 1
    return result
#用于括号匹配的数据结构
class brace (object):
    def __init__(self, index,layer):
        """括号匹配，并且分出代码层数（只需要看左括号）/n
            左括号节点对应的next就是右括号节点在字符串中的下标
            :param data:
            :return:
        """
        self.index = index
        self.layer = layer
        self.next = None

    def set(self,next):
        self.next = next
        return

#--------------2从代码中提取codeBlock----------------
def codeBlockExtractor(content:str):
    print("-----------codeBlockExtractor---------------")
    cb = []
    #array数组用于记录所有brace，并判断其所处层数
    # array = [];atop = -1;
    #stack栈用于记录括号匹配信息，在左括号进栈之后,栈的深度stop的值等于左括号所处的层数layer
    stack = [];stop = -1;

    #利用brace括号匹配生成代码块，形成初步的node list
    #layer = 0,1,2,3....
    for i in range(len(content)):
        c = content[i]
        if stop<0 and c == "{":
            #初始化一定为左括号，进栈
            layer = stop+1;
            temp = brace(i,layer)
            # array.append(temp);
            # atop += 1;
            stack.append(temp);
            stop += 1;
            # print("--------1---------------")
            # print("i is {}\n".format(i))
            # print("stop is {}\n".format(stop))
            # print("len stack is {}\n".format(len(stack)))
            # print("stack is {}\n".format(stack[stop]))
        else:
            if c == "{":
                #若当前为左括号，进栈
                layer = stop + 1;
                temp = brace(i, layer)
                # array.append(temp);
                # atop += 1;

                if  len(stack)-1 > stop and stack[stop+1] == None :
                    stack[stop+1] = temp
                else :
                    stack.append(temp);
                stop += 1;
                # print("--------2---------------")
                # print("i is {}\n".format(i))
                # print("stop is {}\n".format(stop))
                # print("len stack is {}\n".format(len(stack)))
                # print("stack is {}\n".format(stack[stop]))

            elif c == "}":
                 # 若当前为右括号，出栈。并检测到一个code black,放入cb中
                 layer = stop - 1;
                 temp = brace(i, layer)
                 stack[stop].set(temp)
                 # print("--------3---------------")
                 # print("i is {}\n".format(i))
                 # print("stop is {}\n".format(stop))
                 # print("len stack is {}\n".format(len(stack)))
                 # print("stack is {}\n".format(stack[stop]))
                 cb.append(stack[stop])

                 # array.append(temp);
                 # atop += 1;
                 stack[stop]=None;
                 stop -= 1;

        #
        # if  c == "{" :
        #     if atop<0:
        #         #第一个左括号，层数初始为0
        #         layer = 0
        #         temp = brace(i, "{", layer)
        #
        #         array.append(temp);atop+=1;
        #         stack.append(temp);stop+=1;
        #
        #         # print(content[i])
        #         # print(i)
        #     else:
        #         #atop>=0若不是第一个左括号,根据array[atop]信息更新层数
        #         if array[atop] == "{":
        #             # 当前{的上个括号也是{，嵌套层数变深，则层数加一
        #             layer += 1;
        #             temp = brace(i, "{", layer)
        #
        #             array.append(temp);atop += 1;
        #             stack.append(temp);stop += 1;
        #         elif array[atop] == "}":
        #             # 当前{的上个括号是},说明是并列层，则层数不变
        #             temp = brace(i, "{", layer)
        #
        #             array.append(temp);
        #             atop += 1;
        #             stack.append(temp);
        #             stop += 1;
        # elif c == "}":
        #     #右括号上个是左括号，说明是同一层，层数不变。出栈一个左括号，发现一个codeblack
        #     if array[atop] == "{":
        #         temp = brace(i, "{", layer)
        #
        #         array.append(temp);
        #         atop += 1;
        #         stack[stop]=None;
        #         stop -= 1;
    nodeList = codeBlockList()
    for j in range(len(cb)):

        data = content[cb[j].index:cb[j].next.index + 1]

        # print("-----------%d---------------" % j)
        # print(cb[j].index)
        # print(cb[j].next.index)
        # print(cb[j].layer)
        # print(data)

        Range = (cb[j].index,cb[j].next.index)
        #temp = Node(len(cb)-j,Range,cb[j].layer,data)
        temp = Node(j, Range, cb[j].layer, data)

        nodeList.append(temp)
    #nodeList是所有代码块node的list

    #nodeList.reverse();#反序前按深度优先排列,反序后node的index顺序中第一个是程序入口处的代码块
    #nodeList中index按深度优先遍历
    # for j in range(len(nodeList)):
    #     print("-----------codeBlock%d---------------" % j)
    #     nodeList[j].show()
    #     print("---------------------------")

    # nodeList.show()
    print("-----------End of codeBlockExtractor---------------")
    return nodeList

#-------------3从代码和codeBlockList中提取出CFG---------
def cfgExtractor(content:str):
    print("-----------cfgExtractor---------------")
    cbList = codeBlockExtractor(content)#cbList存放了所有的codeBlock节点node
    # p_if = find(content,"if")
    # p_else = find(content,"else")
    # print(p_if)
    # print(p_else)
    cbList.sortByBraceOrder()#代码node按照在源程序中的顺序进行排序，并改变索引
    # cbList.sort(key=takeNodeBrace)
    # for j in range(len(cbList)):
    #     print("-----------codeBlock%d---------------" % j)
    #     cbList[j].show()
    #     print("---------------------------")

    cbList.calFindScope(content)#确定每个node的title，以便于生成label
    #-----------生成title后cb.show--------------
    print("-----------生成tiele后cb.show--------------")
    cbList.show()

    print("-----------clear tiele后cb.show--------------")
    cbList.clearTitleString()
    cbList.show()
    # labelList = LabelLinklist()#创建空表
    # print(cbList.nodelist[0].layer)

    # # 若存在0层node，添加为表头
    # if cbList.nodelist[0].layer == 0:
    #     # print("here")
    #     temp = LabelNode(cbList.nodelist[0].layer)
    #     labelList.append(temp)
    #
    #     labelList.show()
    # else:
    #     print("error in cfgExtractor")
    # index = 1
    # pre = labelList.head
    # # while pre and index< cbList.getLength():
    # #     templayer = pre.layer
    # #     #pre = pre.next
    # #
    # #     pass
    # for index in range(cbList.getLength()):

    ls = LabeStack(cbList)#用cnList初始化label栈
    #循环应该使用while栈非空，所以需要初始化栈push第一个元素

    # for i in range(cbList.getLength()):
    #     #理论上进栈完成则label生成完成
    #     #其具体步骤为
    #     #1.进栈push
    #     #2.check，确定出栈序列
    #     #3.popall，按照出栈序列进行出栈并生成label
    #     #4.重复123直到进栈完毕；且最后一次进栈push、check、popall之后栈stack应该为空，不为空报错
    #     #todo
    #     ls.push(cbList.nodelist[i])
    #     poplist = ls.check()
    #     ls.popall(poplist)
    #     pass
    i = 0#while 循环用指针
    if cbList.getLength()<=0:
        print("ERROR: nodeList长度小于等于0")
    else:
        #初始化label栈，push第一个元素
        ls.push(cbList.getNodeByIndex(i))
        i = i+1
        max = cbList.getLength()
    #--------------生成label的主循环-------------------------
        #进行label生成，进栈前检测是否出栈or进栈
        while not ls.isEmpty():
            print("\n-----------while 执行了第%d遍------------" % i)
            #time.sleep(1)
            if i < max:
                #进栈队列未进栈完成
                nodeListIsempty = False
                tempnode = cbList.getNodeByIndex(i)

                #print("tempnode is \n")
                #tempnode.show()

                #todo 进栈前检测并popall
                poplist = ls.checkBefore(tempnode)
                print("进栈前poplist is {}".format(poplist))
                ls.popall(poplist)

                ls.push(tempnode)

                # todo 进栈后检测并popall
                poplist = ls.check(nodeListIsempty)
                print("进栈后poplist is {}".format(poplist))
                ls.popall(poplist)


            else:
                #进栈队列进栈完成
                #一般来说，此处labelStack中只剩第一个元素,或是只剩if
                nodeListIsempty = True
                poplist = ls.check(nodeListIsempty)
                print("poplist is {}".format(poplist))

                ls.popall(poplist)


            i+=1
            if i > 10:
                break


        # -----------生成label后cb.show--------------
        print("-----------生成label后cb.show--------------")
        cbList.show()

        print("-----------label transform后cb.show--------------")
        cbList.labelTransform()
        cbList.show()

        print("\n-----------cb.showPartly--------------")
        cbList.showPartly()






    print("-----------End of cfgExtractor-------------")

    return

def main():
    filename:str = r"dataset/if_else/4.txt";
    #print(filename)
    content = readFileToStr(filename)

    cfgExtractor(content)
    #codeBlockExtractor(content)
    # print(find(content,"{"))
    # print(find(content,"}"))
    return


if __name__ == "__main__":
    print(__name__)

    main()

