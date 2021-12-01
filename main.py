import copy
import services
import pathlib

path = "png"
# PYTHON 3.6이상 필요, dict 정렬 관련.

# property를 path폴더 내부의 폴더들을 이용해 세팅함.
print("## properties init ##")
properties_list = list(pathlib.Path(path).glob("[!.]*"))
properties_list.sort()
print(properties_list)
# final_property = str(properties_list[len(properties_list) - 1])[len(path) + 1:]
# print("final_property")
# print(final_property)

properties = {}
for p in properties_list:
    properties[str(p)[len(path) + 1:]] = 0

# property_counts 세팅
property_counts = copy.deepcopy(properties)

for p in property_counts:
    property_path = path + '/' + p
    file_list = len(list(pathlib.Path(property_path).glob("*.png")))
    property_counts[p] = file_list

print("## property_counts ##")
print(property_counts)

limits = copy.deepcopy(properties)
limits_count = copy.deepcopy(properties)
result_properties = copy.deepcopy(properties)
final_properties = copy.deepcopy(properties)

for li in limits:
    limits[li] = {}
    limits_count[li] = {}
    result_properties[li] = []

for p in property_counts:
    for c in range(0, property_counts[p]):
        limits_count[p][c] = 0
        limits[p][c] = 9999

# ----- CUSTOM ----------------------------------
# limits["0_background"][0] = 1
# limits["1_body"][0] = 1
# limits["2_clothes"][0] = 1
# limits["3_head"][0] = 1
# limits["4_mustache"][0] = 1
# limits["5_hand"][0] = 1
# limits["0_background"][1] = 0
# limits["1_body"][1] = 0
# limits["2_clothes"][1] = 0
# limits["3_head"][1] = 0
# limits["4_mustache"][1] = 0
# limits["5_hand"][1] = 0
# ----- CUSTOM ----------------------------------

print("## limits ##")
print(limits)


def roop_result(c):
    for p in result_properties:
        services.randomSelect(c, property_counts, limits_count, limits, p, result_properties)
    str_at = ""
    for p in result_properties:
        str_at += str(result_properties[p][c]) + "_"
    if str_at not in onlyOne:
        onlyOne[str_at] = True
    else:
        for p in result_properties:
            limits_count[p][result_properties[p][-1]] -= 1
            result_properties[p].pop()
        roop_result(c)


# make!
create_count = 10000
onlyOne = {};
for c in range(0, create_count):
    roop_result(c)

print("## OnlyOne")
print(onlyOne)

# 갯수 검증
print("## final properties count is : ##")
print(limits_count)
for li in limits_count:
    count = 0
    for c in limits_count[li]:
        count = count + limits_count[li][c]
    final_properties[li] = count

print(final_properties)
print("##################################")

# 테스트용
# properties = {"background": [0], "body": [1], "clothes": [5], "head": [0], "mustache": [8],
#               "hand": [5]}
# properties["clothes"]

print("## result_properties ##")
print(result_properties)

# makeImages
services.makeImage(result_properties, create_count, path, properties)
