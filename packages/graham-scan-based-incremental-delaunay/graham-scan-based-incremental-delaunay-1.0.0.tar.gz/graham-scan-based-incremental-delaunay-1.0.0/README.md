# graham-scan-based-incremental-delaunay

A Delaunay triangulation algorithm visualization that incrementally add points during the process and uses Graham Scan to construct the initial triangulation of the iteration.

## Documentation
[Point.py](https://carlklier.github.io/graham-scan-based-incremental-delaunay/html/point.html)  
[Grahamscandelaunay.py](https://carlklier.github.io/graham-scan-based-incremental-delaunay/html/grahamscandelaunay.html)  
[Visual.py](https://carlklier.github.io/graham-scan-based-incremental-delaunay/html/visual.html)  

## Graham Scan-Based Incremental Delaunay Triangulation Algorithm
Given a list of points:
- Sort the list of points such that:
  - the first point is the leftmost, bottommost point, used as the pivot point
  - the remaining points are sorted by their slope in ascending order relative to the first point
- Construct the base convex hull using first 3 points (pivot point and two points with the lowest slopes)
- Incrementally add the next sorted point:
  - Use Graham Scan to get the convex hull, saving any edges that were made
  - Flip the current triangulation to Delaunay
  - Repeat until done

## Hotkeys
- `LEFT CLICK` with your mouse create point on where you clicked
- Press the `G` key to generate a random point
- Press the `S` key to start the algorithm with your set of points
- Press the `SPACEBAR` to iterate to the next step
- Press the `R` key to reset the algorithm, where you can press `S` again to start with the same set of points
- Press the `C` key to stop the algorithm and clear all the points

## Visualization
After starting the algorithm, a triangle will be drawn using three of the points.
- Points
  - Black points indicate points that are in the triangulation
  - Light Grey points indicate points that have yet to be added to the triangulation
  - Red points indicate the most recently added point, and the points that are involved when a circumcircle is displayed
  - Dark Red points indicate the point that is on the opposite triangle of a quadrilateral when an edge is being checked if it is Locally Delaunay
  - Yellow points indicate the circumcenter of the triangle formed by the Red points
- Edges
  - Grey edges indicate the edges in the triangulation
  - Green edges indicate the edges that are in the queue to be checked if they are Locally Delaunay
  - Blue edges indicate the current edge that is being checked if it is Locally Delaunay
A Yellow circle is drawn when the current edge is an inside edge is being checked if it is Locally Delaunay. This is the circumcircle defined by the triangle formed by the Red points, centered on the Yellow circumcenter. If the Dark Red point is within the Yellow circle, then the current edge will be flipped.

When the algorithm is complete, the background will turn green to indicate completion.

## Static Walkthrough
https://user-images.githubusercontent.com/48186448/116015435-3212b200-a607-11eb-8a45-fde9a8893821.mp4

## Environment and package info
Please make sure you have installed the pyglet and numpy before running the code, Those two package can be installed using pip command
```pip install numpy``` and ```pip install pyglet```

This project has been uploaded to PyPi as a package. You can download the package by the following command:
```python3 -m pip install graham-scan-based-incremental-delaunay```
After install the package, you can start the project by
```python3```
and then ```>>> from grahamscandelaunay import visual```

## Interesting Examples
Simple 10-Gon
![Simple 10-gon](https://raw.githubusercontent.com/carlklier/graham-scan-based-incremental-delaunay/main/img/10gon.PNG)

Pentagon in a Pentagon
![Pentagon in Pentagon](https://raw.githubusercontent.com/carlklier/graham-scan-based-incremental-delaunay/main/img/inscribed.PNG)

Counterclockwise Inward Spiral starting from the left
![Spiral](https://raw.githubusercontent.com/carlklier/graham-scan-based-incremental-delaunay/main/img/spiral1.PNG)

Hyperbolic Curve (Horizontal Gap) - looks like a suspension bridge
![5up5down](https://raw.githubusercontent.com/carlklier/graham-scan-based-incremental-delaunay/main/img/set1.PNG)

Hyperbolic Curve (Vertical Gap) - looks like an hourglass
![5left5right](https://raw.githubusercontent.com/carlklier/graham-scan-based-incremental-delaunay/main/img/set2.PNG)
