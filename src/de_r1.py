"""
    de_r1.py 的主要功能是从 pd_code 中去除所有 R-1 拧并生成新的 pd_code
    由于 JavaKh-v2 遇到 R-1 拧就会报错，所以我们要在计算 khovanov 同调前去掉所有 R-1 拧
"""



# 向邻接表添加单向边
def __add_arc(nxt: dict, a: int, b: int) -> None:
    if nxt.get(a) is None:
        nxt[a] = []
    if b not in nxt[a]:
        nxt[a].append(b)



# 向邻接表添加双向边
def __addedge(nxt: dict, a: int, b: int) -> None:
    __add_arc(nxt, a, b)
    __add_arc(nxt, b, a)



# 构造邻接表
def __get_nxt(pd_code: list) -> dict:
    nxt = {}
    for line in pd_code:
        a, b, c, d = line # a -> c, b -> d
        __addedge(nxt, a, c)
        __addedge(nxt, b, d)
    return nxt



# 深度优先搜索找环
def __dfs(nxt: dict, vis: list, pos: int) -> None:
    assert pos not in vis
    vis.append(pos)

    for v in nxt[pos]:
        if v not in vis:
            __dfs(nxt, vis, v)
            break



def __get_value_set(pd_code: list) -> list:
    value_set = []
    for x in pd_code:
        for v in x:
            if v not in value_set:
                value_set.append(v)
    return value_set



# 删除 pd_code 中的所有 r1 拧
def de_r1(pd_code: list) -> list:
    while any(len(set(x)) <= 3 for x in pd_code):
        for i in range(len(pd_code)):
            x = pd_code[i]
            if len(set(x)) <= 3:
                pd_code = pd_code[:i] + pd_code[i+1:] # 删除当前节点
                single  = []
                for v in x:
                    if x.count(v) == 1:
                        single.append(v)
                
                if len(single) == 2:
                    pd_code = [[(single[1] if x==single[0] else x) for x in line] for line in pd_code]
                    break
    
    # 获取编码集合
    value_set = __get_value_set(pd_code)

    # 重新编码
    if pd_code != []:
        nxt = __get_nxt(pd_code)
        vis = [] # 得到 dfs 序

        __dfs(nxt, vis, pd_code[0][0])
        assert set(vis) == set(value_set) # 保证每个元素都出现过

        # 给所有数据重新编码
        new_id = {}
        for i in range(len(vis)):
            new_id[vis[i]] = i + 1
        pd_code = [[new_id[v] for v in x] for x in pd_code]

    return pd_code



if __name__ == "__main__":
    pd_code = input("pd_code>>>").strip()
    print(de_r1(pd_code))