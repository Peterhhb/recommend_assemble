import json
import re
from collections import defaultdict
from pathlib import Path

from recommend_assemble.config.config import SHORT_READS_DIR, LONG_READS_DIR, CONFIG_DIR, OUTPUT_DIR


# 目录设置
# PROJECT_ROOT = Path(__file__).resolve().parent.parent
# DATA_DIR = PROJECT_ROOT / "data"
# SHORT_READS_DIR = DATA_DIR / "short"
# LONG_READS_DIR = DATA_DIR / "long"
# OUTPUT_DIR = PROJECT_ROOT / "output"
# CONFIG_DIR = PROJECT_ROOT / "config"

# 创建目录结构
def setup_directories():
    for path in [SHORT_READS_DIR, LONG_READS_DIR, CONFIG_DIR]:
        path.mkdir(parents=True, exist_ok=True)
    for name in ["short_short", "short_long", "long_long"]:
        (OUTPUT_DIR / name).mkdir(parents=True, exist_ok=True)
    print("✅ 所有目录已创建")

# 自动识别短读配对
def find_short_reads():
    pairs = defaultdict(dict)
    print("\n🔍 扫描短读文件:")
    for file in SHORT_READS_DIR.glob("*.fastq.gz"):
        print(f"  找到文件：{file.name}")

        # 正则：匹配 _R1 或 _R2，支持后缀 .mini.fastq.gz 或 .fastq.gz
        match = re.match(r"(.*)_R(1|2)(?:\.mini)?\.fastq\.gz", file.name)
        if match:
            sample_name, pair_num = match.groups()
            read_key = f"read{pair_num}"
            pairs[sample_name][read_key] = str(file.resolve())
            print(f"    ✅ 匹配样本：{sample_name}, {read_key}")
        else:
            print(f"   ⚠️ 文件名不匹配 R1/R2 模式，跳过")

    # 只返回包含 read1 和 read2 的样本
    complete_pairs = {
        k: v for k, v in pairs.items()
        if "read1" in v and "read2" in v
    }

    print(f"🔎 总共识别出 {len(complete_pairs)} 个有效短读样本对")
    return complete_pairs


# 获取长读
def find_long_reads():
    return [str(f.resolve()) for f in LONG_READS_DIR.glob("*.fastq.gz")]

# 自动组合所有组装方式
def generate_combinations(short_reads, long_reads):
    combos = {
        "short_short": [],
        "short_long": [],
        "long_long": [],
    }
    for sname, reads in short_reads.items():
        combos["short_short"].append({
            "sample_name": sname,
            "reads": reads,
        })
        for lread in long_reads:
            combos["short_long"].append({
                "sample_name": f"{sname}+{Path(lread).stem}",
                "reads": reads,
                "long_read": lread
            })
    for lread in long_reads:
        combos["long_long"].append({
            "sample_name": Path(lread).stem,
            "long_read": lread
        })
    return combos

# 保存为 JSON 配置
def save_combinations(combos):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    output_path = CONFIG_DIR / "sample_combos.json"
    with open(output_path, "w") as f:
        json.dump(combos, f, indent=4)
    print(f"✅ 组合信息已保存到 {output_path}")

# 主流程
if __name__ == "__main__":
    setup_directories()
    short_reads = find_short_reads()
    long_reads = find_long_reads()
    combos = generate_combinations(short_reads, long_reads)
    save_combinations(combos)
