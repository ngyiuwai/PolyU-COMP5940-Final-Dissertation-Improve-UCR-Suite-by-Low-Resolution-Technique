## Dissertation Topic: Improve UCR Suite by Lower Resolution Techniques

*Please see here for previous work for dynamics time warping (DTW): https://github.com/ngyiuwai/PolyU-COMP5940-Final-Dissertation-Improve-UCR-Suite-by-Low-Resolution-Technique*

*In this final dissertation, I focus on accelerating Euclidean distance only. It is because the lower bound of DTW (i.e. LB_Keogh) is a lower bound of Euclidean distance.*

This is an algorithm to accelerate non-segmented sequential search for time series data with Euclidean distance as distance function. The state-of-art method is UCR Suite: https://www.cs.ucr.edu/~eamonn/UCRsuite.html.

You may integrate this algorithm with UCR Suite, because LB_Keogh in UCR Sutie is a lower bound of Euclidean distance.

- See **Presentation Slides** for explanation of the algorithm.
- See **Demo Slides** for visualization of the algorithm.
- See **Dissertation Extract** for a short summary.

The Python scripts in source code folder is a demonstration of this algorithm. **Readme.txt** inside the folder is a guideline for using this program. Library Matplotlib is needed if you wish to visualize the code. No external library is needed if you just want to find k-nearest neighbours.*

I included some documentation in Python scripts. Hope this can help you to understand the algorithm.

*Please note that the original diseertation is submited to The Hong Kong Polytechnic University in June 2020. You may found it in PolyU Library soon.*