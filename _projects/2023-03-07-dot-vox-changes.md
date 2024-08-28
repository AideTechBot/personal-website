---
layout: post
title: Updating the dot_vox Rust Crate
shortTitle: dot_vox Parser Changes
date: 2023-03-07 12:00 -0500
modified: 2024-08-26 13:33 -0400
---

**Status**: Merged and released in [dot_vox v5.1.1](https://github.com/dust-engine/dot_vox/releases/tag/v5.1.1).

**Context:** The software [MagicaVoxel](https://ephtracy.github.io/) is (according to their website):
> A free lightweight GPU-based voxel art editor and interactive path tracing renderer. 


It uses it's own `.vox` file type to store it's voxel positions and color, animations, scene information, camera positions, etc.


There is a Rust crate called [dot_vox](https://github.com/dust-engine/dot_vox). It implements a parser for reading and writing to these types of files.

### Pull Requests
While I was implementing something completely unrelated, I stumbled upon a bug in the aforementioned module. According to the [specification](https://github.com/ephtracy/voxel-model/blob/master/MagicaVoxel-file-format-vox.txt#L50), it was reading/writing files wrong by expecting a deprecated type of chunk. 


To get myself unblocked, I put up [a fix](https://github.com/dust-engine/dot_vox/pull/38).


After the fix, my original project required me to implement a voxel terrain generator that would output a `.vox` file. 
<!-- <aside>I presume hard limit for the size of models is for optimizing ray intersection calculations for the ray-tracing, but I didn't really look into it.</aside> -->
The model abstraction stored within the file was limiting because it only allowed models with smaller dimensions than 256x256x50. This would not work for me because I wanted terrain that was thousands of voxels wide.

This led me to implement the parts of the specification (in a [second PR](https://github.com/dust-engine/dot_vox/pull/39)) that allowed me to save multiple models within the same file.


In conclusion, I'd like to thank [Zhixing Zhang](https://github.com/Neo-Zhixing) for his timely feedback on my contributions. With his help, I was able to merge the code and return to my original project. 