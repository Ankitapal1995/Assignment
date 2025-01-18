Thank you for giving me the opportunity to solve such an amazing and thought-provoking assignment. Here are the scripts for reproducing the results. For Task 1, all the scripts are provided in the `TASK1` folder, and for Task 2, the scripts are provided separately in the `TASK2` folder.

For using the scripts inside `TASK1` and `TASK2` <br>

Please activate the Conda environment using the `assignment.yml` file provided:

```bash
conda env create -f assignment.yml
```

## TASK 1:

### 1. Calculating Median Coverage and Coefficient of Variation (CV)

#### i) File Preparation for cfDNA and Islet Tissue
```bash
{ head -n 1 PupilBioTest_PMP_revA.csv; grep "cfDNA" PupilBioTest_PMP_revA.csv; } > cfDNA_data.csv
{ head -n 1 PupilBioTest_PMP_revA.csv; grep "Islet" PupilBioTest_PMP_revA.csv; } > Islet_data.csv
```

#### ii) Calculating Median Coverage and CV
```bash
python coverage_statistics.py cfDNA_data.csv
python coverage_statistics.py Islet_data.csv
```

### 2. Machine Learning for Differentiating cfDNA and Islet Tissue Using PMPs as Features

#### i) Data Preparation
```bash
python data_reorganize.py PupilBioTest_PMP_revA.csv
```
This will create an output file: `reorganize_data.csv`.

#### ii) Machine Learning Prediction
```bash
python machine_learning_new_matrix.py reorganize_data.csv 2
```
Here, `2` indicates 2-fold cross-validation. Users can specify `2`, `5`, or `10` for 2-fold, 5-fold, or 10-fold cross-validation as per their choice.

### 3. Scoring PMPs for Discriminating Between Two Tissues

#### i) XGBoost Feature Scoring
```bash
python machine_learning_xgboost_feature_scoring.py reorganize_data.csv
```

#### ii) SHAP Feature Scoring
```bash
python machine_learning_shap_feature_scoring.py reorganize_data.csv
```

#### iii) Chi-Square Test
```bash
python machine_learning_feature_scoring_using_chisquare_test.py reorganize_data.csv
```

### 4. Machine Learning for Differentiating cfDNA and Islets Using Single CpG as Features
```bash
python machine_learning_for_data_with_single_cpg.py PupilBioTest_PMP_revA.csv
```

### 5. Calculating Mean Variant Read Fraction and Median Read Depth
```bash
python mean_variant_read_fraction.py cfDNA_data.csv
python mean_variant_read_fraction.py Islet_data.csv
```

## TASK 2

### Requirement
Download `GATK` before proceeding.

### Steps

#### i) Quality Check, Alignment, and BAM File Preparation
Run the following command:
```bash
sh pipeline_for_bam_file.sh --ref <reference.gb> --R1 <reads_1.fastq.gz> --R2 <reads_2.fastq.gz> --prefix <prefix> --output <output_dir>
```

#### ii) Running Mutect2 and Varscan2
Use this command to perform mutation calling:
```bash
python mutect2_varscan2_mutation_calling.py reference.fasta tumor.bam normal.bam normal_sample_prefix
```

#### iii) Running In-House Pipeline
Execute the in-house somatic mutation calling pipeline with the following commands:
```bash
python pipeline_for_somatic_mut_calling.py reference.fasta normal.bam tumor.bam
python identify_cancer_somatic_mutation_cp.py tumor.vcf normal.vcf
```

#### iv) Background Estimation of GATK Mutect2-Generated Normal Sample VCF File
Use the following command for background estimation:
```bash
python background_estimation_new.py normal_sample_vcf_file total_bases output_prefix
```

To calculate the total bases, run:
```bash
grep -v '^>' GCF_000001405.40_GRCh38.p14_genomic.fna | tr -d '\n' | wc -c
```
