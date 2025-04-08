import json
from pathlib import Path

from assemblers.hybridspades_runner import run_hybridspades
from assemblers.megahit_runner import run_megahit
from assemblers.metaflye_runner import run_metaflye
from assemblers.operams_runner import run_opera_ms
from recommend_assemble.config.config import SAMPLE_COMBO_PATH

CONFIG_PATH = Path("config/sample_combos.json")
OUTPUT_DIR = Path("output")

def main():
    with open(SAMPLE_COMBO_PATH) as f:
        combos = json.load(f)
    # ========== SHORT_SHORT ==========
    for sample in combos.get("short_short", []):
        sample_name = sample["sample_name"]
        reads = sample["reads"]
        try:
            run_megahit(sample_name, reads)
        except Exception as e:
            print(f"❌ short_short [{sample_name}] 运行失败: {e}")

    # ========== SHORT_LONG ==========
    for sample in combos.get("short_long", []):
        sample_name = sample["sample_name"]
        reads = sample["reads"]
        long_read = sample["long_read"]
        try:
            run_hybridspades(sample_name, reads, long_read)
            run_opera_ms(sample_name, reads, long_read)
            run_metaflye(sample_name, long_read, is_hybrid=True)
        except Exception as e:
            print(f"❌ short_long [{sample_name}] 运行失败: {e}")

    # ========== LONG_LONG ==========
    for sample in combos.get("long_long", []):
        sample_name = sample["sample_name"]
        long_read = sample["long_read"]
        try:
            run_metaflye(sample_name, long_read)
        except Exception as e:
            print(f"❌ long_long [{sample_name}] 运行失败: {e}")

if __name__ == "__main__":
    main()
