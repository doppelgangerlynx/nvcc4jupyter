## NVCC Plugin for Jupyter notebook


### V3 + V1.revision codes by forker doppelgangerlynx

Includes new support for adding compile arguments (such as -lcublas if you need cuBLAS) for magics ```%%cu``` and ```%%nv_nsight```
##### usage of --compile_custom
> ```%%cu --compile_custom```
- if the cell is run, the cell output will ask for input for compile arguments you would like to add. for my case, I added:
> ```-lcublas```
- nv_nsight is now callable with 
```
%%nv_nsight
# new cell magic made by doppelgangerlynx@github.com
```
- **IMPORTANT**
    - to use nv_nsight, you need to go to v3/v3.py and configure:
> ```cuda_ver = 10.1```
    - But google colab uses CUDA 10.1 anyways, and I made this to run it on there, so if that's our case, no need to do so.
### V2 is available

V2 brings support of multiple source and header files.

##### Usage

- Load Extension
> `%load_ext nvcc_plugin`

- Mark a cell to be treated as cuda cell
> `%%cuda --name example.cu --compile false`
>> NOTE: The cell must contain either code or comments to be run successfully. 
>> It accepts 2 arguments. `-n` | `--name`  - which is the name of either CUDA source or Header
>> The name parameter must have extension `.cu` or `.h`
>> Second argument `-c` | `--compile`; default value is `false`. The argument is a flag to specify
>> if the cell will be compiled and run right away or not. It might be usefull if you're playing in
>> the `main` function

- To compile and run all CUDA files you need to run
```
%%cuda_run
# This line just to bypass an exeption and can contain any text
```

###### **NEW**: nvprof is now callable with 
```
%%nvprof
# new cell magic made by doppelgangerlynx@github.com
```
- Note that since nvidia is considering to transition to NVIDIA Nsight tools, this functionality may become deprecated in the future; hence I place it in the V1. - doppelgangerlynx

