# nlp2hillm

Natural language → `dsl2hillm` command line (no side effects unless `--apply`).

## CLI

```bash
nlp2hillm "read temperature from serial"
nlp2hillm "connect modbus device" --apply
nlp2hillm "capture image from camera" --apply
```

## Python

```python
from nlp2hillm.to_dsl import to_dsl

line = to_dsl("read temperature from serial")
# → READ DEVICE serial-temp REGISTER temperature
```

Mapped keywords: `read`, `write`, `connect`, `capture`, `camera`, `modbus`, `serial`, …

**See also:** [examples/control-layer/nlp-to-dsl.sh](../../examples/control-layer/nlp-to-dsl.sh)
