// ==UserScript==
// @require utils.js
// ==/UserScript==
function unityReady() {
    // Integrate with Unity!
    console.log(Unity);
    var total = 10;
    Unity.Launcher.setLauncherCount(total);
}
var Unity = external.getUnityObject(1.0);
Unity.init({
    name: "Django BMF",
    homepage: 'http://127.0.0.1:8000/bmf/',
    onInit: unityReady
});
