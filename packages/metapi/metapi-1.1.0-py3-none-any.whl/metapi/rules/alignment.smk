rule alignment_scaftigs_index:
    input:
        scaftigs = os.path.join(
            config["output"]["assembly"],
            "scaftigs/{sample}.{assembler}.out/{sample}.{assembler}.scaftigs.fa.gz")
    output:
        temp(expand(
            os.path.join(
                config["output"]["alignment"],
                "index/{{sample}}.{{assembler}}.out/{{sample}}.{{assembler}}.scaftigs.fa.gz.{suffix}"),
            suffix=BWA_INDEX_SUFFIX))
    log:
        os.path.join(
            config["output"]["alignment"],
            "logs/index/{sample}.{assembler}.scaftigs.index.log")
    params:
        bwa = "bwa-mem2" if config["params"]["alignment"]["algorithms"] == "mem2" else "bwa",
        output_prefix = os.path.join(
            config["output"]["alignment"],
            "index/{sample}.{assembler}.out/{sample}.{assembler}.scaftigs.fa.gz")
    shell:
        '''
        {params.bwa} index {input.scaftigs} -p {params.output_prefix} 2> {log}
        '''


rule alignment_reads_scaftigs:
    input:
        reads = assembly_input_with_short_reads,
        index = expand(os.path.join(
            config["output"]["alignment"],
            "index/{{sample}}.{{assembler}}.out/{{sample}}.{{assembler}}.scaftigs.fa.gz.{suffix}"),
            suffix=BWA_INDEX_SUFFIX)
    output:
        flagstat = os.path.join(
            config["output"]["alignment"],
            "report/flagstat/{sample}.{assembler}.align2scaftigs.flagstat"),
        bam = temp(os.path.join(
            config["output"]["alignment"],
            "bam/{sample}.{assembler}.out/{sample}.{assembler}.align2scaftigs.sorted.bam")),
        bai = temp(os.path.join(
            config["output"]["alignment"],
            "bam/{sample}.{assembler}.out/{sample}.{assembler}.align2scaftigs.sorted.bam.bai"))
    log:
        os.path.join(config["output"]["alignment"],
                     "logs/alignment/{sample}.{assembler}.align.reads2scaftigs.log")
    benchmark:
        os.path.join(config["output"]["alignment"],
                     "benchmark/alignment/{sample}.{assembler}.align.reads2scaftigs.benchmark.txt")
    params:
        bwa = "bwa-mem2" if config["params"]["alignment"]["algorithms"] == "mem2" else "bwa",
        index_prefix = os.path.join(
            config["output"]["alignment"],
            "index/{sample}.{assembler}.out/{sample}.{assembler}.scaftigs.fa.gz")
    threads:
        config["params"]["alignment"]["threads"]
    shell:
        '''
        rm -rf {output.bam}*

        {params.bwa} mem \
        -t {threads} \
        {params.index_prefix} \
        {input.reads} 2> {log} |
        tee >(samtools flagstat \
              -@{threads} - \
              > {output.flagstat}) | \
        samtools sort \
        -@{threads} \
        -T {output.bam} \
        -O BAM -o {output.bam} -

        samtools index -@{threads} {output.bam} {output.bai} 2>> {log}
        '''


if config["params"]["alignment"]["cal_base_depth"]:
    rule alignment_base_depth:
        input:
            os.path.join(
                config["output"]["alignment"],
                "bam/{sample}.{assembler}.out/{sample}.{assembler}.align2scaftigs.sorted.bam")
        output:
            os.path.join(
                config["output"]["alignment"],
                "depth/{sample}.{assembler}.out/{sample}.{assembler}.align2scaftigs.depth.gz")
        shell:
            '''
            samtools depth {input} | gzip -c > {output}
            '''


    rule alignment_base_depth_all:
        input:
            expand(os.path.join(
                config["output"]["alignment"],
                "depth/{sample}.{assembler}.out/{sample}.{assembler}.align2scaftigs.depth.gz"),
                   assembler=ASSEMBLERS,
                   sample=SAMPLES.index.unique())

else:
    rule alignment_base_depth_all:
        input:


rule alignment_report:
    input:
        expand(
            os.path.join(
                config["output"]["alignment"],
                "report/flagstat/{sample}.{{assembler}}.align2scaftigs.flagstat"),
            sample=SAMPLES.index.unique())
    output:
        os.path.join(config["output"]["alignment"],
                     "report/alignment_flagstat_{assembler}.tsv")
    run:
        input_list = [str(i) for i in input]
        output_str = str(output)
        metapi.flagstats_summary(input_list, output_str, 2)


rule alignment_report_all:
    input:
        expand(
            os.path.join(
                config["output"]["alignment"],
                "report/alignment_flagstat_{assembler}.tsv"),
            assembler=ASSEMBLERS)


rule single_alignment_all:
    input:
        rules.alignment_base_depth_all.input,
        rules.alignment_report_all.input,

        rules.single_assembly_all.input