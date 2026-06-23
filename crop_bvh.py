def crop_bvh(input_path, output_path, start_frame, end_frame):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 定位MOTION段关键行
    frames_line_idx = None
    frame_time_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("Frames:"):
            frames_line_idx = i
        if line.strip().startswith("Frame Time:"):
            frame_time_idx = i
            break

    if frame_time_idx is None:
        print("❌ 错误：未找到MOTION数据段")
        return

    # 数据起始行：Frame Time的下一行
    data_start = frame_time_idx + 1
    all_data = lines[data_start:]
    total_original = len(all_data)
    print(f"原文件总帧数：{total_original}")

    # 帧号转0索引（左闭右开切片）
    start_idx = start_frame - 1
    end_idx = end_frame

    if start_idx < 0 or end_idx > total_original:
        print(f"❌ 帧范围超限，原文件仅 {total_original} 帧")
        return

    # 截取数据
    cropped_data = all_data[start_idx:end_idx]
    new_frame_num = len(cropped_data)
    print(f"截取后帧数：{new_frame_num}")

    # 拼接新文件
    new_content = lines[:frames_line_idx]
    new_content.append(f"Frames: {new_frame_num}\n")
    new_content.append(lines[frame_time_idx])
    new_content.extend(cropped_data)

    # 写入新文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(new_content)
    print(f"✅ 截取完成，已保存到：{output_path}")


# ========== 按需修改参数 ==========
INPUT_FILE = "assets/lafan1/fallAndGetUp1_subject1.bvh"  # 原BVH路径
OUTPUT_FILE = "assets/lafan1/fallAndGetUp1_406_1950.bvh" # 输出新文件
START_FRAME = 406   # 起始帧（包含）
END_FRAME = 1950    # 结束帧（包含）
# =================================

crop_bvh(INPUT_FILE, OUTPUT_FILE, START_FRAME, END_FRAME)

