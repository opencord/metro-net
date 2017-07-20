# metro-net-gui

## Installation

Having a profile deployed is required. To use the GUI, include the following in the profile manifest
being used in `cord/build/platform-install/profile_manifests`.

```
enabled_gui_extensions:
  - name: metro-net-gui
    path: orchestration/metro-net/xos/gui
    extra-files:
        - app/style/style.css
        - mapconstants.js
```

## Features

 - Maps all UserNetworkInterface locations, and displays the status of created ELine connections
 - Allows for the creation of new and modification of exisiting ELine connections using the map
 
## Interface

![Metro-net-gui Screenshot](http://i.imgur.com/f4YxuyV.png)