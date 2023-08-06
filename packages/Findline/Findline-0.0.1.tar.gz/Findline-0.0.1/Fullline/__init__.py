def findLines(filename,keyword):
    with open(filename,"r")as f:
        content=f.readlines()
        a=-1
        b=[]
        for l in content:
            a=a+1
            if keyword in l:
                b.append(a)
    for item in b:
        g=(content[item])
        print(g)
        #if you are working with tkinter then use the following command rather than print
        #it will put your text line in a letter box I have 
        # my_list.insert(END,g)
