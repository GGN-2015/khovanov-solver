# 给定一个没有 r1-move 和 nugatory crossing 的扭结
# 利用 javaKh 计算它的 khovanov 同调

def __pd_code_wrapper(pd_code: list) -> str:   # 获取 JavaKh 输入风格的名字
    xlist = ["X" + str(x) for x in pd_code] # 交叉点序列
    return "PD[" + (", ".join(xlist)) + "]"

def kho_solver(pd_code: list) -> str:
    warpped_pd_code = __pd_code_wrapper(pd_code)
    return warpped_pd_code