document.addEventListener('DOMContentLoaded', () => {
    const titleElement = document.getElementById('title');
    const userInput = document.getElementById('userInput');
    const output = document.getElementById('output');
    const previousSearches = document.getElementById('previousSearches');
    const convertBtn = document.getElementById('convertBtn');
    const navLinks = document.querySelectorAll('.nav-link');
    const inputLabel = document.getElementById('inputLabel');
    const outputLabel = document.getElementById('outputLabel');

    let currentTab = 'emojify';

    const tabInfo = {
        emojify: {
            title: "Emoji 🎨 Converter 💻",
            input: 'Enter text to emojify:',
            output: 'Emojified text:'
        },
        linkedin: {
            title: "LinkedIn Post Generator",
            input: 'Enter text to convert to LinkedIn post:',
            output: 'LinkedIn post:'
        },
        prompt: {
            title: "AI Prompt Generator",
            input: 'Enter text to convert to AI prompt:',
            output: 'AI prompt:'
        }
    };

    function typeTitle(title) {
        titleElement.innerHTML = '';
        let index = 0;

        function addChar() {
            if (index < title.length) {
                titleElement.innerHTML += title.charAt(index);
                index++;
                setTimeout(addChar, 100);
            }
        }

        addChar();
    }

    function updateLabels() {
        inputLabel.textContent = tabInfo[currentTab].input;
        outputLabel.textContent = tabInfo[currentTab].output;
        typeTitle(tabInfo[currentTab].title);
    }

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            currentTab = link.dataset.tab;
            userInput.value = '';
            output.textContent = '';
            updateLabels();
            fetchPreviousSearches();
        });
    });

    convertBtn.addEventListener('click', () => {
        const text = userInput.value;
        fetch(`/convert/${currentTab}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text }),
        })
        .then(response => response.json())
        .then(data => {
            output.textContent = data.result;
            fetchPreviousSearches();
        });
    });

    function fetchPreviousSearches() {
        fetch(`/previous_searches/${currentTab}`)
        .then(response => response.json())
        .then(data => {
            previousSearches.innerHTML = '';
            data.searches.forEach(search => {
                const searchElement = document.createElement('a');
                searchElement.className = 'list-group-item list-group-item-action previous-search';
                searchElement.innerHTML = `<strong>Input:</strong> ${search.input}<br><strong>Output:</strong> ${search.output}`;
                previousSearches.appendChild(searchElement);
            });
        });
    }

    updateLabels();
    fetchPreviousSearches();
});