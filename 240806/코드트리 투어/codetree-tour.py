import sys
import heapq


def input():
    return sys.stdin.readline().rstrip()


def cost(start, n):
    global dp
    # 다익스트라
    dp = [INF] * (n)
    visited = [False] * n
    dp[start] = 0
    for i in range(n):
        v = -1
        minDist = INF
        for j in range(n):
            # 방문하지 않았고 최소값보다 갱신값이 더 작으면
            # 해당 노드를 방문해야함
            # 해당 과정으로 n번 돌려서 갱신할 수 있는 값중 가장 작은 값을 찾아서 방문
            if not visited[j] and minDist > dp[j]:
                v = j
                minDist = dp[j]
        visited[v] = True
        for j in range(n):
            if graph[v][j] != INF and dp[j] > graph[v][j] + dp[v]:
                dp[j] = dp[v] + graph[v][j]


def buildLand(n, m, lst):
    global N, M
    global graph
    N = n
    M = m
    # 외부에있는 graph초기화해서 만들어주기
    graph = [[INF] * N for _ in range(N)]
    for i in range(N):
        graph[i][i] = 0
    for i in range(0, len(lst), 3):
        u, v, w = lst[i], lst[i + 1], lst[i + 2]

        graph[u][v] = min(graph[u][v], w)
        graph[v][u] = min(graph[v][u], w)
    return graph


def createTravel(lst):
    global dp
    travel_id = lst[0]
    revenue = lst[1]
    dest = lst[2]
    isMade[travel_id] = True
    profit = revenue - dp[dest]
    heapq.heappush(travel, [-(profit), travel_id, revenue, dest])


def cancelTravel(travel_id):
    if isMade[travel_id]:
        isCancel[travel_id] = True


def sellTravel():
    while travel:
        # 최적이라고 생각한 여행 상품이 판매 불가능하다면 while빠져나감
        travel_item = travel[0]
        if travel_item[0] > 0:
            break
        heapq.heappop(travel)
        # 제거되지 않음
        if not isCancel[travel_item[1]]:
            return travel_item[1]
    return -1


def changeStart(start, n):
    # dp를 다시 갱신
    cost(start, n)
    new_travel = []
    while travel:
        new_travel.append(heapq.heappop(travel))
    for travel_item in new_travel:
        createTravel(travel_item[1:])


N, M = 0, 0
# 각 경로 정보
graph = []
# 다익스트라
dp = []

MAX_N = 2000
MAX_ID = 30005
INF = float('INF')

travel = []
Q = int(input())
isMade = [False] * MAX_ID
isCancel = [False] * MAX_ID

for _ in range(Q):
    query = list(map(int, input().split()))
    T = query[0]
    if T == 100:
        graph = buildLand(query[1], query[2], query[3:])
        cost(0, N)
    elif T == 200:
        createTravel(query[1:])
    elif T == 300:
        cancelTravel(query[1])
    elif T == 400:
        print(sellTravel())
    else:
        changeStart(query[1], N)