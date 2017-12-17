# тестовые штуки, в процессе не участвуют


# рандомное заполнение матрицы расположений
# import random
# s = ""
# for i in range(15):
#     s+="["
#     for j in range(15):
#         if j > i:
#             r = random.randint(1,6)
#             if r == 1:
#                 s+="\'A\',"
#             if r == 2:
#                 s+="\'E\',"
#             if r == 3:
#                 s+="\'I\',"
#             if r == 4:
#                 s+="\'O\',"
#             if r == 5:
#                 s+="\'U\',"
#             if r == 6:
#                 s+="\'X\',"
#         else:
#             s += "\'Z\',"
#     s+="]\n"
# print(s)

from Settings import get_test_settings
import json
traffic = get_test_settings()["traffic"]
f = open("settings.txt",'w')
json.dump(get_test_settings(),f)
