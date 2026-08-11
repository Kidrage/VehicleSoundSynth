autowatch = 1;
outlets = 1;

function bang() {
    var patchPath = this.patcher.filepath || "";
    var root = patchPath.replace(/\/patchers\/[^\/]+$/, "");
    if (root === patchPath) {
        root = patchPath.replace(/\/[^\/]+$/, "");
    }
    var localPath = root + "/media/local/ferrari_sf90_residual.wav";
    var fallbackPath = root + "/media/reference_texture_fallback.wav";
    var candidate = new File(localPath, "read");
    if (candidate.isopen) {
        candidate.close();
        outlet(0, "replace", localPath);
    } else {
        outlet(0, "replace", fallbackPath);
    }
}
