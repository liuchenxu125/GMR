#!/usr/bin/env python3
import sys  # 新增：导入sys模块读取命令行参数
import os   # 新增：导入os模块处理路径/文件夹创建

def cut_bvh_keep_range(input_path, output_path, keep_start, keep_end):
    """
    保留BVH文件中 [keep_start, keep_end] 帧（闭区间，帧索引从0开始）
    :param input_path: 输入BVH文件路径
    :param output_path: 输出BVH文件路径
    :param keep_start: 保留的起始帧（如680）
    :param keep_end: 保留的结束帧（如800）
    """
    # 读取原始BVH文件
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]

    # 分离HIERARCHY（骨骼层次）和MOTION（运动数据）
    hierarchy_lines = []
    motion_meta_lines = []  # Frames: xxx 和 Frame Time: xxx
    motion_frame_lines = []
    in_motion_section = False

    for line in lines:
        stripped_line = line.strip()
        # 标记进入MOTION段
        if stripped_line == "MOTION":
            in_motion_section = True
            hierarchy_lines.append(line)
            continue
        
        if in_motion_section:
            # 处理MOTION段的元数据（帧数、帧时间）
            if stripped_line.startswith("Frames:"):
                total_frames = int(stripped_line.split()[1])
                motion_meta_lines.append(line)
            elif stripped_line.startswith("Frame Time:"):
                motion_meta_lines.append(line)
            elif stripped_line != "":  # 处理帧数据行（非空）
                motion_frame_lines.append(line)
        else:
            # 保留HIERARCHY段（骨骼结构不能改）
            hierarchy_lines.append(line)

    # 校验帧范围（防止越界）
    keep_start = max(0, keep_start)
    keep_end = min(total_frames - 1, keep_end)
    if keep_start > keep_end:
        raise ValueError(f"错误：起始帧{keep_start}大于结束帧{keep_end}（总帧数：{total_frames}）")

    # 提取目标帧（闭区间，所以+1）
    selected_frames = motion_frame_lines[keep_start:keep_end + 1]
    new_frame_count = len(selected_frames)

    # 生成新的MOTION元数据（更新帧数）
    new_motion_meta = [
        motion_meta_lines[0].replace(str(total_frames), str(new_frame_count)),
        motion_meta_lines[1]  # 保留帧时间
    ]

    # 拼接新BVH内容并保存
    new_bvh_content = hierarchy_lines + new_motion_meta + selected_frames
    
    # 新增：自动创建输出文件夹（如果不存在）
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"📁 自动创建输出文件夹：{output_dir}")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_bvh_content))

    # 打印结果确认
    print("="*50)
    print(f"✅ BVH剪切完成！")
    print(f"原始文件：{input_path}（总帧数：{total_frames}）")
    print(f"输出文件：{output_path}（保留帧数：{new_frame_count}，{keep_start}-{keep_end}帧）")
    print("="*50)

# 核心配置：支持命令行传参 + 保留默认值（兼容原有用法）
if __name__ == "__main__":
    # 读取命令行参数（规则：参数顺序为 输入路径 → 输出路径 → 起始帧 → 结束帧）
    if len(sys.argv) == 5:
        # 命令行传参模式
        INPUT_BVH = sys.argv[1]
        OUTPUT_BVH = sys.argv[2]
        KEEP_START_FRAME = int(sys.argv[3])
        KEEP_END_FRAME = int(sys.argv[4])
    elif len(sys.argv) == 1:
        # 无参数模式（使用默认值，兼容原有用法）
        INPUT_BVH = "fallAndGetUp1_subject1.bvh"       # 默认输入文件
        OUTPUT_BVH = "fallAndGetUp1_subject1_680_800.bvh"  # 默认输出文件
        KEEP_START_FRAME = 680  # 默认起始帧
        KEEP_END_FRAME = 800    # 默认结束帧
    else:
        # 参数数量错误：提示用法
        print("❌ 参数错误！正确用法：")
        print("用法1（命令行传参）：python cut_bvh.py <输入BVH路径> <输出BVH路径> <起始帧> <结束帧>")
        print("示例1：python cut_bvh.py fallAndGetUp1_subject1.bvh ./amp/cut.bvh 680 800")
        print("用法2（默认值）：python cut_bvh.py")
        sys.exit(1)  # 退出脚本，避免执行后续代码

    # 执行剪切
    cut_bvh_keep_range(INPUT_BVH, OUTPUT_BVH, KEEP_START_FRAME, KEEP_END_FRAME)
