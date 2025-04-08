import os
import subprocess


def run_metaflye(input_fasta, output_dir, use_nextpolish=False):
    """
    运行 MetaFlye 进行组装，并可选地进行 NextPolish 后处理
    """
    os.makedirs(output_dir, exist_ok=True)

    # 运行 MetaFlye 进行长读组装
    command = [
        'metaflye',
        '--pacbio', input_fasta,
        '--out-dir', output_dir
    ]
    subprocess.run(command, check=True)
    print(f"MetaFlye assembly completed for {input_fasta}")

    # 如果需要 NextPolish 后处理
    if use_nextpolish:
        nextpolish_dir = output_dir + "_nextpolish"
        command_nextpolish = [
            'nextpolish', '--pacbio', input_fasta, '--out-dir', nextpolish_dir
        ]
        subprocess.run(command_nextpolish, check=True)
        print(f"NextPolish correction completed for {input_fasta}")

