N, M, P, C, D = map(int, input().split())

# 1부터 P번까지 순서대로 산타가 돌기때문에 각 번마다의 산타 좌표를 저장할 리스트 필요
santa_info = [[N, N] for _ in range(P + 1)]
# 기절해 있거나 격자 밖으로 빠져나가서 탈락한 산타들은 움직일 수 없으니
# alive와 살아있더라도 언제 산타가 깨어날지를 나타내는 자료구조 필요
alive = [1] * (P + 1)
alive[0] = 0
santa_turn = [1] * (P + 1)
score = [0] * (P + 1)

# 루돌프와 가장 가까이에 있는 산타를 하나의 큐에 넣어서 sort시켜서 거리(오름), 행(내림),열(내림)
# 디버깅에 필요한 visited도 2차원으로 표현(루돌프는 -1, 산타는 번호를 넣어줌)
visited = [[0] * (N) for _ in range(N)]

Rr, Rc = map(lambda x: int(x) - 1, input().split())
visited[Rr][Rc] = -1

for _ in range(P):
    santaNum, Sr, Sc = map(int, input().split())
    santa_info[santaNum] = [Sr - 1, Sc - 1]
    visited[Sr - 1][Sc - 1] = santaNum


def move_santa(cur, sr, sc, dr, dc, move):
    # cur 번 산타를 sr, sc에서 dr,dc방향으로 move 칸 이동
    q = [(cur, sr, sc, move)]
    while q:
        cur, cr, cc, move = q.pop(0)
        # 진행방향으로 move칸 만큼 이동시키고 범위내이고 산타있으면 q삽입, 범위 밖 처리 확인
        nr, nc = cr + dr * move, cc + dc * move
        # 범위 내
        if nr in range(N) and nc in range(N):
            # 산타 있는지 확인
            # 산타없으면
            if visited[nr][nc] == 0:
                visited[nr][nc] = cur
                santa_info[cur] = [nr, nc]
                return
            else:
                # 산타가 있는 경우
                q.append((visited[nr][nc], nr, nc, 1))
                visited[nr][nc] = cur
                santa_info[cur]=[nr, nc]

        # 범위밖이면 탈락
        else:
            alive[cur] = 0
            return


for turn in range(1, M + 1):
    # 산타가 모두 탈락됐으면 break
    if sum(alive) == 0:
        break
    # 루돌프가 가장 가까이에 있는 산타로 이동 및 충돌 처리(최소값 초기값은 인피니트 안쓰는 게 좋음)
    min_value = 2 * N ** 2
    for idx in range(1, P + 1):
        # 1번부터 P까지 산타까지 거리를 측정
        if alive[idx] == 0:
            continue
        sr, sc = santa_info[idx]
        dist = (Rr - sr) ** 2 + (Rc - sc) ** 2
        if min_value > dist:
            min_value = dist
            minList = [(sr, sc, idx)]  # 갱신이 됐으면 리스트를 새로 만들어줌
        elif min_value == dist:
            minList.append((sr, sc, idx))
    minList.sort(reverse=True)  # 행이 크고 열이 큰 reverse정렬
    sr, sc, minIdx = minList[0]  # 목표 산타의 정보

    # 루돌프를 이동시키고 산타를 루돌프가 이동한 방향으로 1칸 움직임
    rdr = rdc = 0
    if Rr > sr:
        rdr = -1
    elif Rr < sr:
        rdr = 1

    if Rc > sc:
        rdc = -1
    elif Rc < sc:
        rdc = 1
    visited[Rr][Rc] = 0  # 루돌프 자리 지우기
    Rr, Rc = Rr + rdr, Rc + rdc  # 범위 체크 안해줘도 됨 why? 산타가 범위내에 있기때문
    visited[Rr][Rc] = -1  # 무조건 루돌프가 우선이기때문에(산타가 밀려나기 때문에) 표시

    # 만약 산타와 루돌프가 충돌했다면 충돌처리
    # 루돌프가 산타에 충돌한 경우 산타 밀림 처리
    if (Rr, Rc) == (sr, sc):
        # 충돌
        # 산타 C점 얻기
        # 주의 산타가 있던 자리를 0으로 지워버리면 루돌프가 지워지므로 생략

        score[minIdx] += C
        santa_turn[minIdx] = turn + 2
        # 산타가 밀리는건 연쇄적이므로 따로 함수로 처리
        move_santa(minIdx, sr, sc, rdr, rdc, C)  # minIdx 산타를 C칸 rdr, rdc 방향으로 이동

    #
    # 이제는 순서대로 루돌프에게 산타를 이동
    for idx in range(1, P + 1):
        # 탈락한지 확인
        if alive[idx] == 0:
            continue
        # 깨어날 턴이 아직 안된 경우
        if santa_turn[idx] > turn:
            continue

        sr, sc = santa_info[idx]
        # 루돌프에게 가까워 지는 방향으로 가야함
        # 현재보다 짧아야 이동을 하는것
        minDist = (Rr - sr) ** 2 + (Rc - sc) ** 2
        tempList = []

        # 상우하좌 순으로 최소거리 찾기
        for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            nr, nc = sr + dr, sc + dc
            dist = (Rr - nr) ** 2 + (Rc - nc) ** 2

            # 범위내, 산타없고, 최소값 갱신해야하는 경우
            if nr in range(N) and nc in range(N) and visited[nr][nc] <= 0 and minDist > dist:
                minDist = dist
                tempList.append((nr, nc, dr, dc))
        if len(tempList) == 0:
            continue

        nr, nc, dr, dc = tempList[-1]

        # 루돌프와 충돌 시 처리
        if (nr, nc) == (Rr, Rc):
            # 산타 C점 얻기
            score[idx] += D
            santa_turn[idx] = turn + 2
            visited[sr][sc] = 0

            # 산타가 밀리는건 연쇄적이므로 따로 함수로 처리

            move_santa(idx, nr, nc, -dr, -dc, D)  # minIdx 산타를 C칸 dr, dc 방향으로 이동
        else:
            # 빈칸으로 산타가 왔을 경우
            # 좌표갱신하고 이동처리
            visited[sr][sc] = 0
            visited[nr][nc] = idx
            santa_info[idx] = [nr, nc]

    # 깨어있는 산타(turn이 santa_turn보다 크거나 같아야)가 루돌프로 가장 가까운 방향으로 이동

    # 1부터 P까지 돌면서 살아있으면 자기점수에 1점씩 추가
    for i in range(1, P + 1):
        if alive[i] == 1:
            score[i] += 1
print(*score[1:])