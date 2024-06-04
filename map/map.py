from flask import Flask, render_template, url_for, request, Blueprint
from app import login_required
# Written by: Zheng (c2041164)
map_bp = Blueprint('map', __name__, template_folder='templates')


@map_bp.route('/map')
@login_required
def index():
    # Get the base URL for the images stored in the images directory
    image_base_url = url_for('static', filename='images/')

    # Get the region parameter from the request's query string, default to 'ALC map.jpg'
    selected_region = request.args.get('region', 'ALC map.jpg')

    # Render the 'map.html' template and pass the base URL and selected region to the template
    return render_template('map/map.html', image_base_url=image_base_url, selected_region=selected_region)

