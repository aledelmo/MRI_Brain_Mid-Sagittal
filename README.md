# Symmetry Plane using Inertia Ellipsoid and Optimization

Mid-Sagittal plane computation from brain MRI images.

![symmetry](https://i.imgur.com/d4SZLgD.jpg)

Algorithm for the automatic determination of the symmetry plane in volumetric medical images. Initial plane 
position is estimated using the ellipsoid of inertia. This position is then optimized using the
Sequential Least Squares Programming (SLSQP) algorithm. The optimization metric is the L2 distance between the
original image and its reflection in respect to the symmetry plane.

If you use this work please cite:
```bibtex
@INPROCEEDINGS{1044783,  
author={A. V. {Tuzikov} and O. {Colliot} and I. {Bloch}}, 
booktitle={Object recognition supported by user interaction for service robots},
title={Brain symmetry plane computation in MR images using inertia axes and optimization},
year={2002},
volume={1},
number={},
pages={516-519 vol.1},
doi={10.1109/ICPR.2002.1044783}}
```

To run a test:
```shell
python mid_sagittal.py test_dataset/100307.nii.gz
```
## Contacts

For any inquiries please contact: 
[Alessandro Delmonte](https://aledelmo.github.io) @ [alessandro.delmonte@institutimagine.org](mailto:alessandro.delmonte@institutimagine.org)

## License

This project is licensed under the [Apache License 2.0](LICENSE) - see the [LICENSE](LICENSE) file for
details