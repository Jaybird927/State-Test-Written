document.addEventListener('DOMContentLoaded', () => {
    const substitutionGrid = document.getElementById('substitution-grid');
    const encodedMessage = document.getElementById('encoded-message');
    const decodedMessage = document.getElementById('decoded-message');
    
    // Create substitution inputs for A-Z
    for (let i = 65; i <= 90; i++) {
        const letter = String.fromCharCode(i);
        const inputContainer = document.createElement('div');
        inputContainer.className = 'substitution-input';
        
        const label = document.createElement('label');
        label.textContent = letter;
        
        const input = document.createElement('input');
        input.type = 'text';
        input.maxLength = 1;
        input.dataset.original = letter;
        
        // Add event listener to handle input
        input.addEventListener('input', (e) => {
            e.target.value = e.target.value.toUpperCase();
            updateDecodedMessage();
        });
        
        inputContainer.appendChild(label);
        inputContainer.appendChild(input);
        substitutionGrid.appendChild(inputContainer);
    }
    
    // Add event listener to encoded message
    encodedMessage.addEventListener('input', updateDecodedMessage);
    
    function updateDecodedMessage() {
        const message = encodedMessage.value;
        const substitutionMap = new Map();
        
        // Build substitution map
        document.querySelectorAll('.substitution-input input').forEach(input => {
            const originalLetter = input.dataset.original;
            const substitution = input.value;
            if (substitution) {
                substitutionMap.set(originalLetter, substitution);
            }
        });
        
        // Apply substitutions
        let decoded = '';
        for (let char of message) {
            const upperChar = char.toUpperCase();
            if (substitutionMap.has(upperChar)) {
                // Preserve case
                decoded += char === upperChar ? 
                    substitutionMap.get(upperChar) : 
                    substitutionMap.get(upperChar).toLowerCase();
            } else {
                decoded += char;
            }
        }
        
        decodedMessage.value = decoded;
    }
}); 