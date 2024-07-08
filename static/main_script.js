const socket = io.connect('http://localhost:5000/');

socket.on('upload_done', function(data) {
    console.log('Upload done emit recieved');
    document.getElementById('loadingOverlay').style.display = 'none';
    showProgress();
    
});
socket.on('upload_progress', function(data) {
    console.log('Upload progress emit recieved:', data.progress);
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = data.progress + '%';
    progressBar.textContent = Math.round(data.progress) + '%';
});

//Scripts for buttons
function settingsHover() {
    var settingsIcon = document.getElementById("settingsIcon");
    settingsIcon.src = settingsIconHoverUrl;
    settingsIcon.style='cursor:pointer';
}

function settingsDefault(){
    var settingsIcon = document.getElementById("settingsIcon");
    settingsIcon.src = settingsIconUrl;
}

function reset_menu_hide() {
    var alert = document.getElementById("resetPopup");
    alert.style.display = "none";
}

function reset_menu_show() {
    var alert = document.getElementById("resetPopup");
    alert.style.display = "flex";
}


function hideProgress() {
    var progressInfo = document.getElementById("progressInfo");
    var progressBar = document.getElementById("progressBar");
    progressInfo.style.display = "none";
    progressBar.style.display = "none";
}

function showProgress() {
    var progressInfo = document.getElementById("progressInfo");
    var progressBar = document.getElementById("progressBar");
    progressInfo.style.display = "block";
    progressBar.style.display = "block";
}

function showDownload() {
    var downloadInfo = document.getElementById("downloadInfo");
    downloadInfo.style.display = "flex";
}

function hideDownload() {
    var downloadInfo = document.getElementById("downloadInfo");
    downloadInfo.style.display = "none";
}

function resetApp() {
    var folderInput = document.getElementById("fileInput");
    folderInput.value = "";
    var thresholdInput = document.getElementById("thresholdInput");
    thresholdInput.value = "127";
    hideDownload();
    reset_menu_hide();
    hideProgress();
}

function reset() {
    location.reload();
}

function toggleDropdown() {
    var dropdownMenu = document.querySelector(".dropdown-menu");
    dropdownMenu.classList.toggle("show");
}

function downloadVids() {
    
}

document.addEventListener("click", function(event) {
    var dropdownMenu = document.querySelector(".dropdown-menu");
    if (!event.target.closest(".settings")) {
        dropdownMenu.classList.remove("show");
    }
});

// MAIN EVENT LISTENERS
document.addEventListener('DOMContentLoaded', function() {
    var uploadForm = document.getElementById('uploadForm');
    
    uploadForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        document.getElementById('loadingOverlay').style.display = 'block';

        var fileInput = document.getElementById('fileInput');
        var files = fileInput.files;

        if (!files) {
            alert('No folder selected');
            return;
        }

        var formData = new FormData(uploadForm);
        
        
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Files processed successfully:', data);
            document.getElementById('loadingOverlay').style.display = 'none';
            showDownload();
        })
        .catch(error => {
            console.error('Error uploading files:', error);
        });

    });
});

