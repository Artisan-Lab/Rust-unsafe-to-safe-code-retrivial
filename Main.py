import DataStructure,CFGextractor


def main():
    for i in range(1,6):
        filename:str = r"dataset/if_else/"+str(i)+".txt";
        print("============"+filename+"============")
        content = DataStructure.readFileToStr(filename)

        CFGextractor.cfgExtractor(content)
        #codeBlockExtractor(content)
        # print(find(content,"{"))
        # print(find(content,"}"))
    return


if __name__ == "__main__":
    print(__name__)

    main()