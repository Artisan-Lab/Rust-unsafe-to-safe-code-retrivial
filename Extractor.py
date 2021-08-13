import time


#代码块node
class Node (object):
    def __init__(self, index,Range,layer,data):
        """链表中节点结构，只有data和next，多跳转情况下需调整
            :param data:
            :return:
        """
        self.index = index#每个node的唯一编号。编号顺序按深度优先
        self.Range = Range#该代码块在原字符串中坐标范围
        self.data = data
        self.label = []#用于存储该代码块的控制语句，由于嵌套可能存在，故将label定义为数组.其值为[(condition，index),...]
        self.layer =layer#相对于程序入口，该代码块的嵌套层数
        self.next = None

    def show(self):
        print("index of the code blocks is \n\t{}".format(self.index))
        print("Range of source code is \n\t{}".format(self.Range))
        print("data of the code block is \n\t{}".format(self.data))
        print("label of the code blocks is \n\t{}".format(self.label))
        print("layer of the code blocks is \n\t{}".format(self.layer))

#用于生成node的label的数据结构
class LabelNode(object):
    def __init__(self,layer):
        self.value = []#用于存储该代码块的控制语句，由于嵌套可能存在，故将value定义为数组.其值为[(condition，index),...]
        #由于是深度优先，所以当有深层嵌套时，next必有值
        self.next = None
        self.layer = layer#label是第几层嵌套的label

#动态单链表，用于labelnode生成为每个代码块node生成label
class Linklist(object):

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

#读取数据转为字符串
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

#用于管理一份代码的所有codeBlock（即node）
class codeBlockList(object):
    def __init__(self):
        self.nodelist = []
        self.length = 0
    def append(self,node):
        self.nodelist.append(node)
    def getLength(self):
        self.length = len(self.nodelist)
        return self.length
    def show(self):
        for j in range(len(self.nodelist)):
            print("-----------codeBlock%d---------------" % j)
            self.nodelist[j].show()
            print("---------------------------")
    #各代码块顺序按在文件中的顺序排列
    def sortByBraceOrder(self):
        self.nodelist.sort(key=self.takeNodeBrace)
    def takeNodeBrace(self,elem):
        return elem.Range[0]

#从代码中提取codeBlock
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

    nodeList.show()
    print("-----------End of codeBlockExtractor---------------")
    return nodeList

#从代码和codeBlockList中提取出CFG
def cfgExtractor(content:str):
    print("-----------cfgExtractor---------------")
    cbList = codeBlockExtractor(content)
    # p_if = find(content,"if")
    # p_else = find(content,"else")
    # print(p_if)
    # print(p_else)
    cbList.sortByBraceOrder()
    # cbList.sort(key=takeNodeBrace)
    # for j in range(len(cbList)):
    #     print("-----------codeBlock%d---------------" % j)
    #     cbList[j].show()
    #     print("---------------------------")
    cbList.show()
    return

def main():
    filename:str = r"dataset/if_else/1.txt";
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

