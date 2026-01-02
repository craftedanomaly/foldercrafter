# FolderCrafter Website Deployment

This is the source code for the FolderCrafter landing page.

## 🚀 How to Customize

### 1. Download Link
Open `index.html` and search for `id="download-btn"`.
Replace `href="#"` with the path to your executable (e.g., `href="FolderCrafter.exe"`).

```html
<a href="FolderCrafter.exe" id="download-btn" class="glass-btn primary">
```

### 2. Adding Video & Images to Carousel
The carousel is pre-configured. You just need to replace the placeholders in `index.html`.

**To add a Video:**
Find the "Slide 1" comment and replace the inner div with a `<video>` tag:

```html
<!-- BEFORE -->
<div class="carousel-slide">
    <div class="media-placeholder video">
        <span>▶ Video Demo</span>
    </div>
</div>

<!-- AFTER -->
<div class="carousel-slide">
    <video controls poster="video-thumbnail.jpg" style="width:100%; height:100%; object-fit:cover;">
        <source src="demo-video.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</div>
```

**Carousel Navigation:**
The carousel now includes Left/Right arrows and is Full Width (100%).
The JavaScript handles the sliding logic automatically.

### 3. Support Link
The "Buy Me a Coffee" link is now integrated into the Features grid.
Search for `feature-support` in `index.html` if you need to update the link.

## ☁️ Deployment
Simply upload this entire folder to your web host (e.g., public_html).
Ensure `FolderCrafter.exe` is in the same folder if using a direct local link.
