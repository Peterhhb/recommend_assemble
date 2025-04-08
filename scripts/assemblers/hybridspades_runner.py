import os
import subprocess


def run_hybridspades(input_fasta, output_dir):
    """
    运行 HybridSPAdes 进行混合组装
    """
    os.makedirs(output_dir, exist_ok=True)

    command = [
        'hybridspades',
        '--pe1', input_fasta,  # 混合组装时的输入
        '--out-dir', output_dir
    ]
    subprocess.run(command, check=True)
    print(f"HybridSPAdes assembly completed for {input_fasta}")
