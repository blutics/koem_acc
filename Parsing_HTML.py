from bs4 import BeautifulSoup
import re

class LoadParsing():
    def __init__(self,file):
        with open(file,'r',encoding='utf-8') as fp:
            self.origin = BeautifulSoup(fp,'html.parser')
        self.soup = self.origin.find_all(class_='t')
    def getPairs(self):
        files = [i.get_text()for i in self.soup if 'xxx' in i.get_text()]
        stitches = [i.get_text()[9:]for i in self.soup if 'stitches' in i.get_text()]
        return [i for i in zip(files,stitches)]
    def extractHTML(self,x):
        output=open('output.html','w',encoding='utf-8')
        index=0
        print("hello world!")
        for i in self.soup:
            if 'Dim' in i.get_text():
                t=i.get_text()
                #i.string.replace_with(t+"\n"+x[index].text())
                #"span", style="font-weight: bold; font-size: 40pt"
                new = self.origin.new_tag("h1")
                price=x[index].text()
                print(price)
                z=[*reversed(price)]
                count=1
                result=[]
                for k in z:
                    result+=k,
                    if count%3==0:
                        if len(x)!=count:
                            result+=","
                    count+=1
                price=""
                for k in [*reversed(result)]:
                    price=price+k
                new.append("￦"+price)
                print(new)
                if i.span != None:
                    i.span.decompose()
                print(i)
                # i.string.insert_after(new)
                i.append(new)
                index+=1
        output.write(str(self.origin))
        output.close()
"""
a=LoadParsing('2018-05.html')

b=a.getPairs()
for i in b:
    print(i)

g = open('new.html','w')
for i in a.origin.prettify():
    g.write("%s"%str(i))
g.close()
"""
