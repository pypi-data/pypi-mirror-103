# lhereader
[![PyPI version](https://badge.fury.io/py/lhereader.svg)](https://badge.fury.io/py/lhereader)

A Python module to read LHE files. Originally by [diptaparna](https://github.com/diptaparna/lhereader), significantly rewritten by me. No dependency on ROOT, requires python version >= 3.6.

Usage example:

```python
import numpy as np
from lhereader import LHEReader


reader = LHEReader('path/to/file.lhe')

# Mediator mass in each event
mmed = []
counter = 0
for iev, event in enumerate(reader):
    # Find DM particles
    dm = filter(lambda x: abs(x.pdgid)== 52, event.particles)

    # Sum over all DM four-momenta in the event
    combined_p4 = None
    for p4 in map(lambda x: x.p4(), dm):
        if combined_p4:
            combined_p4 += p4
        else:
            combined_p4 = p4
    mmed.append(combined_p4.mass)

print(f'Mean mediator mass: {np.mean(mmed)}')
print(f'Median mediator mass: {np.median(mmed)}')
```

## Treatment of weights


The parser assumes that each weight XML element has an attribute called `id` that uniquely identifies the weight per event. In practical terms, each entry should look roughly like this:

```
<wgt id='some string'> 123456.7 </wgt>
```

Weights are read in one of two modes: `list` or `dict`, which can be set via the `weight_mode` argument to the `LHEReader` constructor. In the first case, weights are returned as an unlabelled list in the order of appearance. In the second case, weights are returned as a dictionary per event, which the `id` attribute serving as the key, and the weight as the value. 

The weights can easily be filtered using the `weight_regex` argument. Only weights with an `id` matching this regular expression will be returned.

In case no `id` attribute can be found, the `dict` mode, as well as filtering are not supported