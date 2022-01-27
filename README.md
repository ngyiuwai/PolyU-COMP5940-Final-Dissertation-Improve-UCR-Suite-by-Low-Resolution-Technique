## Dissertation Topic: Improve UCR Suite by Lower Resolution Techniques

*Please see here for previous work for dynamics time warping (DTW): https://github.com/ngyiuwai/PolyU-COMP5940-Dissertation-Improve-UCR-Suite*

*In the final dissertation, I focus on accelerating computation of Euclidean distance only. It is because the lower bound of DTW (i.e. LB_Keogh) is a lower bound of Euclidean distance.*

This is an algorithm to accelerate non-segmented sequential search for time series data with Euclidean distance as distance function. The state-of-art method is UCR Suite: https://www.cs.ucr.edu/~eamonn/UCRsuite.html.

You may integrate this algorithm with UCR Suite, because LB_Keogh in UCR Sutie is a lower bound of Euclidean distance.

- See **Presentation Slides.pdf** for explanation of this algorithm.
- See **Demo Slidesp.pdf** for visualization of this algorithm.
- See **Dissertation Extract.pdf** for a short summary.

The Python scripts in source code folder is a demonstration of this algorithm. **Readme.txt** inside the folder is a guideline for using this program. Library Matplotlib is needed if you wish to visualize the code. No external library is needed if you just want to find k-nearest neighbours.

I included some documentation in Python scripts. Hope this can help you understanding this algorithm.

*Please note that the original diseertation is submited to The Hong Kong Polytechnic University in June 2020. You may find it in PolyU Library soon.*
