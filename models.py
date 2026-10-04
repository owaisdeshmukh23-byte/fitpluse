from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    fitness_goal = db.Column(db.String(60), default='Build Muscle')
    fitness_level = db.Column(db.String(30), default='Intermediate')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    favorites = db.relationship('Favorite', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set user password securely."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify user password against hashed password."""
        return check_password_hash(self.password_hash, password)

    def is_favorite(self, workout_id):
        """Check if a workout is in the user's favorites list."""
        return self.favorites.filter_by(workout_id=workout_id).first() is not None

    def __repr__(self):
        return f"<User {self.username}>"


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(140), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(30), nullable=False)  # Beginner, Intermediate, Advanced
    duration_minutes = db.Column(db.Integer, nullable=False)
    target_muscle = db.Column(db.String(60), nullable=False)  # Full Body, Chest & Triceps, Legs, Back, Core, HIIT
    calories_burned = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(400), nullable=False)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    favorites = db.relationship('Favorite', backref='workout', lazy='dynamic', cascade='all, delete-orphan')
    routine_exercises = db.relationship('WorkoutExercise', backref='workout', lazy='joined', cascade='all, delete-orphan', order_by='WorkoutExercise.order')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'difficulty': self.difficulty,
            'duration_minutes': self.duration_minutes,
            'target_muscle': self.target_muscle,
            'calories_burned': self.calories_burned,
            'image_url': self.image_url,
            'featured': self.featured
        }

    def __repr__(self):
        return f"<Workout {self.title}>"


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    target_muscle = db.Column(db.String(60), nullable=False)  # Chest, Back, Legs, Shoulders, Arms, Core
    equipment = db.Column(db.String(60), nullable=False)      # Dumbbells, Barbell, Bodyweight, Cable, Machine
    difficulty = db.Column(db.String(30), nullable=False)     # Beginner, Intermediate, Advanced
    description = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)         # Step-by-step instructions
    form_tips = db.Column(db.Text, nullable=True)             # Tips for form
    image_url = db.Column(db.String(400), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'target_muscle': self.target_muscle,
            'equipment': self.equipment,
            'difficulty': self.difficulty,
            'description': self.description,
            'instructions': self.instructions,
            'form_tips': self.form_tips,
            'image_url': self.image_url
        }

    def __repr__(self):
        return f"<Exercise {self.name}>"


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id', ondelete='CASCADE'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id', ondelete='CASCADE'), nullable=False)
    order = db.Column(db.Integer, default=1)
    sets = db.Column(db.Integer, default=3)
    reps = db.Column(db.String(40), default='10-12')
    rest_seconds = db.Column(db.Integer, default=60)

    # Relationships
    exercise = db.relationship('Exercise', lazy='joined')

    def __repr__(self):
        return f"<WorkoutExercise Workout:{self.workout_id} Exercise:{self.exercise_id}>"


class Nutrition(db.Model):
    __tablename__ = 'nutrition_recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    slug = db.Column(db.String(160), unique=True, nullable=False, index=True)
    category = db.Column(db.String(60), nullable=False)  # High Protein, Post-Workout, Pre-Workout, Fat Loss, Plant-Based
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Float, nullable=False)        # in grams
    carbs = db.Column(db.Float, nullable=False)          # in grams
    fats = db.Column(db.Float, nullable=False)           # in grams
    prep_time = db.Column(db.Integer, nullable=False)    # in minutes
    ingredients = db.Column(db.Text, nullable=False)     # Pipe '|' or newline separated list
    instructions = db.Column(db.Text, nullable=False)    # Step-by-step
    tips = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(400), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_ingredients_list(self):
        """Return ingredients as a clean list."""
        if '|' in self.ingredients:
            return [i.strip() for i in self.ingredients.split('|') if i.strip()]
        return [i.strip() for i in self.ingredients.split('\n') if i.strip()]

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'category': self.category,
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fats': self.fats,
            'prep_time': self.prep_time,
            'ingredients': self.get_ingredients_list(),
            'instructions': self.instructions,
            'image_url': self.image_url
        }

    def __repr__(self):
        return f"<Nutrition {self.title}>"


class BlogPost(db.Model):
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    slug = db.Column(db.String(180), unique=True, nullable=False, index=True)
    excerpt = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(80), default='FitPulse Coach')
    read_time = db.Column(db.Integer, default=4)
    category = db.Column(db.String(60), default='Fitness Tips')
    image_url = db.Column(db.String(400), nullable=False)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<BlogPost {self.title}>"


class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'workout_id', name='uq_user_workout_favorite'),
    )

    def __repr__(self):
        return f"<Favorite User:{self.user_id} Workout:{self.workout_id}>"
