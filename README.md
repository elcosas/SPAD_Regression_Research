# SPAD Regression Research
This repository contains various tests and jupyter notebook experimentations with various
regression algorithms, mainly non-parametic, in order to better model the response curves of
SPAD sensors from both EWH and EDH datasets

## Motivation
The use of equi-depth histograms (EDH) to model photon arrival times in SPAD sensors for single-photon 3D cameras has greatly improved the accuracy of identifying the precise depth value of an object in a scene. Additionally, EDH also allow for much smaller binning requirements in order to accurately model depth levels, thus decreasing the amount of data needed to process each pixel in the image. Despite this, there are still issues with solely using EDH data to estimate depth and saturation, mainly the limited amount of actual depth levels that can be extracted from smaller-bin-sized datasets. The use of non-parametic regresssion equations as proposed both here and the writeup hope to remedy this by allowing for estimation of photon counts at any point in the camera's capture time. This not only allows for obtaining more information about the object captured by each pixel (such as reflectivity of the object and other sources of ambient light), but also allows for more potential depth levels for even smaller sized equi-depth bins. 

## Installation
The project can be installed using git via:
```bash
    git clone https://github.com/elcosas/SPAD_Regression_Research.git
```
All libraries required for installation can be installed through pip using `requirements.txt`
(**TODO:** add minimal required requirements.txt)
```bash
    pip install -r requirements.txt
```
## Usage (Notebooks)
First, once inside the project folder, use `cd notebooks` to change to the notebooks directory. The notebooks contain the various expermentations done with the sample data provided as well as 
different parametic and non-parametic regression methods tested with the sample data. the notebooks themselves can be viewed by running `jupyter lab` and then opening `localhost:8888/lab/` in your
prefered browser

## Usage (Graph Tests)
The tests for the main three potential regression algorithms (GP, LOWESS, & KDE, as highlighted in
the writeup) have been split into 2 folders for EDHs and EWHs, use `cd {hist_type}_tests` to move 
to the directory of your choosing\
Each directory contains a file named `hist_test_run.py` which takes 3 arguments and can be used via the following syntax:
```bash
    python3 hist_test_run.py {test_type} {regression_method} {data_set_#}
```
Where:\
`test_type`: which test to run, either "single", "multi", or "all"\
`regression_method`: the method to use, either "gaussian", "lowess", or "kde"\
`data_set_#`: the data set to use, only accounted for with the single test but still required (default data set ranges from 0-29)\
(**TODO:** provide example outputs)

## Write-up installation
**TODO**

## Attributions and License
**TODO**
