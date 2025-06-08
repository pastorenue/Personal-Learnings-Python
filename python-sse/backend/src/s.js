eventSource.onerror = function() {
    terminal.textContent += '\n[Connection lost. Reconnecting...]\n';
    terminal.scrollTop = terminal.scrollHeight;
};