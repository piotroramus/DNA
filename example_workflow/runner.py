import subprocess
import os.path

scripts = [
    "alignment.sh",
    "SAM_to_BAM_conversion.sh",
    "marking_PCR_duplicates.sh",
    "local_realignment.sh",
    "quality_score_recalibration.sh",
    "produce_raw_SNP_calls.sh",
    "filter_SNPs.sh",
    "conversion_to_annovar.sh"
]


for script in scripts:
    path = "scripts/"+script
    if os.path.exists(path):
        try:
           out = subprocess.check_output(path, shell=True)
        except subprocess.CalledProcessError as subprocess_exception:
            print "error code", subprocess_exception.returncode
            break
    else:
        print "Cannot find", script
        break