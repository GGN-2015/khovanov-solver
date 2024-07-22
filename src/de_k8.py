"""_summary_
    删除扭结中具有 “8” 字结构的额外交点
    要求输入的扭结中不能具有 R1 拧
"""



def edge_index(a: int, b: int) -> int:
    if abs(a-b) == 1:
        return min(a, b) # 比如 (2, 3) => 2，意思是这条边是从 2 出发的
    else:
        return max(a, b) # 比如 (1, 10) => 10，意思是这条边是从 10 出发的



def get_cross(pd_code: list) -> dict:
    cross = {}
    for x in pd_code:
        a, b, c, d = x # (a, c) 与 (b, d) 相交
        e1 = edge_index(a, c)
        e2 = edge_index(b, d)
        cross[e1] = e2
        cross[e2] = e1 # 记录每条边和谁相交
    return cross



def sort_by_direction(a: int, c: int) -> tuple:
    xfrom = edge_index(a, c)
    xto   = a + c - xfrom
    return (xfrom, xto) # 按照经过的先后次序排序



def get_next_pos(pos: int, nmax: int) -> int: # 后继编号
    pos += 1
    if pos > nmax: pos = 1
    return pos



def get_node_list(nfrom, nto, nmax):
    arr = []
    pos = nfrom
    while pos != nto:
        arr.append(pos)
        pos = get_next_pos(pos, nmax)
    return arr



def check_8_core(pd_code: list, cross: dict, index: int, n: int) -> bool:
    assert index in range(0, len(pd_code))
    a, b, c, d = pd_code[index] # 得到这个交叉点的 pd_code
    a, c = sort_by_direction(a, c)
    b, d = sort_by_direction(b, d)

    clist = get_node_list(c, b, n)
    dlist = get_node_list(d, a, n)
    assert clist != [] and dlist != [] # 我们要求没有 R1 拧

    for x in clist:
        if cross[x] in dlist: # 说明两侧的纽结仍有其他交点
            return False
    return True



def get_8_core_index(pd_code: list) -> int: # 寻找八字核心，找不到返回 -1
    cross = get_cross(pd_code)
    n     = max([max(x) for x in pd_code]) # 最大结点编号
    for i in range(len(pd_code)):
        if check_8_core(pd_code, cross, i, n): # 检查一个位置是否是 8 字核心
            return i
    return -1



def addarc(nxt: dict, a: int, b: int): # 增加单向边
    if nxt.get(a) is None:
        nxt[a] = []
    nxt[a].append(b)



def addedge(nxt: dict, a: int, b: int): # 增加双向边
    addarc(nxt, a, b)
    addarc(nxt, b, a)



def get_nxt_dict(pd_code) -> list: # 得到邻接矩阵
    nxt = {}
    for a, b, c, d in pd_code:
        addedge(nxt, a, c)
        addedge(nxt, b, d)
    return nxt



def dfs(pos: int, nxt: dict, vis: list):
    assert pos not in vis
    vis.append(pos)

    assert len(nxt[pos]) == 2 # 恰有两个出边
    for npos in nxt[pos]:
        if npos not in vis:
            dfs(npos, nxt, vis) # 继续 dfs
            return



def sanity_number(pd_code: list, dlis_f, dlis_t):
    nxt = get_nxt_dict(pd_code) # 计算邻接矩阵
    vis = [dlis_f]
    
    dfs(dlis_t, nxt, vis)          # 得到 vis 是 dfs 序
    assert len(vis) == len(nxt) # 保证一定要遍历到所有节点（不适用于链环）

    nnum = {}
    for i in range(len(vis)):
        nnum[vis[i]] = i + 1 # 从 1 开始重新编号

    return [
        [nnum[a] for a in x] # 使用新的编号进行编码
        for x in pd_code
    ]



def del_8_core_by_index(pd_code: list, cross_index: int) -> list:
    assert cross_index in range(0, len(pd_code))
    n = max([max(x) for x in pd_code]) # 最大结点编号

    a, b, c, d = pd_code[cross_index] # 得到这个交叉点的 pd_code
    
    a, c = sort_by_direction(a, c)
    b, d = sort_by_direction(b, d)
    
    dlist = get_node_list(d, a, n)
    cset   = set(get_node_list(c, b, n) + [b]) # 所有恰好在 clist 侧的交点取镜像
    new_pd = []
    for i in range(len(pd_code)):
        ax, bx, cx, dx = pd_code[i]

        if i == cross_index: # 删除掉旧的交点
            continue

        if set([ax, bx, cx, dx]).issubset(cset): # 完全在里面 取镜像
            turn = [ax, dx, cx, bx] # 严格来说不是镜像，而是空间翻转
            xf, _ = sort_by_direction(bx, dx)
            while turn[0] != xf:
                turn = turn[1:] + [turn[0]] # 转一转，把 xf 转到入口
            new_pd.append(turn)
        else:
            new_pd.append(pd_code[i])

    new_pd = [
        [x if x != b else d for x in line] 
        for line in new_pd] # a 映射成 b
    new_pd = [
        [x if x != c else a for x in line] 
        for line in new_pd] # c 映射成 d
    new_pd = sanity_number(new_pd, dlis_f=dlist[0], dlis_t=dlist[1])                # 重新计算合法编号
    return new_pd



def de_k8(pd_code: list) -> list: # 删除所有的 8 字核心
    while len(pd_code) > 0 and (cross_index := get_8_core_index(pd_code)) >= 0:
        pd_code = del_8_core_by_index(pd_code, cross_index)
    return pd_code



if __name__ == "__main__":
    pd_code = eval(input("pd_code>>>"))
    print(de_k8(pd_code))