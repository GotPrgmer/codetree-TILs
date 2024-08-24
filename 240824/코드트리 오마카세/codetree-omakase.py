import heapq
from collections import deque,defaultdict

L, Q = map(int, input().split())

query = []
saram_entry_time = defaultdict(int)
saram_position = defaultdict(int)
saram_exit_time = defaultdict(int)
names = set()
saram_sushi_query = defaultdict(list)

#데이터 입력
for _ in range(Q):
    data = list(map(str,input().split()))
    cmd_type = int(data[0])
    t, x, n = -1, -1, -1
    name = ""

    if cmd_type == 100:
        t, x, name = data[1:]
        t = int(t)
        x = int(x)

    if cmd_type == 200:
        t, x, name, n = data[1:]
        t = int(t)
        x = int(x)
        n = int(n)

    if cmd_type == 300:
        t = int(data[1])

    #t가 같다면 cmd_type으로 구분
    heapq.heappush(query,(t,cmd_type,x,name,n))

    #사람별로 초밥생성을 기준으로 연산
    if cmd_type == 100:
        saram_sushi_query[name].append((t,cmd_type,x,name,n))
    if cmd_type == 200:
        names.add(name)
        saram_entry_time[name]=t
        saram_position[name]=x



#이름별로 초밥 생성할때마다 원하는 만큼 먹고 언제 사람이 떠나는지 갱신
for name in names:
    #사람 이름별 초밥 생성
    for t,cmd,x,p_name,n in saram_sushi_query[name]:
        when_eat = 0
        #사람 들어오기전에 초밥 생성
        if t < saram_entry_time[name]:
            t_diff = saram_entry_time[name]-t
            sushi_position = (x+t_diff)%L
            #사람이 들어온 시각으로 초기화
            when_eat = saram_entry_time[name]
            if sushi_position>saram_position[name]:
                add_time = L - (sushi_position-saram_position[name])
                when_eat += add_time
            elif sushi_position<saram_position[name]:
                add_time = (saram_position[name]-sushi_position)
                when_eat += add_time
            

        #사람이 들어오고 초밥 생성
        else:
            #사람이 들어온 시각으로 초기화
            when_eat = t
            if x>saram_position[name]:
                add_time = l - (x-saram_position[name])
                when_eat += add_time
            elif x<saram_position[name]:
                add_time = saram_position[name]-x
                when_eat += add_time
            

        saram_exit_time[name] = max(when_eat,saram_exit_time[name])
        #초밥 사라지는 쿼리 추가
        heapq.heappush(query,(when_eat,101,-1,name,-1))

for name in names:
    heapq.heappush(query,(saram_exit_time[name],201,-1,name,-1))

ppl_num = 0
sushi_num = 0
while query:
    cur = heapq.heappop(query)
    cmd = cur[1]
    if cmd == 100:
        sushi_num += 1
    elif cmd == 101:
        sushi_num -= 1
    elif cmd == 200:
        ppl_num += 1
    elif cmd == 201:
        ppl_num -= 1
    else:
        print(ppl_num,sushi_num)