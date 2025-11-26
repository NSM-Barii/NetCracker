# signatures.py
# THIS FILE WILL HOLD MAC INFO FOR FLOCK AND OTHER TYPES OF SIMILAR DEVICES

FLOCK_SIGNATURES = {
    "wifi_ssid_patterns": [
        "flock", 
        "Flock", 
        "FLOCK",
        "FS Ext Battery",
        "Penguin",
        "Pigvision",
    ],

    "mac_prefixes": [
        "58:8E:81","CC:CC:CC","EC:1B:BD","90:35:EA","04:0D:84",
        "F0:82:C0","1C:34:F1","38:5B:44","94:34:69","B4:E3:F9",
        "70:C9:4E","3C:91:80","D8:F3:BC","80:30:49","14:5A:FC",
        "74:4C:A1","08:3A:88","9C:2F:9D","94:08:53","E4:AA:EA",
    ],

    "ble_name_patterns": [
        "FS Ext Battery",
        "Penguin",
        "Flock",
        "Pigvision",
    ],

    "raven_service_uuids": [
        "0000180a-0000-1000-8000-00805f9b34fb",
        "00003100-0000-1000-8000-00805f9b34fb",
        "00003200-0000-1000-8000-00805f9b34fb",
        "00003300-0000-1000-8000-00805f9b34fb",
        "00003400-0000-1000-8000-00805f9b34fb",
        "00003500-0000-1000-8000-00805f9b34fb",
        "00001809-0000-1000-8000-00805f9b34fb",
        "00001819-0000-1000-8000-00805f9b34fb",
    ],
}
