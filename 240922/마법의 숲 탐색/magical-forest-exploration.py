from collections import deque
d_r = [-1,0,1,0]
d_c = [0,1,0,-1]
#해당 방향으로 갈 수 있니(서쪽이나 동쪽이면 남쪽으로 한 내려와야 함)
def valid(n,m,r,c):
    #열만 우선 검사하고
    if c in range(m) and r<n:
        #행도 범위내면 골렘값 확인
        if r in range(n):
            #0이어야 통과
            if map_info[r][c] == 0:
                return True
            else:
                return False
        #행이 범위밖이면 그냥 통과
        else:
            return True
    else:
        return False

def checkDir(n,m,r,c,d):
    #남쪽
    if d == 0:
        if valid(n,m,r+2,c) and valid(n,m,r+1,c-1) and valid(n,m,r+1,c+1):
            return True
    #서쪽
    elif d == 1:
        if valid(n,m,r,c-2) and valid(n,m,r-1,c-1) and valid(n,m,r+1,c-1) and checkDir(n,m,r,c-1,0):
            return True
    elif d == 2:
        if valid(n,m,r-1,c+1) and valid(n,m,r,c+2) and valid(n,m,r+1,c+1) and checkDir(n,m,r,c+1,0):
            return True
    return False
def mapRangeCheck(n,r):
    if r-1 in range(n):
        return True
    else:
        return False



R, C, K = map(int,input().split())
map_info = [[0]*C for _ in range(R)]
ans =0
cnt = 1
for _ in range(K):
    #입력받아서
    c, d = map(int,input().split())
    #남쪽으로 계속가다가 막히면
    c -= 1
    r = -2
    #아래로 내려감
    while True:
        #남쪽으로 가는 시도
        if checkDir(R,C,r,c,0):
            r+= 1
        #서쪽으로 가는 시도
        elif checkDir(R,C,r,c,1):
            c -= 1
            r+=1
            d = (4+d-1)%4
        #동쪽으로 가는 시도
        elif checkDir(R,C,r,c,2):
            c+= 1
            r += 1
            d = (4+d+1)%4
        else:
            break
    #숲밖으로 나갔는지 확인!
    if r-1 in range(R):
        #맵에 해당 골렘 기록
        for point in [[r-1,c],[r,c],[r,c+1],[r+1,c],[r,c-1]]:
            map_info[point[0]][point[1]] = cnt
        map_info[r+d_r[d]][c+d_c[d]] = -cnt
        cnt += 1

        #bfs 돌리기
        q = deque([(r,c),(r+1,c),(r-1,c),(r,c+1),(r,c-1)])
        visited = [[0]*C for _ in range(R)]
        max_r = -1
        while q:
            cur_r, cur_c = q.popleft()
            if visited[cur_r][cur_c] == 1:
                continue
            visited[cur_r][cur_c] = 1
            max_r= max(max_r,cur_r)
            #네 방향탐색해서 골렘있는 방향으로 q넣기
            for d in range(4):
                n_r = cur_r+d_r[d]
                n_c = cur_c+d_c[d]
                if n_r in range(R) and n_c in range(C):
                    if map_info[cur_r][cur_c]<0:
                        if map_info[n_r][n_c] != 0:
                            q.append((n_r,n_c))
                    elif map_info[n_r][n_c] == map_info[cur_r][cur_c] or abs(map_info[n_r][n_c])==map_info[cur_r][cur_c]:
                        q.append((n_r,n_c))



        #최대 행 누적합하기
        ans += max_r+1

    else:
        #지금까지 쌓인 골렘 초기화
        map_info = [[0]*C for _ in range(R)]
        cnt = 1
print(ans)