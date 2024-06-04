const regionSelector = document.getElementById('region-selector');
const mapImage = document.getElementById('map-image');

regionSelector.addEventListener('change', function() {
  const selectedImage = this.value;
  const newImageUrl = "{{ url_for('static', filename='images/') }}" + selectedImage;

  mapImage.src = newImageUrl;
  mapImage.alt = selectedImage.replace('.jpg', '').replace('-', ' ') + " Regional Map"; // Add descriptive alt text
}); 
