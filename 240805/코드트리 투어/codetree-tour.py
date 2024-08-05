import sys
import heapq


def input():
    return sys.stdin.readline().rstrip()


def cost(start, n):
    global dp
    # 다익스트라
    q = []
    dp = [float('INF')] * (n)
    heapq.heappush(q, [0, start])
    while q:
        sum_value, cur = heapq.heappop(q)
        if dp[cur] < sum_value:
            continue
        # 갱신
        dp[cur] = sum_value
        for value, node in graph[cur]:
            if dp[node] > dp[cur] + value:
                heapq.heappush(q, [dp[cur] + value, node])



def buildLand(lst, n):
    global graph
    # 외부에있는 graph초기화해서 만들어주기
    graph = [[] for _ in range(n)]
    for i in range(0, len(lst), 3):
        graph[lst[i]].append([lst[i + 2], lst[i + 1]])
        graph[lst[i + 1]].append([lst[i + 2], lst[i]])
    # print(graph)


def createTravel(lst):
    global delete_set
    global dp
    travel_id = lst[0]
    revenue = lst[1]
    dest = lst[2]
    # print(travel_id,revenue,dest,dp[dest])
    # delete_set에 안들어가야 넣음
    if travel_id not in delete_set:
        #id, 매출, 도착지, 거리
        heapq.heappush(travel, [-(revenue-dp[dest]),travel_id,revenue, dest,dp[dest]])



def cancelTravel(lst):
    delete_id = lst[0]
    delete_set.add(delete_id)


def sellTravel():
    global travel
    ans = -1
    q = []
    while travel:
        total,travel_id,revenue, dest,distance= heapq.heappop(travel)
        if travel_id in delete_set:
            continue
        else:
            if -total < 0:
                q.append([total,travel_id, revenue,dest,dp[dest]])
                continue
            ans = travel_id
            break
    #q에 있는것들 다시 넣기
    for info in q:
        heapq.heappush(travel,info)
    print(ans)


def changeStart():
    global travel
    global dp
    # dp를 다시 갱신
    # print("변경전",dp)
    q = []
    # print("변경후",dp)
    # 현재 존재하는 여행 상품들의 거리들을 변경
    # print(dp[4],"ㅓㅓㅓ")\
    dp = dp[:]
    entire_length = len(travel)
    cnt = 0
    while cnt<entire_length:
        cnt += 1
        total,travel_id,revenue, dest,distance = heapq.heappop(travel)
        change = dp[dest]
        # print(dest,dp[dest])
        # print(change)
        heapq.heappush(q, [-(revenue-change),travel_id, revenue, dest, change])
    travel = q[:]



graph = []
dp = []
delete_set = set()
travel = []
Q = int(input())
n = -1
m = -1
for _ in range(Q):
    input_list = list(map(int, input().split()))
    if input_list[0] == 100:
        n = input_list[1]
        m = input_list[2]
        buildLand(input_list[3:], n)
        # print(graph)
        cost(0, n)
        # print("다익스트라 출력",dp)
    elif input_list[0] == 200:
        createTravel(input_list[1:])
        # print("여행상품 추가",travel)
    elif input_list[0] == 300:
        cancelTravel(input_list[1:])
        # print("취소",input_list[1:])
    elif input_list[0] == 400:
        sellTravel()
        # print("팔기 판매여행상품",travel)
    else:
        cost(input_list[1], n)
        changeStart()
        # print("변경 판매여행상품",travel)