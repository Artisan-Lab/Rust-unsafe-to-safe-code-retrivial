import DataStructure
from DataStructure import brace,codeBlockList,Node,LabeStack

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
            temp = DataStructure.brace(i, layer)
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

