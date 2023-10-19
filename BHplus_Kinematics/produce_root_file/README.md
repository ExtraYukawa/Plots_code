# Produce ROOT file
This section is mainly focus on producing slim root file. The input directory is kept in `../../pyhon/common.py`.  
```
python runcondor.py [args]
```
The arguments are:\\
1. `--outdir`: Target stored directory. It can be in `\eos`.
2. `--era`: Target era. Default is `all`, which runs all four eras
3. `--region`: List of regions
4. `--channels`: List of channels
5. `--Labels`: Target label/group of `variables`
6. `--Black_list`: Banned label/group of `variables`
7. `--POIs`: List of `variables` that will perform nuisance varition.
8. `--JobFlavour`: condor JobFlavour
9. `--universe`: condor universe
10. `--blocksize`: Events processed in each condor job` 
11. `--test`: Do not trigger condor submission
12. `--check`: Check all files are produced successfully and merged them.
<a/>
After running `runcondor.py`, the code will produce `check.sh`, which is cheat sheet to do the checking and merging. Feel free to modify the `JobFlavour` in it etc. (TODO: it is normal to have failed job and need to resubmit again, need to fix it)
```
sh check.sh
``` 

 
