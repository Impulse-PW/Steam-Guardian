#Application color class
class colors(object):
    #Initialize
    def __init__(self):
        #Create our colors dictionary
        self.colorDic = {}
        with open("colors.txt","r") as f:
            colorsList = f.read()
        #Split dictionary by every new line
        colorsList = colorsList.split("\n")
        #Append colors and names to colors dictionary
        for color in colorsList:
            colorSplit = color.split(" ")
            self.colorDic[colorSplit[0].split("=")[0]] = colorSplit[-1].split("=")[-1]
