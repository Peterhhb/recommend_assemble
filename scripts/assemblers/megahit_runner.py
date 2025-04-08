import subprocess

from recommend_assemble.config.config import OUTPUT_PATHS
from recommend_assemble.scripts.utils.utils import run_metaquast, run_checkm2, save_feature_summary, run_ss_sembin


# OUTPUT_DIR = Path("output/short_short")

def run_megahit(sample_name, reads):
    sample_out = OUTPUT_PATHS['short_short'] / sample_name
    megahit_dir = sample_out / "megahit"
    final_contig = megahit_dir / "final.contigs.fa"

    # 🏗️ 保证目录存在
    megahit_dir.mkdir(parents=True, exist_ok=True)
    sembin_dir = sample_out/"sembin"
    sembin_dir.mkdir(parents=True, exist_ok=True)
    eval_dir = sample_out / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)

    # 🧬 组装
    if not final_contig.exists():
        cmd = [
            "megahit",
            "-1", reads["read1"],
            "-2", reads["read2"],
            "-o", str(megahit_dir),
            "--force"
        ]
        print(f"🚀 开始 MEGAHIT：{sample_name}")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise RuntimeError(f"❌ MEGAHIT 失败: {result.stderr.decode()}")
        print(f"✅ 完成 MEGAHIT：{sample_name}")
    else:
        print(f"⏭️ 跳过 MEGAHIT：{sample_name} 已完成")

    print(f"🔍 sample_out: {sample_out}")
    print(f"🔍 megahit_dir: {megahit_dir}")
    print(f"🔍 sembin_dir: {sembin_dir}")

    # 📦 分箱
    run_ss_sembin(final_contig, sembin_dir,reads["read1"],reads["read2"])

    # 📊 评估
    run_metaquast(final_contig, eval_dir)

    checkm2_tsv = eval_dir / "checkm2_report.tsv"
    run_checkm2(sembin_dir / "bins", checkm2_tsv)

    # 📈 特征输出
    save_feature_summary(
        sample_name=sample_name,
        method="megahit",
        combo_type="short_short",
        metaquast_dir=eval_dir,
        checkm2_tsv=checkm2_tsv,
        output_path=sample_out / "features.json"
    )