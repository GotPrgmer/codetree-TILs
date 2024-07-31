import sys
from collections import defaultdict, deque


def input():
    return sys.stdin.readline().rstrip()


def node_add(m, p, c, md):
    # -1이면 바로 삽입
    if p == -1:
        # 처음은 자식수
        tree_rel[m] = [-1]
        # 마지막은 깊이
        tree_info[m] = [p, c, md, 1]
        # print(tree_rel[m])
    else:
        # 깊이수가 +1한 값보다 작아야함
        # 해당 노드부터 최상위 노드까지 올라가야함
        # 못올라가면 추가할 수 없는 애
        # print(m, "을 넣기 위함")
        q = []
        if ascend(m,p,q):
            # print("나이스", m)
            tree_info[m] = [p, c, md, 1]
            tree_rel[m] = [-1]
            tree_rel[p].append(m)
            # print(tree_rel[m],"sdafas")


def ascend(m,x, q):
    # print("올라감",m, x)
    if x == -1:
        for node in q:
            if len(tree_rel[node]) == 1:
                tree_info[node][3] += 1
            # print(tree_info[node])
        # print(m)
        return True
    if tree_info[x][2] >= tree_info[x][3] + 1:
        q.append(x)
        return ascend(m,tree_info[x][0], q)
    return False




def color_change(m,c):
    color_dfs(c,m)

def color_dfs(c,cur):
    tree_info[cur][1] = c
    for i in tree_rel[cur]:
        if i != -1:
            color_dfs(c,i)


def color_view(m):
    return tree_info[m][1]


def score_view():
    value = 0
    for i in tree_info.keys():
        if i != -1:
            value += bfs(i)
    return value


def bfs(x):
    q = deque([x])
    selected_color = [False] * 5
    while q:
        cur = q.popleft()
        color = tree_info[cur][1]
        selected_color[color - 1] = True
        for child in tree_rel[cur]:
            if child != 0 and child != -1:
                q.append(child)
    v = sum(selected_color)
    return v**2


Q = int(input())
tree_rel = defaultdict(list)
tree_info = defaultdict(list)
for _ in range(Q):
    cmd_line = list(map(int, input().split()))
    cmd_kind = cmd_line[0]

    if cmd_kind == 100:
        if cmd_line[2] == -1:
            start = cmd_line[1]
        node_add(cmd_line[1], cmd_line[2], cmd_line[3], cmd_line[4])
    elif cmd_kind == 200:
        color_change(cmd_line[1], cmd_line[2])
    elif cmd_kind == 300:
        print(color_view(cmd_line[1]))
    else:
        print(score_view())