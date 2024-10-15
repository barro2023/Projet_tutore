from flask import render_template, redirect, url_for, request
from app import app, db, login_manager
from app.models import User
from flask_login import login_user, logout_user, login_required


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        user = User.query.filter_by(username=username, password=password, email=email).first()
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    return render_template('search.html')

from app.models import Listing
@app.route('/search_result', methods=['GET'])
@login_required
def search_result():
    type = request.args.get('type')
    price = request.args.get('price')
    location = request.args.get('location')
    
    query = Listing.query

    if type and type.strip():
        query = query.filter(Listing.type.ilike(f'%{type.strip()}%'))
    if price:
        try:
            price = int(price)
            query = query.filter(Listing.price <= price)
        except ValueError:
            pass

    if location and location.strip():
        query = query.filter(Listing.location.ilike(f'%{location.strip()}%'))
    
    print(f"Critères de recherche - Type: {type}, Prix: {price}, Localisation: {location}")
    listings = query.all()
    print(f"Listings trouvés : {listings}")
    return render_template('search_result.html', listings=listings)

@app.route('/annonces')
@login_required
def annonces():
    listings = Listing.query.order_by(Listing.id.desc()).all()
    return render_template('annonces.html', annonces=listings)


@app.route('/annonce/<int:id>')
@login_required
def view_annonce(id):
    # Récupérer l'annonce avec l'ID spécifié
    annonce = Listing.query.get_or_404(id)

    if annonce:
        if annonce.description == None:
            annonce.description = 'Description indisponible'
        return render_template('view_annonce.html', annonce=annonce)
    else:
        return "Annonce non trouvée", 404
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from flask import request, redirect, url_for
from app.models import db, User, SearchPreferences

@app.route('/set_preferences', methods=['POST'])
def set_preferences():
    user_id = request.form['user_id']
    user = User.query.get(user_id)
    if user:
        # Supposons que les préférences sont envoyées dans un formulaire
        new_preferences = SearchPreferences(
            type=request.form['type'],
            price=request.form['price'],
            location=request.form['location'],
            user=user
        )
        db.session.add(new_preferences)
        db.session.commit()
        return redirect(url_for('profile', user_id=user_id))
    return "User not found", 404



import plotly.express as px
import plotly.io as pio
from real_estate_scraper.real_estate_scraper.pipelines import get_db
import pandas as pd
from flask import render_template
from plotly.subplots import make_subplots


@app.route('/visualisation')
def visualisation():
    try:
        db = get_db()
        cur = db.cursor()

        query = """
        SELECT location, AVG(price::float) AS avg_price
        FROM listing
        GROUP BY location
        """
        
        cur.execute(query)
        tendances = cur.fetchall()

        # Créer un DataFrame à partir des résultats
        df = pd.DataFrame(tendances, columns=['Location', 'AvgPrice'])

        # Créer un sous-graphique avec 1 ligne et 3 colonnes
        fig = make_subplots(rows=1, cols=3, subplot_titles=('Bar Chart', 'Histogramme', 'Carte Thermique'))

        # Créer le bar chart
        fig_bar = px.bar(df, x='Location', y='AvgPrice', labels={'Location': 'Région', 'AvgPrice': 'Prix moyen'})
        fig.add_trace(fig_bar['data'][0], row=1, col=1)

        # Créer l'histogramme
        fig_histogram = px.histogram(df, x='Location', y='AvgPrice', labels={'Location': 'Région', 'AvgPrice': 'Prix moyen'})
        fig.add_trace(fig_histogram['data'][0], row=1, col=2)

        # Créer la carte thermique
        fig_heatmap = px.density_heatmap(df, x='Location', y='AvgPrice', labels={'Location': 'Région', 'AvgPrice': 'Prix moyen'})
        fig.add_trace(fig_heatmap['data'][0], row=1, col=3)

        # Mettre à jour la mise en page du graphique
        fig.update_layout(height=600, width=1800, title_text='Comparaison des prix par région')

        # Générer le HTML pour le graphique
        graph_html = pio.to_html(fig, full_html=False)

    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        graph_html = None

    finally:
        # Fermer le curseur et la connexion
        if cur:
            cur.close()
        if db:
            db.close()

    return render_template('visualisation.html', graph_html=graph_html)
