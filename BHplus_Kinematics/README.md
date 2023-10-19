# Kinematic Plot Tool
This tool is made for plotting distribution and skim the root files in general purpose. The main input is controled by the `json` files in `../data` and main functions are defined in the `h` files in `../script`. Since it utilize the novel function in RDataFrame, it **requires ROOT v6.26** and thus **do not run cmsenv** , otherwise it will conflict with each other. \\
## Input - sample
The sample information should be keep in `../data/sample_ERA.json`. It contains following information:
1. **xsec**:  cross section for MC samples.
2. **Label**: Indicate whether this sample is MC or data or data drivien, background or signal.
3. **Category**: The group/process this sample belongs to.
## Input - cut
The region definition is kept in `../data/cut.json`. It supports multiple regions and channels definition. It follows the structure below:
- Region name
  - channel\_cut
    - Channel name
      - cut name: Channel cut definition
  - general\_cut
    - cut name: cut definition
## Input - variable
The variable definition is kept in `../data/variable.json`. **All the new variables and variables used to vary nuisance (even it is already defined in NanoAOD)** should be in this file. Note that the variables are defined following the order in this file, so **order matters**. It contains following information:
1. **Def**: Definition of this variable. If it is defined, just type "Defined".
2. **Labels**: Labels of this variable. In later stage, we can utilize it to control which group of variables to use. Please note that if this variable is **MC only**, please type "MC".
3. **Save**: This is highly related to Labels, it means when certain group is called, the variable will be saved in the skim root file.
## Input - histogram
The registered histograms are kept in `../data/histogram.json`. Note that `nbin` is defined the plotting `nbin`. When generating the histogram, we actually use 600 times `nbin` in order to provide flexibility for future rebin purpose. It contains following information:
1. **Title**
2. **xlow**
3. **xhigh**
4. **nbin**
5. **Labels**: Same function as `Labels` in variable part.
## Input - nuisance
The nuisance information is stored in `../data/nuisance.json`. It follows the structure below:
- Name of varition
  - Nominal: List of variables that change
  - Def: RVec of variated varialbe definition 
  - Label: affect which type of data [MC/data\_driven]
