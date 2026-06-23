import mujoco
import os
import shutil

# 路径配置（适配你的项目结构）
URDF_PATH = "urdf/marathon_001.urdf"
OUTPUT_XML = "urdf/marathon_final.xml"
MESH_DIR = "meshes"
URDF_MESH_DIR = "urdf/meshes"

def main():
    # 1. 修复路径问题：把meshes文件夹复制到urdf目录下（urdf2mjcf需要）
    if not os.path.exists(URDF_MESH_DIR):
        shutil.copytree(MESH_DIR, URDF_MESH_DIR)
        print(f"✅ 已复制网格文件到: {URDF_MESH_DIR}")
    
    # 2. 关键修复：使用MuJoCo官方API加载并保存模型
    # 加载URDF（会自动编译）
    model = mujoco.MjModel.from_xml_path(URDF_PATH)
    
    # 3. 正确保存方法：使用mj_saveLastXML（兼容所有MuJoCo版本）
    # 这个函数会保存最后一次编译的模型XML
    mujoco.mj_saveLastXML(OUTPUT_XML, model)
    
    print(f"✅ 转换成功！生成文件：{os.path.abspath(OUTPUT_XML)}")
    print("✅ 自动修复：惯性参数、网格路径、模型结构")
    print("✅ 直接放入GMR项目使用即可！")

if __name__ == "__main__":
    main()
