from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 数据目录
DATA_DIR = PROJECT_ROOT / "data"
SHORT_READS_DIR = DATA_DIR / "short"
LONG_READS_DIR = DATA_DIR / "long"

# 配置文件目录
CONFIG_DIR = PROJECT_ROOT / "config"
SAMPLE_COMBO_PATH = CONFIG_DIR / "sample_combos.json"

# 输出路径
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_PATHS = {
    "short_short": OUTPUT_DIR / "short_short",
    "short_long": OUTPUT_DIR / "short_long",
    "long_long": OUTPUT_DIR / "long_long"
}

# 工具输出路径拼接函数
def get_tool_output_path(combo_type, sample_name, tool_name):
    return OUTPUT_PATHS[combo_type] / sample_name / tool_name
