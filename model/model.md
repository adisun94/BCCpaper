
![alt text for screen readers](../images/features.png)

List of descriptors to model the target properties. The table lists the set of descriptors u<sub>p</sub> based on alloy/metal properties p in its second column and the corresponding feature parameters in its third column, which include the feature parameters ( p<sub>ij</sub><sup>BCC/B2</sup> and p<sub>ij</sub><sup>FCC/L10</sup>) of the first-nearest-neighbor bond between element i and j and the element properties ( pi ). xi/xj is the mole fraction of element i/j in the alloys.

![alt text for screen readers](../images/TargetVSDesc.png)

Distribution of target properties with few descriptors. The descriptors are listed in the table above.

![](../images/LRusf.png)
![](../images/LASSOusf.png)
![](../images/GBRusf.png)

Linear regression and LASSO models result in poor predictive accuracies.

![alt text for screen readers](../images/RFR.png)

Random Forest Regression was the final model chosen for screening. (d) and (e) Training (d) and testing (e) performances for the RFR model of γ<sub>surf</sub>. (f) and (g) Training (f) and testing (g) performance for the RFR model of γ<sub>usf</sub>. The training sets in (d) and (f) include data from binary and ternary alloys (red dots). The testing sets in (e) and (g) include quaternary alloys (red circles). The vertical black lines in (e) and (g) denote the [15, 85] quantile from the RFR model.
