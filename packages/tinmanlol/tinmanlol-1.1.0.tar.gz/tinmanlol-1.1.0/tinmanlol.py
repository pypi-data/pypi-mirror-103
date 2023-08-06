'''
这个“tinmanlol”模块，提供了一个名为print_lol()的函数，其作用是打印列表，顺利显示出其中可能包含（也可能不包含）的嵌套列表。
'''
'''
取一个位置参数，名为“the_list”，这可以是任何Python列表，也可以是包含嵌套列表的列表。所指定列表中的每个数据项会（递归地）输出到屏幕上，各数据项各占一行。
'''
def print_lol(the_list, level):  
    for x in the_list:
        if isinstance(x, list):
            print_lol(x, level+1)
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(x)