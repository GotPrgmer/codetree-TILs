# 맨처음에는 유물 존재하는지 파악하지 않아도 된다.
# (1,1)에서 (3,3)까지 90도, 180도, 270도 돌리면서 각도 회전하면서 사라지는 조각들의 최대치를 pq에다가
# -조각 수, 열, 행, 회전 을 넣는다.
# 이때 bfs를 돌려서 사라지는 조각을 알게된다.

# 만약 여기서 단 한개의 조각도 사라지지 않는다면 턴을 종료한다.
# 이 경우 출력되는 유물의 값은 없다.

# 만약 턴이 계속해서 진행이 된다면
# -조각 수, 열, 행 회전이 맨 앞에 있는 것을 해당되는 회전으로 돌린다.

# 아래와 같은 행위를 사라지는 3조각 이상이 나오지 않을 때까지 계속 반복한다.
# 그리고 사라지는 조각들을 계속 누적시킨다.
# bfs를 돌려서 3조각 이상인 것들을 지운다.
# spare_yumul에서 하나씩 빼서 유물의 빈공간을 채운다.
# spare_yumul가 부족한 경우는 없다.

# 위와 같은 행위를 K번 반복한다.

# -------------------구현
import heapq
from collections import deque
import copy

K, M = map(int, input().split())
map_info = []
for _ in range(5):
    map_info.append(list(input().split()))
spare_yumul = deque(list(input().split()))


# 맨처음에는 유물 존재하는지 파악하지 않아도 된다.

# 맵 전체 돌려서 사라지는 조각 수 계산
def bfs(map_info):
    visited = [[0] * 5 for _ in range(5)]
    total = 0
    for r in range(5):
        for c in range(5):
            if visited[r][c] == 0:
                # bfs돌리기
                q = deque([(r, c)])
                cnt = 0
                while q:
                    cur_r, cur_c = q.popleft()
                    if visited[cur_r][cur_c] == 1:
                        continue
                    visited[cur_r][cur_c] = 1
                    cnt += 1
                    # 사방탐색
                    for d in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
                        n_r = cur_r + d[0]
                        n_c = cur_c + d[1]
                        if n_r in range(5) and n_c in range(5) and map_info[n_r][n_c] == map_info[cur_r][cur_c]:
                            q.append((n_r, n_c))
                if cnt >= 3:
                    total += cnt
    return total


def bfsAndDisappear(map_info):
    result = []
    visited = [[0] * 5 for _ in range(5)]
    for r in range(5):
        for c in range(5):
            if visited[r][c] == 0:
                # bfs돌리기
                tmp = []
                q = deque([(r, c)])
                while q:
                    cur_r, cur_c = q.popleft()
                    if visited[cur_r][cur_c] == 1:
                        continue
                    visited[cur_r][cur_c] = 1
                    tmp.append((cur_c, -cur_r))

                    # 사방탐색
                    for d in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
                        n_r = cur_r + d[0]
                        n_c = cur_c + d[1]
                        if n_r in range(5) and n_c in range(5) and map_info[n_r][n_c] == map_info[cur_r][cur_c]:
                            q.append((n_r, n_c))
                if len(tmp) >= 3:
                    result.extend(tmp)
    return result


# (1,1)에서 (3,3)까지 90도, 180도, 270도 돌리면서 각도 회전하면서 사라지는 조각들의 최대치를 pq에다가
for turn in range(K):
    pq = []
    this_cnt = 0
    for r in range(1, 4):
        for c in range(1, 4):
            copy_map = copy.deepcopy(map_info)
            lst = [copy_map[r - 1 + i][c - 1:c + 2] for i in range(3)]
            cnt = 0
            select_rotate = 0
            rotate = 0
            for d in range(3):
                # 90도 돌리고 넣기
                lst = list(map(list, zip(*lst[::-1])))
                rotate += 1
                for cur_r in range(3):
                    for cur_c in range(3):
                        copy_map[r - 1 + cur_r][c - 1 + cur_c] = lst[cur_r][cur_c]
                bfs_cnt = bfs(copy_map)
                if cnt < bfs_cnt:
                    cnt = bfs_cnt
                    select_rotate = rotate
                    heapq.heappush(pq, (-cnt,rotate, c, r ))
    # pq에서 하나를 뽑아서 rotate를 다시 돌리자
    if len(pq)==0:
        break
    cur_cnt, rotate,c, r = heapq.heappop(pq)

    # 이번에 사라지는 조각이 0개이면 break
    if cur_cnt == 0:
        break
    lst = [map_info[r - 1 + i][c - 1:c + 2] for i in range(3)]
    cur_cnt = -cur_cnt
    for d in range(rotate):
        # rotate만큼 돌리기
        lst = list(map(list, zip(*lst[::-1])))
    for i in range(3):
        for j in range(3):
            map_info[r - 1 + i][c - 1 + j] = lst[i][j]
    # bfs돌려서 사라지는 조각수 계산
    while True:
        delete_lst = bfsAndDisappear(map_info)
        delete_lst.sort()
        if len(delete_lst) != 0:
            for p in delete_lst:
                # (c,r)임!
                map_info[-p[1]][p[0]] = spare_yumul.popleft()
                this_cnt += 1
        else:
            break
    print(this_cnt,end=" ")

# -조각 수, 열, 행, 회전 을 넣는다.
# 이때 bfs를 돌려서 사라지는 조각을 알게된다.


# 만약 여기서 단 한개의 조각도 사라지지 않는다면 턴을 종료한다.
# 이 경우 출력되는 유물의 값은 없다.

# 만약 턴이 계속해서 진행이 된다면
# -조각 수, 열, 행 회전이 맨 앞에 있는 것을 해당되는 회전으로 돌린다.

# 아래와 같은 행위를 사라지는 3조각 이상이 나오지 않을 때까지 계속 반복한다.
# 그리고 사라지는 조각들을 계속 누적시킨다.
# bfs를 돌려서 3조각 이상인 것들을 지운다.
# spare_yumul에서 하나씩 빼서 유물의 빈공간을 채운다.
# spare_yumul가 부족한 경우는 없다.

# 위와 같은 행위를 K번 반복한다.