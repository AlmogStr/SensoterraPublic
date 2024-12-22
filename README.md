# SensoterraPublic
My Python scripts developed for Sensoterra user's

# api_transfer_script
Use the Sensoterra Rest-API (https://monitor.sensoterra.com/api/v3/#/probe/put_probe__probeId__transfer). Moves sensors between sub-accounts of the same Reseller. Requires Sensoterra credentials. Allows to visualize (in a list) the sensors and choose them with a tick-box GUI.

# soil_downlink
Based on Sensoterra's Decoder (https://gitlab.com/sensoterra/public/codec#probe-calibration-downlinks). Creates a LoRaWAN downlink payload based on a csv input file with parameters a, b, c, and sp that describe the soil-type's calibration curve.
