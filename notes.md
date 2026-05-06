## slicing rows

Set threshold to 500 and gap to 5: over-slicing (slicing rows that belonged to one vocab entry)

Increased gap to 10: Slicing wrong, some entries were split and became a part of another entry (D1 test). Tested on A1 and found that it does not split because background color (light gray), making a "gap" value = ~10000, but setting threshold to 10000 will cause under-slicing of images iwth white background

Added dynamic threshold by selecting the lower 10th percentile of horizontal projection to be the threshold. However, 10th percentile was still slightly low and was not enough to slice A1.

Adjusted threshold percentile to 15, decreased gap to 5, passed for A1, but fails D1 because of too little gap. However, looking closely at D1, it seems to be a hard edge case because the gap between lines is not consistent.

Tested C1 (green-colored background), needed to adjust threshold to 60 percentile to work.
