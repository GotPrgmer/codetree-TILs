import sys
from collections import deque

n, m = map(int, input().split())

queue = deque()
# 초밥을 담을 배열 추가
for _ in range(n):
    queue.append(deque())

people_dict = {}
# 이전 시간 기록 ( 초밥 회전을 위해 ), 초밥 갯수
prev_time, cnt = 0, 0

for _ in range(m):
    now_info = list(input().split())
    # 시간만큼 초밥 회전하기
    queue.rotate(int(now_info[1]) - prev_time)
    prev_time = int(now_info[1])
    
    # 초밥 만들기
    if now_info[0] == '100':
        queue[int(now_info[2])].append(now_info[3])
        cnt += 1
    # 손님
    if now_info[0] == '200':
        # 손님 추가하기
        if int(now_info[2]) not in people_dict:
            people_dict[int(now_info[2])] = [now_info[3], int(now_info[4])]
        elif people_dict[int(now_info[2])][0] == "":
            people_dict[int(now_info[2])] = [now_info[3], int(now_info[4])]
    # 초밥 먹기
    for i in range(n):
        sub_list = []
        while queue[i]:
            now_name = queue[i].popleft()

            # 사람이 있을 경우
            if i in people_dict and people_dict[i][0] == now_name:
                if people_dict[i][1] > 0:
                    people_dict[i][1] -= 1
                    cnt -= 1
                # 초기화
                if people_dict[i][1] == 0:
                    people_dict[i][0] = ""
            else:
                sub_list.append(now_name)
        # 먹지 못한 초밥 다시 넣어놓기
        for sub in sub_list:
            queue[i].append(sub)
    
    # 사진 찍기
    if now_info[0] == '300':
        people_cnt = 0

        for k, v in people_dict.items():
            if v[0] != "":
                people_cnt += 1
        
        print(people_cnt, cnt)