from collections import defaultdict, deque

# 특정 기사의 명령에 따른 이동할 영역에 벽이나 다른 기사의 영역이 있는지
d_r = [-1, 0, 1, 0]
d_c = [0, 1, 0, -1]


def checkIfMove(knight, cmd):
    # 벽을 만나게 되면 빈 리스트를 반환하고
    # 한번도 벽을 만나지 않으면 겹치는 기사의 번호 리스트를 반환

    # 시작 좌표
    start_r = knight_info[knight][0] + d_r[cmd]
    start_c = knight_info[knight][1] + d_c[cmd]

    # 특정 기사의 영역을 돌면서 해당 좌표가 특정 기사의 영역과 겹치면 리스트에 넣어줌
    # 벽과 만나면 그 즉시 break
    flag = 0
    knight_list = []
    visited = set()
    for r in range(start_r, start_r + knight_info[knight][2]):
        for c in range(start_c, start_c + knight_info[knight][3]):
            # 벽인지 확인
            if r in range(L) and c in range(L) and trap[r][c]!=2:
                for k in knight_info.keys():
                    if knight != k and k not in visited and knight_info[k][4] > knight_info[k][5]:
                        # 검사할 기사의 영역과 겹치는지 확인
                        if r in range(knight_info[k][0] + knight_info[k][2]) and c in range(
                                knight_info[k][1] + knight_info[k][3]):
                            knight_list.append(k)
                            visited.add(k)
            else:
                # 벽을 만났으니 탈출!
                flag = 1
                break
        if flag == 1:
            return [-1]
    return knight_list



L, N, Q = map(int, input().split())
# 함정정보 입력
trap = []
for _ in range(L):
    trap.append(list(map(int,input().split())))

# 기사정보를 딕셔너리에 넣고 체력이 0보다 작거나 같게되면 해당 기사 del
knight_info = defaultdict(list)
for i in range(1, N + 1):
    info = list(map(int, input().split()))
    info[0] = info[0] - 1
    info[1] = info[1] - 1
    knight_info[i] = info + [0]

# 명령
for cmd in range(1, Q + 1):
    knight, direction = map(int, input().split())
    if knight_info[knight][4]<=knight_info[knight][5]:
        continue
    move_knight = []
    visited = set()
    q = deque([knight])
    flag = 0
    while q:
        cur_k = q.popleft()
        knight_list = checkIfMove(cur_k, direction)
        #겹치는게 없다?
        if len(knight_list)>0 and knight_list[0] == -1:
            flag = 1
            break
        # 겹치는 기사들리스트
        else:
            if cur_k not in visited:
                move_knight.append(cur_k)
                visited.add(cur_k)
            for k in knight_list:
                if k not in visited:
                    q.append(k)
    if flag == 1:
        continue
    # 기사들 리스트 이동시키자
    for k in move_knight:
        knight_info[k][0] += d_r[direction]
        knight_info[k][1] += d_c[direction]
        # 대미지 계산합시다
        if knight != k:
            damage = 0
            for r in range(knight_info[k][0], knight_info[k][0] + knight_info[k][2]):
                for c in range(knight_info[k][1], knight_info[k][1] + knight_info[k][3]):
                    if trap[r][c] == 1:
                        damage += 1
            knight_info[k][5] += damage
ans = 0
for k in knight_info.keys():
    if knight_info[k][4] > knight_info[k][5]:
        ans += knight_info[k][5]
print(ans)