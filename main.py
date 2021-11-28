import copy
import os
import random
import services
import pathlib

# TODO head와 clothes의 일부 처럼 겹치는 경우


# property_counts 세팅
property_counts = {"background": 0, "body": 0, "clothes": 0, "head": 0, "moustache": 0,
                   "hand": 0}
property = copy.deepcopy(property_counts)

path = "png"
for p in property_counts:
    property_path = path + '/' + p
    file_list = len(list(pathlib.Path(property_path).glob("*.png")))
    property_counts[p] = file_list

print("## property_counts ##")
print(property_counts)

# limits and count 세팅
limits = {"background": {}, "body": {}, "clothes": {}, "head": {}, "moustache": {},
          "hand": {}}
limits_count = {"background": {}, "body": {}, "clothes": {}, "head": {}, "moustache": {},
                "hand": {}}

for p in property_counts:
    for c in range(0, property_counts[p]):
        limits_count[p][c] = 0
        limits[p][c] = 9999

limits["background"][1] = 2

print("## limits_count ##")
print(limits)

properties = {"background": [], "body": [], "clothes": [], "head": [], "moustache": [],
              "hand": []}


def randomSelect(num):
    random_num = random.randrange(0, property_counts[p])
    if limits_count[p][random_num] < limits[p][random_num]:
        if p == "head":
            if properties["clothes"][num] == 5:
                properties[p].append(0)
                limits_count[p][0] = limits_count[p][0] + 1
                return
        properties[p].append(random_num)
        limits_count[p][random_num] = limits_count[p][random_num] + 1
    else:
        randomSelect(num)


# make!
count = 3

for c in range(0, count):
    for p in properties:
        randomSelect(c)

# 테스트용
# properties = {"background": [0], "body": [1], "clothes": [5], "head": [0], "moustache": [8],
#               "hand": [5]}
# properties["clothes"]

print("## properties ##")
print(properties)

# makeImages
services.makeImage(properties, count, path, property)
