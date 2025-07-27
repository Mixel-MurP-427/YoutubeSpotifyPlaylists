#you can edit the values in this dictionary to configure your desired features.
config_settings = {
    "initial wait time": 1, #time (in seconds) to wait before starting the scan, to allow the page to load
    "iteration pause time": 0.25, #time (in seconds) to wait between each scan iteration, so it doesn't loop too fast
    "scan iterations": 5, #number of times to loop scanner
    "auto-save each iteration": False #if true then will write to playlist.json after each iteration. If false then read_Spotlist will return the playlist as a dictionary and the user can save it however they want.
}

assert config_settings["initial wait time"] >= 0, "Initial wait time cannot be negative."
assert config_settings["iteration pause time"] >= 0, "Iteration pause time cannot be negative."
assert config_settings["scan iterations"] > 0, "Scan iterations must be a positive integer."
assert config_settings["auto-save each iteration"] in {True, False}, "Auto-save each iteration must be a boolean."