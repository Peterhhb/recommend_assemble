import json
import statistics
import subprocess


def run_ss_sembin(contig_path, output_dir, read1, read2):
    bins_dir = output_dir / "bins"
    if bins_dir.exists():
        print("⏭️ SEMBIN 已完成，跳过")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "SemiBin2",
        "bin",
        "-i", str(contig_path),
        "--data", f"{read1},{read2}",
        "--model", "global",
        "-o", str(output_dir),
    ]
    print(f"🚀 开始 SEMBIN2：{contig_path}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print(result.stderr.decode())
        raise RuntimeError(f"❌ SEMBIN2 运行失败")
    print("✅ SEMBIN 完成")


def run_metaquast(contig_path, output_dir):
    if (output_dir / "report.tsv").exists():
        print("⏭️ MetaQUAST 已完成，跳过")
        return
    subprocess.run(["quast.py", str(contig_path), "-o", str(output_dir)])
    print("✅ MetaQUAST 完成")

def run_checkm2(bin_folder, output_tsv):
    if output_tsv.exists():
        print("⏭️ CheckM2 已完成，跳过")
        return
    subprocess.run(["checkm", "predict", str(bin_folder), "-x", "fa", "-o", str(output_tsv)])
    print("✅ CheckM2 完成")


def save_feature_summary(sample_name, method, combo_type, metaquast_dir, checkm2_tsv, output_path):
    report_path = metaquast_dir / "report.tsv"
    meta_features = {}

    # 简单解析 metaquast 报告
    with open(report_path) as f:
        for line in f:
            if "\t" not in line:
                continue
            key, value = line.strip().split("\t", 1)
            try:
                meta_features[key.strip()] = float(value.strip())
            except:
                meta_features[key.strip()] = value.strip()

    checkm2_data = {}
    with open(checkm2_tsv) as f:
        lines = f.readlines()[1:]  # 跳过标题
        for line in lines:
            cols = line.strip().split("\t")
            completeness = float(cols[1])
            contamination = float(cols[2])
            checkm2_data.setdefault("completeness", []).append(completeness)
            checkm2_data.setdefault("contamination", []).append(contamination)

    checkm2_summary = {
        "completeness_mean": round(statistics.mean(checkm2_data["completeness"]), 2),
        "contamination_mean": round(statistics.mean(checkm2_data["contamination"]), 2),
        "bin_count": len(checkm2_data["completeness"])
    }

    summary = {
        "sample_name": sample_name,
        "method": method,
        "combo_type": combo_type,
        "features": {
            "metaquast": meta_features,
            "checkm2": checkm2_summary
        }
    }

    with open(output_path, "w") as f:
        json.dump(summary, f, indent=4)
    print(f"✅ 特征已写入：{output_path}")
