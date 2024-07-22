# 从标准输入读取一个 list 作为 PD_CODE
# 将对应扭结的信息输出到标准输出流中
# 将错误信息输出到标准错误流中

import sys

from kho_solver   import kho_solver
from input_sanity import input_sanity
from de_k8        import de_k8
from de_r1        import de_r1

def main() -> None:
    all_input = sys.stdin.read().strip() # 获取全部输入信息
    pd_code1  = input_sanity(all_input)  # 检查输入是否是合法的 pd_code
    pd_code2  = de_r1(pd_code1)
    pd_code3  = de_k8(pd_code2)
    if pd_code3 == []: # 处理平凡扭结的特殊情况，以免 JavaKh 出现异常
        print("q^-1*t^0*Z[0] + q^1*t^0*Z[0]")
        return
    khovanovH = kho_solver(pd_code3) # 调用 JavaKh
    print(khovanovH)

if __name__ == "__main__":
    main()