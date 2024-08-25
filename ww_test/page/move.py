# from collections import deque

# def reconstruct_path(came_from, start, goal):
#     path = []
#     current = goal
#     while current != start:
#         path.append(current)
#         current = came_from[current]
#     path.append(start)
#     path.reverse()
#     return path

# def find_path(start, goal, movable_areas):
#     queue = deque()
#     queue.append(start)
#     visited = set()
#     came_from = {}

#     while queue:
#         current = queue.popleft()

#         if current == goal:
#             return reconstruct_path(came_from, start, goal)

#         for area in movable_areas:
#             if area[0][0] <= current[0] <= area[1][0] and area[0][1] <= current[1] <= area[1][1]:
#                 for neighbor in [(current[0] - 1, current[1]), (current[0] + 1, current[1]),
#                                  (current[0], current[1] - 1), (current[0], current[1] + 1)]:
#                     if neighbor in visited:
#                         continue

#                     if is_position_valid(neighbor, movable_areas):
#                         queue.append(neighbor)
#                         visited.add(neighbor)
#                         came_from[neighbor] = current

#     return None  # 没有找到路径

# def is_position_valid(position, movable_areas):
#     for area in movable_areas:
#         if area[0][0] <= position[0] <= area[1][0] and area[0][1] <= position[1] <= area[1][1]:
#             return True
#     return False

# # 示例使用
# start = (49.47, 38.10)
# goal = (48.41, 34.60)
# movable_areas = [((49.47, 38.10), (52.60, 38.10)), ((49.47, 34.60), (52.60, 34.60)),((48.41, 34.60),(51.10, 34.60),(48.41, 31.40),(51.10, 31.40))]  # 可移动范围区域的四个角落顶点坐标

# path = find_path(start, goal, movable_areas)
# print(path)
# # if path:
# #     for position in path:
# #         move(position)
# # else:
# #     print("无法找到路径")



# import heapq

# def heuristic_cost_estimate(start, goal):
#     # 使用曼哈顿距离作为启发式估计函数
#     return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

# def reconstruct_path(came_from, current):
#     path = []
#     while current is not None:
#         path.append(current)
#         current = came_from[current]
#     path.reverse()
#     return path

# def find_path(start, goal, movable_areas):
#     open_set = []
#     heapq.heappush(open_set, (0, start))
#     came_from = {}
#     g_score = {start: 0}
#     f_score = {start: heuristic_cost_estimate(start, goal)}

#     while open_set:
#         _, current = heapq.heappop(open_set)

#         if current == goal:
#             return reconstruct_path(came_from, current)

#         for area in movable_areas:
#             if area[0][0] <= current[0] <= area[1][0] and area[0][1] <= current[1] <= area[1][1]:
#                 for neighbor in [(current[0] - 1, current[1]), (current[0] + 1, current[1]),
#                                  (current[0], current[1] - 1), (current[0], current[1] + 1)]:
#                     if not is_position_valid(neighbor, movable_areas):
#                         continue

#                     tentative_g_score = g_score[current] + 1

#                     if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
#                         came_from[neighbor] = current
#                         g_score[neighbor] = tentative_g_score
#                         f_score[neighbor] = g_score[neighbor] + heuristic_cost_estimate(neighbor, goal)
#                         heapq.heappush(open_set, (f_score[neighbor], neighbor))

#     return None  # 没有找到路径

# def is_position_valid(position, movable_areas):
#     for area in movable_areas:
#         if area[0][0] <= position[0] <= area[1][0] and area[0][1] <= position[1] <= area[1][1]:
#             return True
#     return False

# # 示例使用
# start = (49.47, 38.10)
# goal = (48.41, 34.60)
# movable_areas = [((49.47, 38.10), (52.60, 38.10)), ((49.47, 34.60), (52.60, 34.60)),((48.41, 34.60),(51.10, 34.60),(48.41, 31.40),(51.10, 31.40))]  # 可移动范围区域的四个角落顶点坐标

# path = find_path(start, goal, movable_areas)
# # if path:
# #     for position in path:
# #         move(position)
# # else:
# #     print("无法找到路径")
# print(path)


# import heapq

# def heuristic_cost_estimate(start, goal):
#     # 使用曼哈顿距离作为启发式估计函数
#     return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

# def reconstruct_path(came_from, current):
#     path = []
#     while current is not None:
#         path.append(current)
#         current = came_from[current]
#     path.reverse()
#     return path

# def find_path(start, goal, movable_areas):
#     grid_size = 0.5  # 网格大小，根据具体情况调整
#     start = (int(start[0] / grid_size), int(start[1] / grid_size))
#     goal = (int(goal[0] / grid_size), int(goal[1] / grid_size))

#     open_set = []
#     heapq.heappush(open_set, (0, start))
#     came_from = {}
#     g_score = {start: 0}
#     f_score = {start: heuristic_cost_estimate(start, goal)}

#     while open_set:
#         _, current = heapq.heappop(open_set)

#         if current == goal:
#             return reconstruct_path(came_from, current)

#         for area in movable_areas:
#             if area[0][0] <= current[0] * grid_size <= area[1][0] and area[0][1] <= current[1] * grid_size <= area[1][1]:
#                 for neighbor in [(current[0] - 1, current[1]), (current[0] + 1, current[1]),
#                                  (current[0], current[1] - 1), (current[0], current[1] + 1)]:
#                     if not is_position_valid(neighbor, movable_areas, grid_size):
#                         continue

#                     tentative_g_score = g_score[current] + 1

#                     if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
#                         came_from[neighbor] = current
#                         g_score[neighbor] = tentative_g_score
#                         f_score[neighbor] = g_score[neighbor] + heuristic_cost_estimate(neighbor, goal)
#                         heapq.heappush(open_set, (f_score[neighbor], neighbor))

#     return None  # 没有找到路径

# def is_position_valid(position, movable_areas, grid_size):
#     for area in movable_areas:
#         if area[0][0] <= position[0] * grid_size <= area[1][0] and area[0][1] <= position[1] * grid_size <= area[1][1]:
#             return True
#     return False

# # 示例使用
# start = (49.47, 38.10)
# goal = (48.41, 34.60)
# movable_areas = [((49.47, 38.10), (52.60, 38.10)), ((49.47, 34.60), (52.60, 34.60)),((48.41, 34.60),(51.10, 34.60),(48.41, 31.40),(51.10, 31.40))]  # 可移动范围区域的四个角落顶点坐标

# path = find_path(start, goal, movable_areas)

# print(path)

import heapq

def heuristic_cost_estimate(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

def reconstruct_path(came_from, current, grid_size):
    path = []
    while current is not None:
        path.append((current[0] * grid_size, current[1] * grid_size))
        current = came_from[current]
    path.reverse()
    return path

def find_path(start, goal, movable_areas):
    grid_size = 0.01  # 网格大小，根据具体情况调整
    start = (int(start[0] / grid_size), int(start[1] / grid_size))
    goal = (int(goal[0] / grid_size), int(goal[1] / grid_size))

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic_cost_estimate(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current, grid_size)

        for area in movable_areas:
            if area[0][0] <= current[0] * grid_size <= area[1][0] and area[0][1] <= current[1] * grid_size <= area[1][1]:
                for neighbor in [(current[0] - 1, current[1]), (current[0] + 1, current[1]),
                                 (current[0], current[1] - 1), (current[0], current[1] + 1)]:
                    if not is_position_valid(neighbor, movable_areas, grid_size):
                        continue

                    tentative_g_score = g_score[current] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = g_score[neighbor] + heuristic_cost_estimate(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # 没有找到路径

def is_position_valid(position, movable_areas, grid_size):
    for area in movable_areas:
        if area[0][0] <= position[0] * grid_size <= area[1][0] and area[0][1] <= position[1] * grid_size <= area[1][1]:
            return True
    return False

# 示例使用
start = (49.47, 38.10)
goal = (48.41, 34.60)
movable_areas = [((49.47, 38.10), (52.60, 38.10)), ((49.47, 34.60), (52.60, 34.60)),((48.41, 34.60),(51.10, 34.60),(48.41, 31.40),(51.10, 31.40))]  # 可移动范围区域的四个角落顶点坐标

path = find_path(start, goal, movable_areas)

print(path)