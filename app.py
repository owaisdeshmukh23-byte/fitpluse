import os
import functools
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, jsonify, Response, abort
)
from config import Config
from models import db, User, Workout, Exercise, WorkoutExercise, Nutrition, BlogPost, Favorite
from seed import get_seed_data, seed_database

app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
db.init_app(app)

# Global status tracking for DB connectivity
db_status = {
    "connected": False,
    "error_message": None
}

# Cached fallback seed data in memory for preview when PostgreSQL is connecting
FALLBACK_DATA = get_seed_data()

def check_and_init_db():
    """Verify PostgreSQL connectivity and auto-create tables and seed data."""
    with app.app_context():
        try:
            # Test database connection
            with db.engine.connect() as conn:
                db_status["connected"] = True
                db_status["error_message"] = None
                print("[PulseFit] PostgreSQL database connection successful!")
                
            # Create tables and auto-seed if empty
            db.create_all()
            if not Workout.query.first():
                print("[PulseFit] Tables created. Running initial seed...")
                seed_database(app)
        except Exception as e:
            db_status["connected"] = False
            db_status["error_message"] = str(e)
            print(f"[PulseFit Notice] PostgreSQL is not yet connected: {e}")
            print("[PulseFit Notice] PulseFit will run with sample data in display mode until PostgreSQL is reached.")

# Run initial DB check on startup
check_and_init_db()


# -------------------------------------------------------------
# Context Processor & Auth Decorator
# -------------------------------------------------------------

def login_required(view):
    """Decorator to require login on protected routes."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return view(**kwargs)
    return wrapped_view

@app.context_processor
def inject_globals():
    """Inject current_user, db_status and helper values to all templates."""
    current_user = None
    user_favorites_ids = set()
    
    if 'user_id' in session and db_status["connected"]:
        try:
            current_user = db.session.get(User, session['user_id'])
            if current_user:
                favs = Favorite.query.filter_by(user_id=current_user.id).all()
                user_favorites_ids = {f.workout_id for f in favs}
        except Exception:
            pass
    elif 'user_id' in session and not db_status["connected"]:
        # Fallback dummy user for preview
        current_user = {
            'id': 1,
            'username': session.get('username', 'alexfit'),
            'full_name': 'Alex Rivera',
            'email': 'alex@pulsefit.com',
            'fitness_goal': 'Build Lean Muscle & Strength',
            'fitness_level': 'Intermediate'
        }
        user_favorites_ids = {1}

    return {
        'current_user': current_user,
        'user_favorites_ids': user_favorites_ids,
        'db_status': db_status,
        'active_path': request.path
    }


# -------------------------------------------------------------
# Public & Catalog Routes
# -------------------------------------------------------------

@app.route('/')
def home():
    """Home landing page with hero, statistics, featured routines, BMI preview, and blogs."""
    featured_workouts = []
    recent_blogs = []
    total_workouts = 6
    total_exercises = 10

    if db_status["connected"]:
        try:
            featured_workouts = Workout.query.filter_by(featured=True).limit(3).all()
            if not featured_workouts:
                featured_workouts = Workout.query.limit(3).all()
            recent_blogs = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(3).all()
            total_workouts = Workout.query.count()
            total_exercises = Exercise.query.count()
        except Exception:
            pass

    if not featured_workouts:
        featured_workouts = [w for w in FALLBACK_DATA['workouts'] if w.get('featured')][:3]
        recent_blogs = FALLBACK_DATA['blogs'][:3]

    return render_template(
        'index.html',
        featured_workouts=featured_workouts,
        recent_blogs=recent_blogs,
        total_workouts=total_workouts,
        total_exercises=total_exercises
    )


@app.route('/workouts')
def workouts():
    """Filterable workout routine catalog."""
    difficulty = request.args.get('difficulty', '').strip()
    muscle = request.args.get('muscle', '').strip()
    search = request.args.get('search', '').strip()

    workouts_list = []

    if db_status["connected"]:
        try:
            query = Workout.query
            if difficulty and difficulty.lower() != 'all':
                query = query.filter(Workout.difficulty.ilike(f"%{difficulty}%"))
            if muscle and muscle.lower() != 'all':
                query = query.filter(Workout.target_muscle.ilike(f"%{muscle}%"))
            if search:
                query = query.filter(
                    db.or_(
                        Workout.title.ilike(f"%{search}%"),
                        Workout.description.ilike(f"%{search}%"),
                        Workout.target_muscle.ilike(f"%{search}%")
                    )
                )
            workouts_list = query.all()
        except Exception:
            workouts_list = []

    if not workouts_list and not db_status["connected"]:
        # Fallback filter
        items = FALLBACK_DATA['workouts']
        if difficulty and difficulty.lower() != 'all':
            items = [w for w in items if difficulty.lower() in w['difficulty'].lower()]
        if muscle and muscle.lower() != 'all':
            items = [w for w in items if muscle.lower() in w['target_muscle'].lower()]
        if search:
            items = [w for w in items if search.lower() in w['title'].lower() or search.lower() in w['description'].lower()]
        workouts_list = items

    return render_template(
        'workouts.html',
        workouts=workouts_list,
        selected_difficulty=difficulty,
        selected_muscle=muscle,
        search_query=search
    )


@app.route('/workouts/<slug>')
def workout_detail(slug):
    """Detailed view for a single workout and its exercises."""
    workout = None

    if db_status["connected"]:
        try:
            workout = Workout.query.filter_by(slug=slug).first()
        except Exception:
            workout = None

    if not workout:
        # Check fallback
        match = next((w for w in FALLBACK_DATA['workouts'] if w['slug'] == slug), None)
        if match:
            # Map exercises for fallback display
            exercise_dict = {ex['slug']: ex for ex in FALLBACK_DATA['exercises']}
            routine_list = []
            for r in match.get('routine', []):
                ex_info = exercise_dict.get(r['exercise_slug'])
                if ex_info:
                    routine_list.append({
                        'exercise': ex_info,
                        'order': r['order'],
                        'sets': r['sets'],
                        'reps': r['reps'],
                        'rest_seconds': r['rest_seconds']
                    })
            workout = dict(match)
            workout['routine_exercises'] = routine_list
        else:
            abort(404)

    return render_template('workout_detail.html', workout=workout)


@app.route('/exercises')
def exercises():
    """Exercise library with filter by target muscle and equipment."""
    muscle = request.args.get('muscle', '').strip()
    equipment = request.args.get('equipment', '').strip()
    search = request.args.get('search', '').strip()

    exercises_list = []

    if db_status["connected"]:
        try:
            query = Exercise.query
            if muscle and muscle.lower() != 'all':
                query = query.filter(Exercise.target_muscle.ilike(f"%{muscle}%"))
            if equipment and equipment.lower() != 'all':
                query = query.filter(Exercise.equipment.ilike(f"%{equipment}%"))
            if search:
                query = query.filter(
                    db.or_(
                        Exercise.name.ilike(f"%{search}%"),
                        Exercise.description.ilike(f"%{search}%"),
                        Exercise.target_muscle.ilike(f"%{search}%")
                    )
                )
            exercises_list = query.all()
        except Exception:
            exercises_list = []

    if not exercises_list and not db_status["connected"]:
        items = FALLBACK_DATA['exercises']
        if muscle and muscle.lower() != 'all':
            items = [e for e in items if muscle.lower() in e['target_muscle'].lower()]
        if equipment and equipment.lower() != 'all':
            items = [e for e in items if equipment.lower() in e['equipment'].lower()]
        if search:
            items = [e for e in items if search.lower() in e['name'].lower() or search.lower() in e['description'].lower()]
        exercises_list = items

    return render_template(
        'exercises.html',
        exercises=exercises_list,
        selected_muscle=muscle,
        selected_equipment=equipment,
        search_query=search
    )


@app.route('/exercises/<slug>')
def exercise_detail(slug):
    """Detailed view for a specific exercise."""
    exercise = None
    if db_status["connected"]:
        try:
            exercise = Exercise.query.filter_by(slug=slug).first()
        except Exception:
            exercise = None

    if not exercise:
        exercise = next((e for e in FALLBACK_DATA['exercises'] if e['slug'] == slug), None)
        if not exercise:
            abort(404)

    return render_template('exercise_detail.html', exercise=exercise)


@app.route('/nutrition')
def nutrition():
    """Nutrition guides, meal prep recipes and macro breakdowns."""
    category = request.args.get('category', '').strip()
    search = request.args.get('search', '').strip()

    recipes_list = []

    if db_status["connected"]:
        try:
            query = Nutrition.query
            if category and category.lower() != 'all':
                query = query.filter(Nutrition.category.ilike(f"%{category}%"))
            if search:
                query = query.filter(
                    db.or_(
                        Nutrition.title.ilike(f"%{search}%"),
                        Nutrition.ingredients.ilike(f"%{search}%")
                    )
                )
            recipes_list = query.all()
        except Exception:
            recipes_list = []

    if not recipes_list and not db_status["connected"]:
        items = FALLBACK_DATA['nutrition']
        if category and category.lower() != 'all':
            items = [n for n in items if category.lower() in n['category'].lower()]
        if search:
            items = [n for n in items if search.lower() in n['title'].lower() or search.lower() in n['ingredients'].lower()]
        recipes_list = items

    return render_template(
        'nutrition.html',
        recipes=recipes_list,
        selected_category=category,
        search_query=search
    )


@app.route('/nutrition/<slug>')
def nutrition_detail(slug):
    """Detailed view for a specific nutrition recipe."""
    recipe = None
    if db_status["connected"]:
        try:
            recipe = Nutrition.query.filter_by(slug=slug).first()
        except Exception:
            recipe = None

    if not recipe:
        match = next((n for n in FALLBACK_DATA['nutrition'] if n['slug'] == slug), None)
        if match:
            recipe = dict(match)
            recipe['get_ingredients_list'] = lambda: [i.strip() for i in match['ingredients'].split('|')]
        else:
            abort(404)

    return render_template('nutrition_detail.html', recipe=recipe)


@app.route('/bmi-calculator')
def bmi_calculator():
    """Interactive visual BMI calculator with health range and calorie advice."""
    return render_template('bmi.html')


@app.route('/blog')
def blog():
    """Fitness blog list with categories and search."""
    category = request.args.get('category', '').strip()
    search = request.args.get('search', '').strip()

    posts_list = []

    if db_status["connected"]:
        try:
            query = BlogPost.query.order_by(BlogPost.created_at.desc())
            if category and category.lower() != 'all':
                query = query.filter(BlogPost.category.ilike(f"%{category}%"))
            if search:
                query = query.filter(
                    db.or_(
                        BlogPost.title.ilike(f"%{search}%"),
                        BlogPost.content.ilike(f"%{search}%"),
                        BlogPost.excerpt.ilike(f"%{search}%")
                    )
                )
            posts_list = query.all()
        except Exception:
            posts_list = []

    if not posts_list and not db_status["connected"]:
        items = FALLBACK_DATA['blogs']
        if category and category.lower() != 'all':
            items = [b for b in items if category.lower() in b['category'].lower()]
        if search:
            items = [b for b in items if search.lower() in b['title'].lower() or search.lower() in b['excerpt'].lower()]
        posts_list = items

    return render_template(
        'blog.html',
        posts=posts_list,
        selected_category=category,
        search_query=search
    )


@app.route('/blog/<slug>')
def blog_detail(slug):
    """Detailed view for an individual blog post."""
    post = None
    related_posts = []

    if db_status["connected"]:
        try:
            post = BlogPost.query.filter_by(slug=slug).first()
            if post:
                related_posts = BlogPost.query.filter(BlogPost.id != post.id).limit(2).all()
        except Exception:
            post = None

    if not post:
        post = next((b for b in FALLBACK_DATA['blogs'] if b['slug'] == slug), None)
        if post:
            related_posts = [b for b in FALLBACK_DATA['blogs'] if b['slug'] != slug][:2]
        else:
            abort(404)

    return render_template('blog_detail.html', post=post, related_posts=related_posts)


@app.route('/about')
def about():
    """About PulseFit page for college project viva."""
    return render_template('about.html')


# -------------------------------------------------------------
# User Authentication & Dashboard
# -------------------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        full_name = request.form.get('full_name', '').strip()
        fitness_goal = request.form.get('fitness_goal', 'Build Muscle')
        fitness_level = request.form.get('fitness_level', 'Intermediate')

        if not username or not email or not password:
            flash('All required fields must be completed.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')

        if not db_status["connected"]:
            # Informative message if DB connection is pending
            flash('PostgreSQL database connection is currently pending. You are signed in as a demo user.', 'info')
            session['user_id'] = 1
            session['username'] = username
            return redirect(url_for('dashboard'))

        try:
            # Check existing user
            existing_user = User.query.filter(
                db.or_(User.username == username, User.email == email)
            ).first()

            if existing_user:
                flash('Username or Email already registered. Please log in.', 'warning')
                return render_template('register.html')

            # Create new user
            new_user = User(
                username=username,
                email=email,
                full_name=full_name or username.capitalize(),
                fitness_goal=fitness_goal,
                fitness_level=fitness_level
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            # Set user session
            session['user_id'] = new_user.id
            session['username'] = new_user.username
            flash(f'Welcome to PulseFit, {new_user.username}! Your account has been created.', 'success')
            return redirect(url_for('dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred during registration: {e}', 'error')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        login_input = request.form.get('username_or_email', '').strip()
        password = request.form.get('password', '')

        if not login_input or not password:
            flash('Please provide both username/email and password.', 'error')
            return render_template('login.html')

        if not db_status["connected"]:
            # Demo login for testing when DB is pending
            flash('Logged in under demo mode while PostgreSQL establishes connection.', 'info')
            session['user_id'] = 1
            session['username'] = login_input or 'alexfit'
            return redirect(url_for('dashboard'))

        try:
            # Query user by username or email
            user = User.query.filter(
                db.or_(User.username == login_input, User.email == login_input.lower())
            ).first()

            if user and user.check_password(password):
                session['user_id'] = user.id
                session['username'] = user.username
                flash(f'Welcome back, {user.username}!', 'success')
                
                next_url = request.args.get('next')
                if next_url and next_url.startswith('/'):
                    return redirect(next_url)
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username/email or password.', 'error')
        except Exception as e:
            flash(f'Database connection error: {e}', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Log out the current user."""
    session.clear()
    flash('You have been successfully logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard displaying saved favorite workouts and fitness profile."""
    favorite_workouts = []
    
    if db_status["connected"]:
        try:
            user_id = session.get('user_id')
            favs = Favorite.query.filter_by(user_id=user_id).all()
            workout_ids = [f.workout_id for f in favs]
            if workout_ids:
                favorite_workouts = Workout.query.filter(Workout.id.in_(workout_ids)).all()
        except Exception:
            pass

    if not favorite_workouts and not db_status["connected"]:
        # Fallback favorite for preview
        favorite_workouts = [FALLBACK_DATA['workouts'][0]]

    return render_template(
        'dashboard.html',
        favorite_workouts=favorite_workouts
    )


@app.route('/api/favorites/toggle/<int:workout_id>', methods=['POST'])
def toggle_favorite(workout_id):
    """AJAX endpoint to toggle favorite status for a workout."""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in to save workouts'}), 401

    if not db_status["connected"]:
        return jsonify({
            'success': True,
            'is_favorite': True,
            'message': 'Saved (Preview Mode)'
        })

    try:
        user_id = session['user_id']
        existing = Favorite.query.filter_by(user_id=user_id, workout_id=workout_id).first()

        if existing:
            db.session.delete(existing)
            db.session.commit()
            return jsonify({
                'success': True,
                'is_favorite': False,
                'message': 'Workout removed from favorites'
            })
        else:
            new_fav = Favorite(user_id=user_id, workout_id=workout_id)
            db.session.add(new_fav)
            db.session.commit()
            return jsonify({
                'success': True,
                'is_favorite': True,
                'message': 'Workout saved to favorites!'
            })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


# -------------------------------------------------------------
# SEO, Sitemap & Robots.txt
# -------------------------------------------------------------

@app.route('/sitemap.xml')
def sitemap():
    """Generate dynamic XML sitemap for SEO crawlers."""
    host = request.host_url.rstrip('/')
    urls = [
        {'loc': f"{host}/", 'changefreq': 'daily', 'priority': '1.0'},
        {'loc': f"{host}/workouts", 'changefreq': 'daily', 'priority': '0.9'},
        {'loc': f"{host}/exercises", 'changefreq': 'weekly', 'priority': '0.8'},
        {'loc': f"{host}/nutrition", 'changefreq': 'weekly', 'priority': '0.8'},
        {'loc': f"{host}/bmi-calculator", 'changefreq': 'monthly', 'priority': '0.8'},
        {'loc': f"{host}/blog", 'changefreq': 'daily', 'priority': '0.7'},
        {'loc': f"{host}/about", 'changefreq': 'monthly', 'priority': '0.5'},
    ]

    # Add dynamic workout and blog URLs
    if db_status["connected"]:
        try:
            for w in Workout.query.all():
                urls.append({'loc': f"{host}/workouts/{w.slug}", 'changefreq': 'weekly', 'priority': '0.8'})
            for b in BlogPost.query.all():
                urls.append({'loc': f"{host}/blog/{b.slug}", 'changefreq': 'weekly', 'priority': '0.7'})
            for e in Exercise.query.all():
                urls.append({'loc': f"{host}/exercises/{e.slug}", 'changefreq': 'monthly', 'priority': '0.6'})
            for n in Nutrition.query.all():
                urls.append({'loc': f"{host}/nutrition/{n.slug}", 'changefreq': 'monthly', 'priority': '0.6'})
        except Exception:
            pass
    else:
        for w in FALLBACK_DATA['workouts']:
            urls.append({'loc': f"{host}/workouts/{w['slug']}", 'changefreq': 'weekly', 'priority': '0.8'})
        for b in FALLBACK_DATA['blogs']:
            urls.append({'loc': f"{host}/blog/{b['slug']}", 'changefreq': 'weekly', 'priority': '0.7'})

    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for u in urls:
        xml_lines.append('  <url>')
        xml_lines.append(f"    <loc>{u['loc']}</loc>")
        xml_lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        xml_lines.append(f"    <priority>{u['priority']}</priority>")
        xml_lines.append('  </url>')
    xml_lines.append('</urlset>')

    return Response('\n'.join(xml_lines), mimetype='application/xml')


@app.route('/robots.txt')
def robots():
    """Generate robots.txt file with crawler directives."""
    content = f"""User-agent: *
Allow: /
Disallow: /dashboard
Disallow: /api/

Sitemap: {request.host_url.rstrip('/')}/sitemap.xml
"""
    return Response(content, mimetype='text/plain')


# -------------------------------------------------------------
# Error Handling
# -------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('404.html', error_message="Internal Server Error"), 500


if __name__ == '__main__':
    # Local dev server runner
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
