autowatch = 1;
outlets = 2;

function bang() {
    var patchPath = this.patcher.filepath || "";
    var root = patchPath.replace(/\/patchers\/[^\/]+$/, "");
    if (root === patchPath) {
        root = patchPath.replace(/\/[^\/]+$/, "");
    }
    var idlePath = root + "/media/local/ferrari_sf90_idle_residual.wav";
    var highPath = root + "/media/local/ferrari_sf90_high_residual.wav";
    var fallbackPath = root + "/media/reference_texture_fallback.wav";
    var idle = new File(idlePath, "read");
    var high = new File(highPath, "read");
    var idleExists = idle.isopen;
    var highExists = high.isopen;
    if (idleExists) idle.close();
    if (highExists) high.close();
    outlet(0, "replace", idleExists ? idlePath : fallbackPath);
    outlet(1, "replace", highExists ? highPath : fallbackPath);
}
