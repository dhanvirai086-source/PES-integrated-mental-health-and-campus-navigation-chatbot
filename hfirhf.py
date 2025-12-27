<!DOCTYPE html>
<html>
<head>
<title>System Terminal</title>
<style>
    body { background: black; color: #00ff00; font-family: monospace; padding: 20px; }
    #output { white-space: pre-wrap; }
    .cursor { animation: blink 1s infinite; }
    @keyframes blink { 50% { opacity: 0; } }
</style>
</head>
<body>
<div id="output"></div><span class="cursor">█</span>

<script>
const lines = [
    "Initializing system…",
    "Loading modules…",
    "Bypassing firewall…",
    "Accessing secure server…",
    "Decrypting data packets…",
    "Establishing backdoor…",
    "Running diagnostic scan…",
    ">> Process complete. (Simulation only)"
];

let i = 0;
function typeLine() {
    if (i < lines.length) {
        document.getElementById("output").innerText += lines[i] + "\n";
        i++;
        setTimeout(typeLine, 700);
    }
}
typeLine();
</script>
</body>
</html>
