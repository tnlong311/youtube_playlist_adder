// Scrape all video IDs from the current playlist page
let videoIds = [];
document.querySelectorAll("a#video-title").forEach(a => {
    let url = new URL(a.href);
    if (url.searchParams.get("v")) {
        videoIds.push(url.searchParams.get("v"));
    }
});
console.log("Video IDs:", videoIds);
console.log("Total:", videoIds.length);

// Copy as JSON (for Python script)
copy(JSON.stringify(videoIds));
