# Methodology

## Draft Method

The baseline method will create an Adaptation Gap Index from official datasets.

1. Normalize climate-signal indicators within the available Pacific geography set.
2. Normalize observed-stress indicators within the same geography set.
3. Normalize adaptation-capacity proxies so higher capacity reduces the gap.
4. Combine climate signal and observed stress into a pressure score.
5. Compare pressure score against capacity score.
6. Rescale the pressure-minus-capacity difference to a 0-100 adaptation gap score.

## Missingness Policy

Missing values are not imputed for the primary score. If a geography lacks enough data for a pillar, the app should show an insufficient-data state or score caveat.

## Outlook Method

Outlook modeling is optional. If included, it will use transparent time-series trend baselines and scenario assumptions. It will not be described as an operational prediction.
