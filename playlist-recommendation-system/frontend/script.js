const protocol = window.location.protocol;
const backendUrl = `${protocol}//${window.location.hostname}:30746`;
let availableSongs = [];
let playlist = [];

function fetchSongs() {
    fetch(`${backendUrl}/api/songs`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        availableSongs = data.songs;
        displaySongs(availableSongs);
    })
    .catch(error => console.error('Error:', error));
}

function displaySongs(songs) {
    const availableSongsList = document.getElementById('availableSongs');
    availableSongsList.innerHTML = '';
    songs.forEach(song => {
        const li = document.createElement('li');
        li.textContent = song;
        li.classList.add('cursor-pointer');
        li.addEventListener('click', () => addToPlaylist(song));
        availableSongsList.appendChild(li);
    });
}

function addToPlaylist(song) {
    if (!playlist.includes(song)) {
        playlist.push(song);
        updatePlaylist();
    }
}

function removeFromPlaylist(song) {
    playlist = playlist.filter(item => item !== song);
    updatePlaylist();
}

function updatePlaylist() {
    const playlistElement = document.getElementById('playlist');
    playlistElement.innerHTML = '';
    playlist.forEach(song => {
        const li = document.createElement('li');
        li.textContent = song;
        li.classList.add('cursor-pointer');
        li.addEventListener('click', () => removeFromPlaylist(song));
        playlistElement.appendChild(li);
    });
}

document.getElementById('recommendButton').addEventListener('click', () => {
    fetch(`${backendUrl}/api/recommend`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ songs: playlist })
    })
    .then(response => response.json())
    .then(data => {
        model_date = data.model_date;
        document.getElementById('modelDate').innerHTML = `Model last updated on: ${model_date}`;
        if (data.songs.length === 0) {
            const currentTime = new Date().toLocaleTimeString();
            document.getElementById('response').innerHTML = `<p>No recommendations at this time. Current time: ${currentTime}</p>`;
        } else {
            console.log(data);
            const sortedRecommendations = data.songs.sort((a, b) => b.confidence - a.confidence).slice(0, 10);
            const recommendations = sortedRecommendations.map(song => {
            return `<li class="mb-2">
                <span class="font-bold">${song.name}</span>
                <span class="text-sm text-gray-600">(Confidence: ${(song.confidence * 100).toFixed(2)}%)</span>
            </li>`;
            }).join('');
            document.getElementById('response').innerHTML = `<ul class="list-disc list-inside">${recommendations}</ul>`;
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('searchBar').addEventListener('input', (event) => {
    const query = event.target.value.toLowerCase();
    const filteredSongs = availableSongs.filter(song => song.toLowerCase().includes(query));
    displaySongs(filteredSongs);
});

fetchSongs();