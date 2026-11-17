# Hail Alerts

A lightweight Python script that alerts to observed instances of hail at a set of airports.

METAR is a routine aviation weather report issued on a regular schedule. SPECI is an unscheduled special report issued between routine METARs when weather conditions change significantly or cross safety thresholds. Both are available from the [Aviation Weather Center](https://aviationweather.gov/).

Both weather reports indicate the presence of hail, abbreviated `GR` (from the French "grêle").

| **Code** | **Meaning** |
| --- | --- |
| - | light intensity |
| + | heavy intensity |
| `VC` | in the vicinity |
| `TS` | thunderstorm |
| `SH` | shower(s) |
| `GR` | hail |
| `GS` | small hail and/or snow pellets |

For example, `+TSGR` means "heavy thunderstorm with hail" has been observed at the airport.

Thus, the [hail python script](hail.py) contains the following line:
```
pattern = r"(?<!\S)(?:\+|-|VC)?(?:TS|SH)?(?:GR|GS)(?!\S)"

```

which is a regex (regular expression) that matches standalone codes in the METAR or SPECI reports that consist of:
1. An optional prefix: `+`, `-`, or `VC`
2. An optional intermediate component: `TS` or `SH`
3. A required ending: `GR` or `GS`

If such a pattern is matched in the METAR or SPECI reports from a given airport, then hail was reported there in the past 24 hours!

## Example output

```
[OK] No hail reported at KATL.
[ALERT] Hail reported at KDEN!
  KDEN 171753Z 25012KT 2SM +TSGR BKN025CB 18/14 A2990
[OK] No hail reported at KDFW.
[OK] No hail reported at KORD.
[OK] No hail reported at KJFK.
[OK] No hail reported at KLAX.
```

# To-Do

- Add cloud integrations (AWS/Azure/GCP)
    - Email notifications if hail is detected
