import xml.etree.ElementTree as ET

# 解析 XML 文件
tree = ET.parse('example.xml')
root = tree.getroot()

# 示例分析：获取根元素的标签名和属性
root_tag = root.tag
root_attrs = root.attrib
my_list = [1, 2, 3, 4, 5]
result = ""

# 输出结果
print(f"根元素标签名：{root_tag}")
print("根元素属性：")
for attr, value in root_attrs.items():
    print(f"{attr}: {value}")

# 示例分析：获取所有子元素的标签名和文本内容
print("所有子元素：")
for child in root:
    for grandson in child:
        for grandsonSon in grandson:
            #            print(f"{grandsonSon.text}", end=" ")
            result = result + grandsonSon.text + " "
        result = result + "\t"
        # print("", end="\t")
    my_list.append(result)
    result = ""

for ball in reversed(my_list):
    print(f"{ball}")
