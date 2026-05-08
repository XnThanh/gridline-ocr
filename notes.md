## Slicing rows

Set threshold to 500 and gap to 5: over-slicing (slicing rows that belonged to one vocab entry). \
_Results in slices/t500-g10-[xx]._

Increased gap to 10: Slicing wrong, some entries were split and became a part of another entry (D1 test). Tested on A1 and found that it does not split because background color (light gray), making a "gap" value = ~10000, but setting threshold to 10000 will cause under-slicing of images with white background. \
_Results in slices/t500-g10-[xx]._

Added dynamic threshold by selecting the lower 10th percentile of horizontal projection to be the threshold. However, 10th percentile was still slightly low and was not enough to slice A1.

Adjusted threshold percentile to 15, decreased gap to 5, passed for A1, but fails D1 because of too little gap. However, looking closely at D1, it seems to be a hard edge case because the gap between lines is not consistent. \
_Results in slices/tdynamic15-g5-[xx]._

Tested C1 (green-colored background), needed to adjust threshold to 60 percentile to work. But 60th percentile caused over-slicing in A1 and D1. It also made slices slightly smaller (some of the words/lines were cut off at top and bottom). \
_Results in slices/tdynamic60-g5-[xx]._

Seems like outliers in signal is causing overfitting to some datasets. Switched to trying to normalize horizontal profile and estimating threshold and gap through normalized signal that cuts off outliers. Does much better, passing A1 and E1. C1 is mostly correct, but has [one slice](slices/normalized-C1/vocab-page-C1_row_16.png) that contained 2 entries. D1 is mostly correct, but had [one entry](slices/normalized-D1/vocab-page-D1_row_15.png) that was sliced in between (but this was expected because the spacing between this and the entry below is closer than the entry above). \
_Results in slices/normalized-[xx]._

Switched to a different boundary detection method where I took the left half of the image, ran horizontal projection profile on it, normalized it, then used the normalized profile to detect entry boundaries. Then, adjusted the boundaries using information from the projection profiles of the right half of the image and the full image. This works a lot better. Passing A1, B1, C1, D1, E1, G1. Failed F1, H1, I1. But F1 and H1 were minor failures. \
_Results in slices/left-half-boundary-detection-[xx]_
