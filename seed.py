"""
PulseFit Database Seed Script
Populates the PostgreSQL database with rich, realistic fitness data:
- Sample user
- Workouts with different difficulties, target muscles, and durations
- Comprehensive exercise library
- Workout-Exercise routines
- Nutrition recipes & macro breakdowns
- Fitness & wellness blog articles
"""

from models import db, User, Workout, Exercise, WorkoutExercise, Nutrition, BlogPost, Favorite

def get_seed_data():
    """Return dictionary of seed data records."""
    
    users = [
        {
            'username': 'alexfit',
            'email': 'alex@pulsefit.com',
            'password': 'Password123!',
            'full_name': 'Alex Rivera',
            'fitness_goal': 'Build Lean Muscle & Athleticism',
            'fitness_level': 'Intermediate'
        }
    ]

    exercises = [
        {
            'name': 'Barbell Bench Press',
            'slug': 'barbell-bench-press',
            'target_muscle': 'Chest',
            'equipment': 'Barbell',
            'difficulty': 'Intermediate',
            'description': 'The foundational upper-body compound lift targeting the pectoralis major, anterior deltoids, and triceps.',
            'instructions': '1. Lie flat on the bench with feet firmly planted on the floor.\n2. Grip the barbell slightly wider than shoulder-width.\n3. Unrack with control, inhale and lower the bar smoothly to your mid-chest.\n4. Drive your feet into the floor and press the bar explosively back to lockout.',
            'form_tips': 'Keep your shoulder blades retracted and pinched into the bench throughout the movement. Avoid flaring elbows past 75 degrees.',
            'image_url': 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?auto=format&fit=crop&w=800&q=80'
        },
        {
            'name': 'Incline Dumbbell Press',
            'slug': 'incline-dumbbell-press',
            'target_muscle': 'Chest',
            'equipment': 'Dumbbells',
            'difficulty': 'Intermediate',
            'description': 'Isolates and emphasizes the clavicular (upper) head of the chest while allowing a deeper range of motion.',
            'instructions': '1. Set bench to 30-45 degrees angle.\n2. Kick dumbbells up to shoulder level.\n3. Press upward in a slight arc until arms are extended without locking elbows.\n4. Lower with a controlled 3-second eccentric tempo.',
            'form_tips': 'Do not set the incline too steep (above 45 degrees) or front delts will take over the movement.',
            'image_url': 'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?auto=format&fit=crop&w=800&q=80'
        },
        {
            'name': 'Barbell Back Squat',
            'slug': 'barbell-back-squat',
            'target_muscle': 'Legs',
            'equipment': 'Barbell',
            'difficulty': 'Advanced',
            'description': 'The king of lower body movements. Builds raw quad, glute, hamstring, and core stability.',
            'instructions': '1. Rest the barbell securely across your upper traps or rear delts.\n2. Stand with feet slightly wider than shoulder-width, toes turned 15-30 degrees outward.\n3. Take a deep diaphragmatic breath, brace your core, and sit hips back and down.\n4. Hit parallel or below, then press the floor away through midfoot to stand up.',
            'form_tips': 'Keep your chest tall and maintain a neutral spine. Do not allow your knees to collapse inward.',
            'image_url': 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80'
        },
        {
            'name': 'Romanian Deadlift (RDL)',
            'slug': 'romanian-deadlift',
            'target_muscle': 'Legs',
            'equipment': 'Barbell',
            'difficulty': 'Intermediate',
            'description': 'Premier posterior chain exercise emphasizing hamstring stretch, glute contraction, and lower back endurance.',
            'instructions': '1. Hold barbell at hip height with an overhand grip.\n2. Keep knees soft (slight bend) and hinge at your hips, sending your hips toward the wall behind you.\n3. Lower bar along your shins until you feel a deep stretch in hamstrings.\n4. Squeeze glutes firmly and push hips forward to return to standing.',
            'form_tips': 'Movement comes from hip hinge, not spinal flexion. Keep bar glued close to thighs and shins.',
            'image_url': 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80'
        },
        {
            'name': 'Pull-Ups',
            'slug': 'pull-ups',
            'target_muscle': 'Back',
            'equipment': 'Bodyweight',
            'difficulty': 'Intermediate',
            'description': 'Ultimate upper-body vertical pull building wide latissimus dorsi, rhomboids, and biceps.',
            'instructions': '1. Grip pull-up bar with palms facing away, slightly wider than shoulder-width.\n2. Hang at dead hang with engaged core.\n3. Depress your shoulder blades and pull chest toward the bar.\n4. Clear your chin above the bar, pause briefly, and lower under complete control.',
            'form_tips': 'Avoid kicking your legs or swinging. Imagine driving your elbows down into your back pockets.',
            'image_url': 'https://images.unsplash.com/photo-1598971639058-fab3c3109a00?auto=format&fit=crop&w=800&q=80'
        },
        {
            'name': 'Chest-Supported Row',
            'slug': 'chest-supported-row',
            'target_muscle': 'Back',
            'equipment': 'Dumbbells',
            'difficulty': 'Beginner',
            'description': 'Strict mid-back row that eliminates lower back fatigue and maximizes upper-back muscle mind connection.',
            'instructions': '1. Lie face down on an incline bench set to 30 degrees with dumbbells on the floor.\n2. Grab dumbbells with neutral or overhand grip.\n3. Pull elbows up and back, squeezing shoulder blades together at the peak.\n4. Lower with full stretch at the bottom.',
            'form_tips': 'Do not shrug shoulders up toward ears. Keep neck in neutral alignment with your spine.',
            'image_url': 'https://images.unsplash.com/photo-1605296867304-46d5465a13f1?auto=format&fit=crop&w=800&q=80'
        },
        {
            'name': 'Overhead Dumbbell Shoulder Press',
            'slug': 'overhead-dumbbell-press',
            'target_muscle': 'Shoulders',
            'equipment': 'Dumbbells',
            'difficulty': 'Intermediate',
            'description': 'Builds boulder shoulders, upper chest stability, and overhead functional pressing power.',
            'instructions': '1. Sit on a vertical upright bench with dumbbells at ear height.\n2. Press overhead in a smooth path until arms are fully extended.\n3. Lower steadily to 90 degrees or chin level before pressing again.',
            'form_tips': 'Keep core tight and ribcage down to prevent excessive lumbar arching.',
            'image_url': 'https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?auto=format&fit=crop&w=800&q=80'
        },
        {
            'name': 'Hanging Knee / Leg Raises',
            'slug': 'hanging-leg-raises',
            'target_muscle': 'Core',
            'equipment': 'Bodyweight',
            'difficulty': 'Intermediate',
            'description': 'Highly effective abdominal movement targeting lower rectus abdominis and hip flexor strength.',
            'instructions': '1. Hang from a pull-up bar with an active shoulder posture.\n2. Posteriorly tilt your pelvis and raise knees/toes toward chest level.\n3. Control the lowering phase without swinging back and forth.',
            'form_tips': 'Focus on curling your pelvis upward rather than simply swinging your thighs.',
            'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=800&q=80'
        },
        {
            'name': 'Kettlebell Swing',
            'slug': 'kettlebell-swing',
            'target_muscle': 'Full Body',
            'equipment': 'Kettlebell',
            'difficulty': 'Beginner',
            'description': 'Dynamic explosive ballistic movement forging explosive hip hinge power and intense cardiovascular conditioning.',
            'instructions': '1. Stand with feet slightly wider than shoulder-width, kettlebell one foot in front.\n2. Hinge at hips and hike kettlebell between your legs.\n3. Snap hips explosively forward to propel kettlebell to chest height.\n4. Allow bell to drop naturally back into hip crease and repeat rhythmically.',
            'form_tips': 'Do not squat the bell or lift with your arms; all momentum comes from forceful hip snap.',
            'image_url': 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80'
        },
        {
            'name': 'Push-Ups (Form Perfect)',
            'slug': 'perfect-pushups',
            'target_muscle': 'Chest',
            'equipment': 'Bodyweight',
            'difficulty': 'Beginner',
            'description': 'Timeless classic bodyweight compound pushing movement for chest, triceps, and anterior delts.',
            'instructions': '1. Assume a plank position with hands slightly wider than shoulder-width.\n2. Brace core, squeeze glutes, lower chest to within an inch of the floor.\n3. Push firmly through palm bases to return to top plank.',
            'form_tips': 'Maintain a rigid straight plank line from heels to ears throughout all repetitions.',
            'image_url': 'https://images.unsplash.com/photo-1598971639058-fab3c3109a00?auto=format&fit=crop&w=800&q=80'
        }
    ]

    workouts = [
        {
            'title': 'Upper Body Hypertrophy Blast',
            'slug': 'upper-body-hypertrophy-blast',
            'description': 'A high-yield upper body split designed for maximum muscular growth, v-taper aesthetics, and pressing power. Targets chest, upper back, shoulders, and triceps.',
            'difficulty': 'Intermediate',
            'duration_minutes': 45,
            'target_muscle': 'Chest & Triceps',
            'calories_burned': 380,
            'image_url': 'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?auto=format&fit=crop&w=800&q=80',
            'featured': True,
            'routine': [
                {'exercise_slug': 'barbell-bench-press', 'order': 1, 'sets': 4, 'reps': '8-10', 'rest_seconds': 90},
                {'exercise_slug': 'chest-supported-row', 'order': 2, 'sets': 4, 'reps': '10-12', 'rest_seconds': 75},
                {'exercise_slug': 'incline-dumbbell-press', 'order': 3, 'sets': 3, 'reps': '10-12', 'rest_seconds': 60},
                {'exercise_slug': 'overhead-dumbbell-press', 'order': 4, 'sets': 3, 'reps': '12-15', 'rest_seconds': 60}
            ]
        },
        {
            'title': 'Lower Body Quad & Glute Overload',
            'slug': 'lower-body-quad-glute-overload',
            'description': 'Heavy compound lower body session to build explosive leg power, sculpted quads, and indestructible hamstrings.',
            'difficulty': 'Advanced',
            'duration_minutes': 55,
            'target_muscle': 'Legs & Glutes',
            'calories_burned': 480,
            'image_url': 'https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80',
            'featured': True,
            'routine': [
                {'exercise_slug': 'barbell-back-squat', 'order': 1, 'sets': 5, 'reps': '5-8', 'rest_seconds': 120},
                {'exercise_slug': 'romanian-deadlift', 'order': 2, 'sets': 4, 'reps': '8-10', 'rest_seconds': 90},
                {'exercise_slug': 'kettlebell-swing', 'order': 3, 'sets': 3, 'reps': '15-20', 'rest_seconds': 60}
            ]
        },
        {
            'title': 'Express 20-Min Dorm HIIT Burn',
            'slug': 'express-20-min-dorm-hiit',
            'description': 'Zero equipment needed. High-intensity interval routine created specifically for busy college students to burn fat and elevate metabolism in minutes.',
            'difficulty': 'Beginner',
            'duration_minutes': 20,
            'target_muscle': 'Full Body',
            'calories_burned': 240,
            'image_url': 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80',
            'featured': True,
            'routine': [
                {'exercise_slug': 'perfect-pushups', 'order': 1, 'sets': 4, 'reps': '15 reps', 'rest_seconds': 30},
                {'exercise_slug': 'hanging-leg-raises', 'order': 2, 'sets': 3, 'reps': '12-15 reps', 'rest_seconds': 30},
                {'exercise_slug': 'kettlebell-swing', 'order': 3, 'sets': 4, 'reps': '45 secs', 'rest_seconds': 30}
            ]
        },
        {
            'title': 'V-Taper Pull & Lat Sculptor',
            'slug': 'v-taper-pull-lat-sculptor',
            'description': 'Focuses on the vertical and horizontal pulling chains to forge that classic aesthetic wide back and strong posterior posture.',
            'difficulty': 'Intermediate',
            'duration_minutes': 40,
            'target_muscle': 'Back & Biceps',
            'calories_burned': 350,
            'image_url': 'https://images.unsplash.com/photo-1598971639058-fab3c3109a00?auto=format&fit=crop&w=800&q=80',
            'featured': False,
            'routine': [
                {'exercise_slug': 'pull-ups', 'order': 1, 'sets': 4, 'reps': 'Failure or 8-10', 'rest_seconds': 90},
                {'exercise_slug': 'chest-supported-row', 'order': 2, 'sets': 4, 'reps': '10-12', 'rest_seconds': 60},
                {'exercise_slug': 'romanian-deadlift', 'order': 3, 'sets': 3, 'reps': '10 reps', 'rest_seconds': 75}
            ]
        },
        {
            'title': 'Core Armor & Functional Abs',
            'slug': 'core-armor-functional-abs',
            'description': 'Target deep transverse abdominis, rectus abdominis, and obliques for bulletproof spine health and visible definition.',
            'difficulty': 'Beginner',
            'duration_minutes': 25,
            'target_muscle': 'Core & Abs',
            'calories_burned': 210,
            'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=800&q=80',
            'featured': False,
            'routine': [
                {'exercise_slug': 'hanging-leg-raises', 'order': 1, 'sets': 4, 'reps': '15 reps', 'rest_seconds': 45},
                {'exercise_slug': 'perfect-pushups', 'order': 2, 'sets': 3, 'reps': '20 reps', 'rest_seconds': 45}
            ]
        },
        {
            'title': 'Full Body Athletic Conditioning',
            'slug': 'full-body-athletic-conditioning',
            'description': 'Synthesizes strength lifts and anaerobic power. Designed for functional mobility, agility, and overall body recomposition.',
            'difficulty': 'Advanced',
            'duration_minutes': 50,
            'target_muscle': 'Full Body',
            'calories_burned': 520,
            'image_url': 'https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80',
            'featured': False,
            'routine': [
                {'exercise_slug': 'barbell-back-squat', 'order': 1, 'sets': 4, 'reps': '8 reps', 'rest_seconds': 90},
                {'exercise_slug': 'barbell-bench-press', 'order': 2, 'sets': 4, 'reps': '8 reps', 'rest_seconds': 90},
                {'exercise_slug': 'pull-ups', 'order': 3, 'sets': 3, 'reps': '8 reps', 'rest_seconds': 60},
                {'exercise_slug': 'kettlebell-swing', 'order': 4, 'sets': 3, 'reps': '20 reps', 'rest_seconds': 45}
            ]
        }
    ]

    nutrition = [
        {
            'title': 'Crispy High-Protein Air Fryer Chicken Bowl',
            'slug': 'crispy-protein-chicken-bowl',
            'category': 'High Protein',
            'calories': 520,
            'protein': 54.0,
            'carbs': 48.0,
            'fats': 12.0,
            'prep_time': 20,
            'ingredients': '200g Chicken breast cut into bite-sized cubes | 1 cup Jasmine rice (cooked) | 1 tbsp Olive oil & smoked paprika | 1/2 Avocado sliced | Fresh cucumber & cherry tomatoes | Low-sugar spicy sriracha mayo (1 tbsp)',
            'instructions': '1. Toss chicken cubes with smoked paprika, garlic powder, salt, and half the olive oil.\n2. Air fry at 200°C (400°F) for 10-12 minutes until golden and crispy.\n3. Layer jasmine rice in a bowl, arrange crispy chicken, cucumber, tomatoes, and sliced avocado.\n4. Drizzle with light sriracha mayo and garnish with sesame seeds.',
            'tips': 'Meal prep friendly: Cook 3-4 portions in advance. Chicken stays crispy in airtight containers up to 4 days.',
            'image_url': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Berry Anabolic Protein Power Oats',
            'slug': 'berry-anabolic-protein-oats',
            'category': 'Post-Workout',
            'calories': 440,
            'protein': 42.0,
            'carbs': 52.0,
            'fats': 7.0,
            'prep_time': 10,
            'ingredients': '60g Rolled oats | 1 scoop Whey or plant protein (vanilla) | 1 cup Unsweetened almond milk | 1/2 cup Mixed fresh blueberries and raspberries | 1 tbsp Chia seeds | Dash of cinnamon & drizzle of honey',
            'instructions': '1. Cook rolled oats in almond milk on medium heat or microwave for 2 minutes.\n2. Let cool for 60 seconds so the protein powder blends smoothly without clumping.\n3. Whisk in vanilla protein powder and cinnamon until creamy.\n4. Top with fresh berries and chia seeds.',
            'tips': 'Great 30-45 minutes post-workout when insulin sensitivity and protein synthesis are heightened.',
            'image_url': 'https://images.unsplash.com/photo-1517673132405-a56a62b18caf?auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Loaded Avocado & Egg Sourdough Toast',
            'slug': 'loaded-avocado-egg-sourdough',
            'category': 'Pre-Workout',
            'calories': 390,
            'protein': 22.0,
            'carbs': 35.0,
            'fats': 18.0,
            'prep_time': 12,
            'ingredients': '2 slices Artisanal sourdough bread | 2 Pasture-raised eggs (poached or sunny side) | 1/2 Hass avocado mashed | Chili flakes & sea salt | Microgreens for garnish',
            'instructions': '1. Toast sourdough slices until crispy.\n2. Mash avocado with a squeeze of fresh lime juice, salt, and pepper.\n3. Spread avocado onto toast and top each slice with a soft-cooked egg.\n4. Sprinkle chili flakes and microgreens.',
            'tips': 'Sourdough provides slow-digesting complex carbs that deliver steady workout energy without blood sugar spikes.',
            'image_url': 'https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=800&q=80'
        },
        {
            'title': 'Plant-Powered Mediterranean Tofu Scramble',
            'slug': 'mediterranean-tofu-scramble',
            'category': 'Plant-Based',
            'calories': 380,
            'protein': 30.0,
            'carbs': 20.0,
            'fats': 16.0,
            'prep_time': 15,
            'ingredients': '200g Extra-firm tofu pressed and crumbled | 1 cup Baby spinach | 1/2 cup Kalamata olives and cherry tomatoes | 1 tsp Nutritional yeast & turmeric powder | 1 tbsp Extra virgin olive oil',
            'instructions': '1. Heat olive oil in a skillet on medium.\n2. Add crumbled tofu, turmeric, garlic powder, and nutritional yeast. Sauté for 5 minutes.\n3. Fold in spinach and cherry tomatoes until wilted.\n4. Serve hot with warm pita or roasted sweet potatoes.',
            'tips': 'Nutritional yeast provides rich savory umami flavor along with fortified Vitamin B12.',
            'image_url': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=800&q=80'
        }
    ]

    blogs = [
        {
            'title': 'Progressive Overload: The Only Hypertrophy Law That Actually Matters',
            'slug': 'progressive-overload-hypertrophy-guide',
            'excerpt': 'Why changing workouts every week is killing your gains, and the simple tracking system to guarantee you build muscle consistently.',
            'content': """
### The Muscle Growth Paradox

In an era of TikTok fitness algorithms, you're constantly bombarded with "shock the muscle" tricks and convoluted supersets. But exercise science tells a vastly simpler, more powerful truth: **muscles grow in response to mechanical tension over time**.

If you squat 100 kg for 8 reps today, and 6 months from now you're still squatting 100 kg for 8 reps, your body has zero biological reason to add new muscle tissue.

### What is Progressive Overload?

Progressive overload simply means systematically increasing the demands placed on your musculoskeletal system over successive training sessions.

You do NOT just have to add weight to the bar. Progressive overload can take several forms:

1. **Adding Resistance**: Moving from 20 kg dumbbells to 22.5 kg dumbbells.
2. **Adding Repetitions**: Hitting 10 clean reps where you previously managed 8.
3. **Improving Form & Control**: Slowing down the eccentric phase (the lowering) with zero momentum.
4. **Increasing Volume**: Adding an extra high-quality working set.
5. **Shortening Rest Intervals**: Performing identical work with less downtime between sets.

### How to Apply It in Your Next Workout

Pick 4-5 compound exercises per workout. Keep a simple note on your phone. Record your exact weight and reps. Next week, your singular goal is to beat that note by even 1 rep or 1 kg. That is the true secret of elite fitness.
""",
            'author': 'Marcus Vance, CSCS',
            'read_time': 5,
            'category': 'Training Science',
            'image_url': 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80',
            'featured': True
        },
        {
            'title': 'Creatine Monohydrate: Debunking Myths and Maximizing Cellular Hydration',
            'slug': 'creatine-monohydrate-debunking-myths',
            'excerpt': 'The most scientifically researched supplement on Earth unpacked: timing, dosage, hair loss myths, and how to take it properly.',
            'content': """
### The Most Researched Supplement on the Planet

With over 500 peer-reviewed scientific studies, Creatine Monohydrate holds the gold medal for efficacy, safety, and price-to-performance in sports nutrition. Yet myths still persist around kidneys, dehydration, and bloating.

### How Creatine Actually Works

Creatine increases your muscles' phosphocreatine stores. Phosphocreatine helps form **ATP (adenosine triphosphate)**, the key molecule your cells use for energy during explosive efforts like heavy lifting or sprinting.

More phosphocreatine = 1-2 extra reps at high intensity = higher training volume = faster strength and muscle gains.

### Key Takeaways for Gen-Z Lifters:
- **Dose**: 3 to 5 grams daily is optimal. No expensive "loading phase" is strictly necessary.
- **Timing**: Consistency beats timing. Take it daily with water or juice.
- **Hair Loss Myth**: High-quality meta-analyses show no causal link to dihydrotestosterone (DHT) spikes.
- **Water Weight**: Creatine draws water **intracellularly** (into muscle fibers), not extracellularly beneath the skin, giving muscles a fuller, more aesthetic look.
""",
            'author': 'Elena Rostova, Sports Nutritionist',
            'read_time': 4,
            'category': 'Nutrition',
            'image_url': 'https://images.unsplash.com/photo-1579758629938-03607ccdbaba?auto=format&fit=crop&w=800&q=80',
            'featured': False
        },
        {
            'title': 'Dorm Room Ergonomics & Posture: Fixing Tech Neck for Good',
            'slug': 'dorm-room-ergonomics-tech-neck-fix',
            'excerpt': 'Spent 8 hours hunched over your laptop studying? Here are three daily drills to restore cervical spine posture and relieve shoulder knots.',
            'content': """
### The College Student Posture Epidemic

Hunched over desks, slumped on beds with laptops, and staring down at smartphones for hours leads to what physical therapists call **Upper Crossed Syndrome** (forward head posture, internally rotated shoulders, and rounded upper back).

Not only does this cause headaches and neck fatigue, it directly sabotages your bench press and overhead mobility in the gym.

### The 3-Minute Daily Reset

1. **Chin Tucks (15 reps)**: Pull your chin straight back as if making a double chin. Hold for 2 seconds. Realigns cervical vertebrae.
2. **Band Pull-Aparts or Doorway Y-T-W (2 sets of 12)**: Engages the rhomboids and lower trapezius, pulling the shoulders back into proper pocket alignment.
3. **Doorway Pectoral Stretch (30 seconds per side)**: Loosens tight, shortened chest fibers from desk sitting.
""",
            'author': 'Dr. Kai Chen, DPT',
            'read_time': 4,
            'category': 'Recovery & Wellness',
            'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80',
            'featured': False
        }
    ]

    return {
        'users': users,
        'exercises': exercises,
        'workouts': workouts,
        'nutrition': nutrition,
        'blogs': blogs
    }

def seed_database(app):
    """Seed the database within application context."""
    with app.app_context():
        # Ensure tables exist
        db.create_all()
        
        # Check if already seeded
        if Workout.query.first():
            print("[PulseFit Seed] Database already contains records. Skipping seed.")
            return True

        print("[PulseFit Seed] Seeding fresh data...")
        data = get_seed_data()

        # Seed Users
        test_user = None
        for u in data['users']:
            user = User(
                username=u['username'],
                email=u['email'],
                full_name=u['full_name'],
                fitness_goal=u['fitness_goal'],
                fitness_level=u['fitness_level']
            )
            user.set_password(u['password'])
            db.session.add(user)
            if not test_user:
                test_user = user
        db.session.commit()

        # Seed Exercises
        exercise_map = {}
        for ex_data in data['exercises']:
            ex = Exercise(
                name=ex_data['name'],
                slug=ex_data['slug'],
                target_muscle=ex_data['target_muscle'],
                equipment=ex_data['equipment'],
                difficulty=ex_data['difficulty'],
                description=ex_data['description'],
                instructions=ex_data['instructions'],
                form_tips=ex_data['form_tips'],
                image_url=ex_data['image_url']
            )
            db.session.add(ex)
            exercise_map[ex_data['slug']] = ex
        db.session.commit()

        # Seed Workouts & Routines
        first_workout = None
        for w_data in data['workouts']:
            w = Workout(
                title=w_data['title'],
                slug=w_data['slug'],
                description=w_data['description'],
                difficulty=w_data['difficulty'],
                duration_minutes=w_data['duration_minutes'],
                target_muscle=w_data['target_muscle'],
                calories_burned=w_data['calories_burned'],
                image_url=w_data['image_url'],
                featured=w_data['featured']
            )
            db.session.add(w)
            db.session.flush() # get w.id
            if not first_workout:
                first_workout = w

            for r_item in w_data.get('routine', []):
                slug = r_item['exercise_slug']
                if slug in exercise_map:
                    we = WorkoutExercise(
                        workout_id=w.id,
                        exercise_id=exercise_map[slug].id,
                        order=r_item['order'],
                        sets=r_item['sets'],
                        reps=r_item['reps'],
                        rest_seconds=r_item['rest_seconds']
                    )
                    db.session.add(we)
        db.session.commit()

        # Seed Nutrition Recipes
        for n_data in data['nutrition']:
            n = Nutrition(
                title=n_data['title'],
                slug=n_data['slug'],
                category=n_data['category'],
                calories=n_data['calories'],
                protein=n_data['protein'],
                carbs=n_data['carbs'],
                fats=n_data['fats'],
                prep_time=n_data['prep_time'],
                ingredients=n_data['ingredients'],
                instructions=n_data['instructions'],
                tips=n_data['tips'],
                image_url=n_data['image_url']
            )
            db.session.add(n)
        db.session.commit()

        # Seed Blog Posts
        for b_data in data['blogs']:
            b = BlogPost(
                title=b_data['title'],
                slug=b_data['slug'],
                excerpt=b_data['excerpt'],
                content=b_data['content'],
                author=b_data['author'],
                read_time=b_data['read_time'],
                category=b_data['category'],
                image_url=b_data['image_url'],
                featured=b_data['featured']
            )
            db.session.add(b)
        db.session.commit()

        # Seed a sample favorite for the test user
        if test_user and first_workout:
            fav = Favorite(user_id=test_user.id, workout_id=first_workout.id)
            db.session.add(fav)
            db.session.commit()

        print("[PulseFit Seed] Database successfully seeded with rich content!")
        return True

if __name__ == '__main__':
    from app import app
    seed_database(app)
