import os
import subprocess


def run_opera_ms(input_fasta, output_dir):
    """
    运行 OPERA-MS 进行混合组装
    """
    os.makedirs(output_dir, exist_ok=True)

    command = [
        'opera-ms',
        '--reads', input_fasta,
        '--out-dir', output_dir
    ]
    subprocess.run(command, check=True)
    print(f"OPERA-MS assembly completed for {input_fasta}")
