# graham-scan-based-incremental-delaunay

Graham Scan-Based Incremental Delaunay Triangulation:
- Sort the input points by x-coordinate
- Select the leftmost, bottommost point as the pivot point
- Sort the other points by angle relative to the pivot point their slopes relative to the pivot
- Construct the base convex hull using the pivot point and the first two points sorted by angle
- Incrementally add the next sorted point and use Graham Scan to get the convex hull, saving any edges that were made
- Flip the current triangulation to Delaunay and repeat until done

TODO LIST:
- [x] Implement Halfedge data structure, with addleaf and addedge
  - [x] get two sorting algorithms loglinear time, one for x-coord and one for slope
  - [x] Use a stack to track points on the convex hull
  - [x] Use a queue to track edges that need to be flipped
  - [x] Save all the edges made during the convex hull process
  - [x] Check the queued edges if they are locally Delaunay
  - [x] Flip non-locally Delaunay edges
- [x] Work on visualization
- [ ] Write some tests
  - [ ] Test sorting for setting up the points
  - [ ] Test Convex Hull triangulation
  - [ ] Test Locally Delaunay check
  - [ ] Test edge flipping on a simple case

Due Date: final code and presentation on April 29th

Timeline for progress:
- 4/1
- 4/8
- 4/15
- 4/22
- 4/29 project due along with presentation

## Environment and package info
Please make sure you have installed the pyglet and numpy before running the code, Those two package can be installed using pip command
```pip install numpy``` and ```pip install pyglet```

This project has been uploaded to PyPi as a package. You can download the package by the following command:
```python3 -m pip install grahamscan-delaunay```
After install the package, you can start the project by
```python3```
and then ```>>> import grahamscan_delaunay```
## Visualization
Once you start the program, an empty window will pop up. You can add a point by click inside the window, or randomly generate one by pressing ```G```. 
Once you finish adding points, press ```S``` to start the Delaunay algorithm step-by-step visualization. 
To go to the next step, press the Space Bar. 
To reset to the start of the algorithm, press ```R```. To clear all points, press ```C```.
The red point indicates the most recently added point. 
The blue edge indicates that the edge will be checked if it is Locally Delaunay. 
A black point indicates that the point in in the triangulation while a gray point indicates that it has not yet been added to the triangulation.
When the algorithm is complete, the background will turn green. Press ```R``` or ```C``` to reset the visualization.
