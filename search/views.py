from flask import Blueprint, render_template, request, redirect, url_for
# Written by: Asare (c2059143)
search_blueprint = Blueprint('search', __name__, template_folder='templates')


@search_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        selected_option = request.form.get('crop')
        # Get the value of the crop selected from the form
        return redirect(url_for('search.search_options', selected_option=selected_option))
        # Redirect to the crop options view function to handle crop selection
    return render_template('search/search.html')


@search_blueprint.route('/search/<selected_option>', methods=["GET", "POST"])
def search_options(selected_option):
    # Based on the crop selected, user is redirected to according crop view function
    if selected_option == "maize":
        return redirect(url_for('search.diseases_maize'))
    elif selected_option == "rice":
        return redirect(url_for('search.diseases_rice'))
    elif selected_option == "wheat":
        return redirect(url_for('search.diseases_wheat'))
    elif selected_option == "sugarcane":
        return redirect(url_for('search.diseases_sugarcane'))
    return redirect(url_for('search.search'))


@search_blueprint.route('/search/maize-diseases', methods=["GET", "POST"])
def diseases_maize():
    if request.method == 'POST':
        disease = request.form.get('disease')
        # Get the value of the selected maize disease
        return redirect(url_for('search.disease_maize', disease=disease))
        # Redirect to the disease view function to handle disease selection
    return render_template('maize/diseases_form.html')


@search_blueprint.route('/search/maize-diseases/<disease>', methods=["GET"])
def disease_maize(disease):
    # Based on the value of selected maize disease according disease template is rendered
    if disease == 'blight':
        return render_template('maize/blight.html')
    elif disease == 'gray-leaf-spot':
        return render_template('maize/gray_leaf.html')
    elif disease == 'common-rust':
        return render_template('maize/common_rust.html')
    elif disease == 'dwarf-mosaic-potyvirus':
        return render_template('maize/dwarf_mosaic.html')
    elif disease == 'downy-mildew':
        return render_template('maize/downy_mildew.html')
    elif disease == 'lethal-necrosis':
        return render_template('maize/lethal_necrosis.html')
    return render_template('maize/diseases_form.html')


@search_blueprint.route('/search/rice-diseases', methods=["GET", "POST"])
def diseases_rice():
    if request.method == 'POST':
        disease = request.form.get('disease')
        # Get value of selected rice disease
        return redirect(url_for('search.disease_rice', disease=disease))
        # Redirect to the disease view function to handle disease selection
    return render_template('rice/diseases_form.html')


@search_blueprint.route('/search/rice-diseases/<disease>', methods=["GET", "POST"])
def disease_rice(disease):
    # Based on value of selected rice disease according disease template is rendered
    if disease == 'blast':
        return render_template('rice/blast.html')
    elif disease == 'leaf-blight':
        return render_template('rice/leaf_blight.html')
    elif disease == 'sheath-blight':
        return render_template('rice/sheath_blight.html')
    elif disease == 'foot-rot':
        return render_template('rice/foot_rot.html')
    elif disease == 'brown-stripe':
        return render_template('rice/brown_stripe.html')
    return render_template('rice/diseases_form.html')


@search_blueprint.route('/search/sugarcane-diseases', methods=["GET", "POST"])
def diseases_sugarcane():
    if request.method == 'POST':
        disease = request.form.get('disease')
        # Get value of selected sugar can diseases
        return redirect(url_for('search.disease_sugarcane', disease=disease))
        # Redirect to the disease view function to handle disease selection
    return render_template('sugarcane/diseases_form.html')


@search_blueprint.route('/search/sugarcane-diseases/<disease>', methods=["GET", "POST"])
def disease_sugarcane(disease):
    # Based on value of selected sugarcane disease according disease template is rendered
    if disease == 'gummosis':
        return render_template('sugarcane/gummosis.html')
    elif disease == 'red-rot':
        return render_template('sugarcane/red_rot.html')
    elif disease == 'wilt':
        return render_template('sugarcane/wilt.html')
    elif disease == 'smut':
        return render_template('sugarcane/smut.html')
    elif disease == 'red-stripe':
        return render_template('sugarcane/red_stripe.html')
    return render_template('sugarcane/sugarcane.html')


@search_blueprint.route('/search/wheat-diseases', methods=["GET", "POST"])
def diseases_wheat():
    if request.method == 'POST':
        disease = request.form.get('disease')
        # Get value of selected wheat disease
        return redirect(url_for('search.disease_wheat', disease=disease))
        # Redirect to the disease view function to handle disease selection
    return render_template('wheat/diseases_form.html')


@search_blueprint.route('/search/wheat-diseases/<disease>', methods=["GET", "POST"])
def disease_wheat(disease):
    # Based on value of selected wheat disease according disease template is rendered
    if disease == 'blight':
        return render_template('wheat/blight.html')
    elif disease == 'rust':
        return render_template('wheat/rust.html')
    elif disease == 'powdery-mildew':
        return render_template('wheat/powdery_mildew.html')
    elif disease == 'barley':
        return render_template('wheat/barley_yellow_dwarf.html')
    elif disease == 'tan-spot':
        return render_template('wheat/tan_spot.html')
    elif disease == 'ergot':
        return render_template('wheat/ergot.html')
    return render_template('wheat/diseases_form.html')
