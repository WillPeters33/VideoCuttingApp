
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

function error_menu_hide() {
    var alert = document.getElementById("errorInfo");
    alert.style.display = "none";
}

function error_menu_show() {
    var alert = document.getElementById("errorInfo");
    alert.style.display = "flex";
}

function hideProgress() {
    var progressInfo = document.getElementById("progressInfo");
    var progressArea = document.getElementById("progressArea");
    var progressBar = document.getElementById("progressBar");
    progressInfo.style.display = "none";
    progressBar.style.display = "none";
    progressArea.style.display = "none";
    //progressArea.style.display = "none";
}

function showProgress() {
    var progressInfo = document.getElementById("progressInfo");
    var progressArea = document.getElementById("progressArea");
    var progressBar = document.getElementById("progressBar");
    progressBar.style.width = '3%';
    progressArea.style.display = "flex";
    progressArea.style['margin-top'] = "20px";
    progressInfo.style.display = "block";
    progressBar.style.display = "block";
    progressBar['aria-valuenow'] = '3';
   
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
    error_menu_hide();
}

function reset() {
    document.getElementById('loadingOverlay').style.display = 'block';
    document.getElementById('processingText').innerText = 'Refreshing Please Wait...';
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
        document.getElementById('processingText').innerText = 'Processing...';
        error_menu_hide();
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
        .catch(error => {
            console.error('Error uploading files:', error);
        })
        .then(data => {
            if (data.error) {
                document.getElementById('loadingOverlay').style.display = 'none';
                error_menu_show();
                console.error('Error uploading files:', data.error);
                return;
            }
            console.log('Files uploaded successfully:', data);
            document.getElementById('loadingOverlay').style.display = 'none';
            hideDownload();
            showProgress();
            updateProgress();

        });
        async function updateProgress() {
            let progressValue = 0;
        
            while (progressValue < 100) {
                try {
                    const response = await fetch('/process', {
                        method: 'POST'
                    });
                    const data = await response.json();
                    progressValue = data.progress;
                    console.log(progressValue)
                    const progressBar = document.getElementById('progressBar');
                    progressBar['aria-valuenow'] = progressValue;
                    progressBar.style.width = progressValue + '%';
                } catch (error) {
                    console.error('Error processing files:', error);
                    break; // Optionally break the loop if there's an error
                }
            }
            
            hideProgress();
            showDownload();
        }
    });
});



