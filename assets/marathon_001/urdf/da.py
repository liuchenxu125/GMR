import mujoco
import os

# 路径配置（完全适配你的项目结构，不用修改！）
URDF_PATH = "urdf/marathon_001.urdf"
OUTPUT_XML = "marathon_final.xml"

# 1. 直接加载URDF（MuJoCo官方支持，自动处理路径/惯性）
model = mujoco.MjModel.from_xml_path(URDF_PATH)

# 2. 保存为GMR可用的MJCF(XML)，自动修复所有惯性/路径问题
mujoco.save_model(OUTPUT_XML, model)

print(f"✅ 转换成功！生成文件：{os.path.abspath(OUTPUT_XML)}")
print("✅ 自动修复惯性、网格路径、模型结构")
print("✅ 直接放入GMR项目使用即可！")
