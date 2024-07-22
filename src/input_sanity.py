# 给定一个字符串
# 判断它是否是一个合法的扭结 PD_CODE
# 理论上需要进行平面图判断，但是考虑到节约时间，这里省略了这一步
# 如果输入合法，则返回 pd_code
# 如何输入不合法，则直接报错并退出

def input_sanity(input_string: str) -> list:
    pd_code = eval(input_string)
    assert isinstance(pd_code, list) # PD_CODE 必须是一个 list
    for item in pd_code:
        assert isinstance(item, list) # PD_CODE 中的每个元素必须是一个 list
    for item in pd_code:
        assert len(item) == 4 # PD_CODE 中的每个 crossing 中必须有四个元素
    for item in pd_code:
        for x in item:
            assert isinstance(x, int) # PD_CODE 的每个 crossing 中的四个元素必须都是整数
    cnt = {}
    for item in pd_code: # 统计每个弧编号出现的次数，存入 cnt 中
        for x in item:
            if cnt.get(x) is None:
                cnt[x] = 0
            cnt[x] += 1
    for x in cnt:
        assert cnt[x] == 2 # PD_CODE 中每条弧线，必须恰好出现两次
    return pd_code

if __name__ == "__main__": # 测试程序
    print(input_sanity("[[1,2,2,1]]"))