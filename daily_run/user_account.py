# -*- coding:utf-8 -*-
import os

print("be happy")


class UserAccount(object):

    def __init__(self, dir):

        self.now_status = []
        self.his_status = []
        self.dir = dir

        ua_list = os.listdir(dir)
        ua_list.sort(key=lambda x: int(x.split("_")[-1]), reverse=True)

        path = os.path.join(dir, ua_list[0])
        with open(path, "r") as finput:
            for line in finput:
                if "#" not in line and len(line) >= 2:
                    content = line.strip().split(",")
                    if "now" in line:
                        # 000016.sh,100,20,now
                        self.now_status.append([content[0], float(content[1]), float(content[2])])
                    elif "his" in line:
                        # 000016.sh, 100, 20, in, his
                        self.his_status.append([content[0], float(content[1]), float(content[2]), content[3]])
                    elif "money" in line:
                        self.left_money = float(content[0])

    def save_status(self):

        ua_list = os.listdir(dir)
        ua_list.sort(key=lambda x: int(x.split("_")[-1]), reverse=True)

        path_prefix = "_".join(ua_list[0].split("_")[:-1])
        path_num = 1 + int(ua_list[0].split("_")[-1])
        path = os.path.join(self.dir, "%s_%s" % (path_prefix, path_num))
        print(path)
        with open(path, "w") as foutput:
            foutput.write("# 可用资金\n")
            foutput.write(str(self.left_money) + ",money\n")
            foutput.write("\n")
            foutput.write("# 持仓状态：代码，股数，平均成本\n")
            for now in self.now_status:
                now = [str(x) for x in now]
                foutput.write(",".join(now) + ",now\n")
            foutput.write("\n")
            foutput.write("# 交易历史:代码，股数，平均成本，操作类型(in、out)\n")
            for his in self.his_status:
                his = [str(x) for x in his]
                foutput.write(",".join(his) + "his\n")
            foutput.write("\n")




dir = "../resource/user_account"
ua = UserAccount(dir)
ua.save_status()
