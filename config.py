config_settings = {
    "autoscroll": False, #if false, then the user may need to scroll manually to ensure all songs are loaded
    "initial wait time": 1, #time to wait before starting the scan, to allow the page to load
    "iteration pause time": 0.25, #time to wait between each scan iteration, so it doesn't loop too fast
    "scan iterations": 5, #number of times to loop scanner
    "auto-save each iteration": True #if true then will write to playlist.json after each iteration. If false then read_Spotlist will return the playlist as a dictionary and the user can save it however they want.
}

assert type(config_settings["autoscroll"]) == bool, "Autoscroll must be a boolean."
assert config_settings["initial wait time"] >= 0, "Initial wait time cannot be negative."
assert config_settings["iteration pause time"] >= 0, "Iteration pause time cannot be negative."
assert config_settings["scan iterations"] > 0, "Scan iterations must be a positive integer."
assert config_settings["auto-save each iteration"] == True, "Auto-save each iteration must be a boolean."