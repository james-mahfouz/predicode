import shutil
# from bson import ObjectId
from fastapi.responses import JSONResponse
import base64
import os
from zipfile import ZipFile
from models.fileModel import File
from rapidfuzz import fuzz
import textract


# from models.userModel import User
word_dict = {
    'ART_AND_DESIGN': ['painting', 'drawing', 'sculpture', 'architecture', 'photography', 'graphic design', 'fashion',
                       'ceramics', 'illustration', 'printmaking', 'jewelry', 'textile design', 'interior design',
                       'animation', 'visual arts', 'mixed media', 'crafts', 'digital art', 'fine art', 'cartooning',
                       'collage', 'public art', 'installation art', 'conceptual art', 'art history', 'performance art',
                       'decorative arts', 'artistic expression', 'art education', 'art therapy'],

    'AUTO_AND_VEHICLES': ['car', 'vehicle', 'automobile', 'truck', 'motorcycle', 'boat', 'suv', 'sedan', 'coupe',
                          'convertible', 'minivan', 'pickup truck', 'off-road vehicle', 'classic car', 'hybrid car',
                          'electric car', 'car rental', 'car sharing', 'car repair', 'car maintenance', 'auto parts',
                          'car customization', 'auto racing', 'driving', 'traffic', 'parking', 'gasoline', 'oil change',
                          'tire'],

    'BEAUTY': ['makeup', 'skincare', 'haircare', 'perfume', 'nail polish', 'beauty products', 'cosmetics', 'beauty tips',
               'facial', 'eyelash', 'eyebrow', 'lipstick', 'foundation', 'blush', 'bronzer', 'mascara', 'shampoo',
               'conditioner', 'hair styling', 'haircut', 'hair color', 'skin type', 'anti-aging', 'acne', 'wrinkles',
               'dark circles', 'beauty routine', 'beauty trends', 'beauty influencers'],

    'BOOKS_AND_REFERENCE': ['novel', 'fiction', 'non-fiction', 'literature', 'poetry', 'ebook', 'audiobook', 'bookstore',
                            'library', 'reading', 'writing', 'author', 'publisher', 'manuscript', 'book club', 'book review',
                            'reference book', 'encyclopedia', 'dictionary', 'thesaurus', 'biography', 'memoir', 'history book',
                            'religious book', 'philosophy book', 'cookbook', 'self-help book', 'comic book', 'manga'],

    'BUSINESS': ['startup', 'entrepreneurship', 'small business', 'marketing', 'finance', 'accounting', 'business plan',
                 'sales', 'advertising', 'public relations', 'customer service', 'management', 'leadership', 'human resources',
                 'consulting', 'business strategy', 'e-commerce', 'supply chain', 'logistics', 'mergers and acquisitions',
                 'business law', 'international business', 'business ethics', 'business news', 'trade', 'industry',
                 'productivity', 'innovation', 'business networking'],

    'COMICS': ['comic book', 'cartoon', 'graphic novel', 'superhero', 'manga', 'comic strip', 'webcomic', 'humor', 'animation',
               'illustration', 'funny', 'satire', 'fantasy', 'sci-fi', 'villain', 'hero', 'DC Comics', 'Marvel Comics',
               'comic convention', 'comic art', 'comic writer', 'comic artist', 'comic collector', 'comic character',
               'comic store', 'comic fandom', 'comic movie', 'comic franchise', 'comic merchandise', 'comic culture'],

    'COMMUNICATION': ['conversation', 'messaging', 'email', 'telephone', 'face-to-face', 'writing', 'speaking',
                      'social media', 'broadcasting', 'journalism', 'public speaking', 'speech', 'debate', 'dialogue',
                      'interpersonal', 'nonverbal', 'listening', 'tone', 'message', 'media', 'telecommunication',
                      'networking', 'contact', 'information', 'connection', 'expressive', 'communication skills',
                      'communication style', 'communication channels', 'communication barriers'],

    'DATING': ['relationship', 'love', 'romance', 'attraction', 'matchmaking', 'compatibility', 'chemistry',
               'courtship', 'flirting', 'seduction', 'intimacy', 'commitment', 'affection', 'infatuation', 'breakup',
               'heartbreak', 'trust', 'communication', 'dating app', 'blind date', 'speed dating', 'online dating',
               'dating advice', 'dating coach', 'dating game', 'dating rules', 'dating etiquette', 'dating culture',
               'dating trends', 'dating rituals'],

    'EDUCATION': ['learning', 'teaching', 'school', 'college', 'university', 'teacher', 'student', 'curriculum',
                  'textbook', 'homework', 'lecture', 'classroom', 'exam', 'degree', 'knowledge', 'discipline',
                  'subject', 'academic', 'research', 'training', 'e-learning', 'distance learning', 'tutoring',
                  'mentoring', 'professional development', 'continuing education', 'learning styles',
                  'learning disabilities', 'educational technology', 'educational psychology'],

    'ENTERTAINMENT': ['music', 'film', 'television', 'theatre', 'performing arts', 'visual arts', 'comedy', 'drama',
                      'documentary', 'animation', 'horror', 'science fiction', 'fantasy', 'action', 'adventure',
                      'romantic', 'thriller', 'sitcom', 'reality TV', 'celebrity', 'entertainer', 'concert',
                      'live performance', 'festivals', 'awards shows', 'box office', 'critics', 'audience',
                      'entertainment industry'],

    'EVENTS': ['conferences', 'meetings', 'festivals', 'concerts', 'ceremonies', 'celebrations', 'exhibitions',
               'workshops', 'trade shows', 'product launches', 'sporting events', 'charity events', 'political events',
               'networking events', 'social events', 'weddings', 'parties', 'conventions', 'performances', 'seminars',
               'competitions', 'awards ceremonies', 'cultural events', 'entertainment', 'fundraisers',
               'music festivals', 'film festivals', 'arts events', 'fairs', 'parades'],

    'FAMILY': ['parents', 'children', 'siblings', 'spouses', 'grandparents', 'aunts', 'uncles', 'cousins', 'relatives',
               'in-laws', 'kin', 'nuclear family', 'extended family', 'family tree', 'family history',
               'family dynamics', 'family values', 'family traditions', 'family rituals', 'family time',
               'family support', 'family conflicts', 'family responsibilities', 'family relationships',
               'family communication', 'family structure', 'family roles', 'family health', 'family education',
               'family planning'],

    'FINANCE': ['money', 'budgeting', 'investing', 'savings', 'taxes', 'financial planning', 'credit', 'loans',
                'mortgages', 'insurance', 'retirement', 'wealth', 'debt', 'income', 'expenses', 'assets', 'liabilities',
                'cash flow', 'stocks', 'bonds', 'real estate', 'personal finance', 'business finance',
                'financial management', 'financial literacy', 'financial security', 'financial risks',
                'financial products', 'financial services', 'financial markets'],

    'FOOD_AND_DRINK': ['cooking', 'baking', 'recipes', 'cuisine', 'food culture', 'food history', 'food science',
                       'nutrition', 'health', 'diet', 'ingredients', 'cooking techniques', 'kitchen appliances',
                       'food safety', 'culinary arts', 'gastronomy', 'food industry', 'restaurant industry',
                       'food service', 'beverages', 'alcoholic drinks', 'non-alcoholic drinks', 'wine', 'beer',
                       'spirits', 'coffee', 'tea', 'juices', 'smoothies', 'cocktails'],

    'GAME': ['video games', 'board games', 'card games', 'role-playing games', 'puzzle games', 'strategy games',
             'action games', 'adventure games', 'sports games', 'simulation games', 'casual games', 'multiplayer games',
             'single-player games', 'console games', 'PC games', 'mobile games', 'online games', 'gaming culture',
             'gaming industry', 'game development', 'game design', 'game mechanics', 'gameplay', 'gamer community',
             'e-sports', 'gaming hardware', 'gaming software', 'game streaming', 'game marketing'],

    'HEALTH_AND_FITNESS': ['exercise', 'nutrition', 'workouts', 'fitness goals', 'healthy eating', 'weight loss',
                           'strength training', 'cardio', 'yoga', 'pilates', 'meditation', 'mindfulness',
                           'mental health', 'physical health', 'health apps', 'personal training', 'gym',
                           'outdoor activities', 'sports', 'recovery', 'wellness', 'lifestyle changes',
                           'fitness equipment', 'bodybuilding', 'running', 'cycling', 'swimming', 'hiking', 'dance',
                           'nutrition supplements'],

    'HOUSE_AND_HOME': ['interior design', 'home improvement', 'home decor', 'furniture', 'home renovation', 'DIY',
                       'home organization', 'cleaning', 'gardening', 'landscaping', 'home maintenance',
                       'home automation', 'smart home', 'home security', 'home appliances', 'home technology',
                       'energy efficiency', 'home utilities', 'home safety', 'home entertainment', 'home office',
                       'home buying', 'home selling', 'real estate', 'property management', 'housing trends',
                       'home financing', 'mortgage rates', 'home insurance', 'home warranties'],

    'LIBRARIES_AND_DEMO': ['sample code', 'open source', 'demonstration software', 'libraries', 'APIs',
                           'developer tools', 'programming languages', 'app development', 'web development', 'testing',
                           'debugging', 'software development', 'software engineering', 'computer programming',
                           'mobile development', 'cloud computing', 'database management', 'data analysis',
                           'artificial intelligence', 'machine learning', 'natural language processing',
                           'computer vision', 'virtual reality', 'augmented reality', 'game development',
                           'video editing', 'audio editing', 'animation', 'graphic design'],

    'LIFESTYLE': ['fashion', 'beauty', 'travel', 'food', 'entertainment', 'music', 'art', 'culture', 'books', 'films',
                  'TV shows', 'streaming', 'social media', 'relationships', 'personal development', 'self-improvement',
                  'motivation', 'productivity', 'time management', 'creativity', 'hobbies', 'crafts', 'DIY projects',
                  'parenting', 'pets', 'outdoor activities', 'sports', 'fitness', 'health', 'mindfulness'],

    'MAPS_AND_NAVIGATION': ['GPS', 'directions', 'maps', 'traffic updates', 'transit information', 'navigation apps',
                            'geolocation', 'location-based services', 'local search', 'travel planning',
                            'driving directions', 'walking directions', 'public transportation', 'ride-sharing',
                            'car rental', 'bicycle rental', 'motorcycle rental', 'GPS tracking', 'outdoor recreation',
                            'hiking trails', 'campgrounds', 'tourist attractions', 'points of interest', 'landmarks',
                            'street view', 'satellite view', 'real-time location data', 'route optimization',
                            'fleet management'],

    'MEDICAL': ['healthcare', 'medicine', 'illness', 'injury', 'treatment', 'diagnosis', 'symptoms', 'mental health',
                'physical therapy', 'occupational therapy', 'medication', 'medical devices', 'surgery',
                'disease prevention', 'health insurance', 'health policy', 'medical research', 'public health',
                'pandemics', 'vaccinations', 'clinical trials', 'health education', 'medical terminology',
                'telemedicine', 'genetics', 'biotechnology', 'nutrition', 'obesity', 'addiction', 'cancer'],

    'NEWS_AND_MAGAZINES': ['breaking news', 'local news', 'national news', 'international news', 'politics', 'business',
                           'technology', 'entertainment news', 'celebrity gossip', 'sports news', 'health news',
                           'science news', 'environmental news', 'travel news', 'food news', 'book reviews',
                           'movie reviews', 'TV reviews', 'music reviews', 'opinion pieces', 'editorials',
                           'investigative journalism', 'journalism ethics', 'media literacy', 'fake news', 'clickbait',
                           'headlines', 'current events', 'world news'],

    'PARENTING': ['pregnancy', 'childbirth', 'newborns', 'infants', 'toddlers', 'preschoolers', 'school-age children',
                  'teenagers', 'parenting styles', 'discipline', 'child development', 'parent-child relationships',
                  'family dynamics', 'single parenting', 'co-parenting', 'adoption', 'fostering', 'child care',
                  'education', 'special needs parenting', 'parenting challenges', 'parenting advice',
                  'parenting resources', 'parenting communities', 'parenting books', 'parenting podcasts',
                  'parenting blogs', 'family activities', 'parenting humor'],

    'PERSONALIZATION': ['customization', 'themes', 'wallpapers', 'widgets', 'launchers', 'home screen', 'lock screen',
                        'fonts', 'icons', 'emoji', 'stickers', 'ringtones', 'notifications', 'live wallpapers',
                        'personalized recommendations', 'artificial intelligence', 'machine learning',
                        'contextual awareness', 'user preferences', 'personal data', 'privacy settings',
                        'user interface', 'user experience', 'accessibility', 'assistive technology',
                        'speech recognition', 'facial recognition', 'fingerprint recognition', 'eye tracking'],

    'PHOTOGRAPHY': ['photography techniques', 'composition', 'lighting', 'exposure', 'shutter speed', 'aperture', 'ISO',
                    'white balance', 'post-processing', 'image editing', 'retouching', 'photo filters', 'color grading',
                    'black and white photography', 'portrait photography', 'landscape photography',
                    'street photography', 'documentary photography', 'travel photography', 'wildlife photography',
                    'fashion photography', 'fine art photography', 'product photography', 'photography gear',
                    'camera equipment', 'lenses', 'tripods', 'camera bags'],

    'PRODUCTIVITY': ['efficiency', 'time management', 'task prioritization', 'goal setting', 'project management',
                     'productivity hacks', 'work-life balance', 'focus', 'procrastination', 'deadlines', 'multitasking',
                     'planning', 'organizing', 'streamlining', 'automation', 'optimization', 'self-discipline',
                     'self-motivation', 'creativity', 'innovation', 'continuous improvement', 'learning',
                     'growth mindset', 'resilience', 'stress management', 'mindfulness', 'meditation', 'exercise',
                     'healthy habits', 'rest', 'recreation'],

    'SHOPPING': ['retail therapy', 'online shopping', 'window shopping', 'bargain hunting', 'shopping addiction',
                 'impulsive buying', 'consumerism', 'brand loyalty', 'fashion trends', 'wardrobe essentials',
                 'accessories', 'beauty products', 'home decor', 'electronics', 'books', 'music', 'movies', 'gifts',
                 'shopping list', 'budgeting', 'coupons', 'loyalty programs', 'customer service', 'return policies',
                 'environmental impact', 'ethical consumption', 'sustainable fashion', 'secondhand market',
                 'local businesses', 'shopping malls'],

    'SOCIAL': ['social media', 'communication', 'connection', 'friendship', 'romance', 'family', 'community',
               'networking', 'digital identity', 'privacy', 'online reputation', 'cyberbullying', 'trolling',
               'fake news', 'filter bubbles', 'echo chambers', 'social comparison', 'FOMO', 'self-presentation',
               'self-disclosure', 'empathy', 'active listening', 'conflict resolution', 'teamwork', 'collaboration',
               'leadership', 'diversity', 'inclusion', 'social justice', 'volunteering'],

    'SPORTS': ['athletics', 'competition', 'team sports', 'individual sports', 'fitness', 'training', 'endurance',
               'strength', 'agility', 'speed', 'coordination', 'technique', 'performance', 'sportsmanship', 'fair play',
               'rules', 'equipment', 'injury prevention', 'recovery', 'sports psychology', 'motivation', 'focus',
               'self-confidence', 'discipline', 'strategy', 'tactics', 'analysis', 'commentary', 'spectatorship',
               'sports media'],

    'TOOLS': ['software', 'hardware', 'productivity tools', 'creativity tools', 'design tools', 'code editors',
              'version control', 'database management', 'file management', 'system utilities', 'security software',
              'data backup', 'cloud storage', 'password managers', 'browser extensions', 'mobile apps', 'web apps',
              'APIs', 'plug-ins', 'add-ons', 'user interface', 'user experience', 'accessibility', 'testing',
              'debugging', 'documentation', 'support', 'updates', 'upgrades'],

    'TRAVEL_AND_LOCAL': ['flight', 'hotel', 'rental car', 'travel', 'vacation', 'holiday', 'tourism', 'tourist',
                         'attraction', 'destination', 'sightseeing', 'trip', 'journey', 'cruise', 'adventure',
                         'backpacking', 'camping', 'hiking', 'backpacking', 'solo travel', 'budget travel',
                         'luxury travel', 'ecotourism', 'responsible travel', 'cultural experience', 'travel guide',
                         'passport', 'visa', 'currency exchange', 'maps'],

    'VIDEO_PLAYERS': ['video', 'streaming', 'media', 'entertainment', 'film', 'TV', 'cinema', 'animation', 'music',
                      'comedy', 'documentary', 'live streaming', 'short film', 'viral', 'videography', 'videographer',
                      'videoblog', 'video sharing', 'video production', 'video editing', 'special effects',
                      'video hosting', 'video game', 'e-sports', 'virtual reality', 'augmented reality',
                      'digital video', 'vlog', 'YouTube'],

    'WEATHER': ['forecast', 'temperature', 'humidity', 'wind', 'precipitation', 'climate', 'meteorology', 'sunshine',
                'storm', 'natural disaster', 'emergency', 'UV', 'air quality', 'pollution', 'rain', 'snow', 'cloud',
                'frost', 'heat wave', 'cold wave', 'global warming', 'ozone', 'environment', 'weather report',
                'weather map', 'drought', 'flood', 'hurricane']
}
# word_dict = {
#     'ART_AND_DESIGN': ["Art", "Design"],
#
#     'AUTO_AND_VEHICLES': ["Auto", "Vehicles"],
#
#     'BEAUTY': ["Beauty"],
#
#     'BOOKS_AND_REFERENCE': ["Books", "References"],
#
#     'BUSINESS': ['Business'],
#
#     'COMICS': ['comics'],
#
#     'COMMUNICATION': ['communication'],
#
#     'DATING': ["Dating"],
#
#     'EDUCATION': ['education'],
#
#     'ENTERTAINMENT': ['Entertainement'],
#
#     'EVENTS': ['events'],
#
#     'FAMILY': ['family'],
#
#     'FINANCE': ['finance'],
#
#     'FOOD_AND_DRINK': ['food', 'drink'],
#
#     'GAME': ['game'],
#
#     'HEALTH_AND_FITNESS': ['health', 'fitness'],
#
#     'HOUSE_AND_HOME': ['house', 'home'],
#
#     'LIBRARIES_AND_DEMO': ['libraries', 'demo'],
#
#     'LIFESTYLE': ['lifestyle'],
#
#     'MAPS_AND_NAVIGATION': ['maps', 'navigation'],
#
#     'MEDICAL': ['medical'],
#
#     'NEWS_AND_MAGAZINES': ['news', 'magazine'],
#
#     'PARENTING': ['parenting'],
#
#     'PERSONALIZATION': ['personalization'],
#
#     'PHOTOGRAPHY': ['photography'],
#
#     'PRODUCTIVITY': ['productivity'],
#
#     'SHOPPING': ['shopping'],
#
#     'SOCIAL': ['social'],
#
#     'SPORTS': ['sports'],
#
#     'TOOLS': ['tools'],
#
#     'TRAVEL_AND_LOCAL': ['travel', 'local'],
#
#     'VIDEO_PLAYERS': ['video players'],
#
#     'WEATHER': ['weather']
# }


def verify_user(user):
    return JSONResponse(content={
        "verified": "true",
        "username": user.name,
        "role": user.role
    })


def get_files(user):
    files_list = []
    for file in user.files:
        if File.objects(id=file.id).first() is not None:
            file_dict = file.to_mongo().to_dict()
            file_dict["_id"] = str(file_dict["_id"])
            files_list.append(file_dict)
        else:
            user.files.remove(file)
            user.save()

    return JSONResponse(content={
        "files": files_list,
        "user_name": user.name,
        "role": user.role
    })


def upload_file(file, user):
    unzipped_file_path = ""
    unzipped_file_name = ""
    temp_file_path = ''

    try:
        if file.content_type == "data:application/zip;base64":
            decoded_data = base64.b64decode(file.data)
            temp_file_path = f"./{file.name}"
            with open(temp_file_path, 'wb') as f:
                f.write(decoded_data)

            extracted_files = []

            with ZipFile(temp_file_path, "r") as zip_ref:
                for filename in zip_ref.namelist():
                    if not filename.startswith("__MACOSX"):
                        zip_ref.extract(filename)
                        if os.path.exists(filename):
                            extracted_files.append(filename)
            os.remove(temp_file_path)

            copied_folders = []
            for extracted_file in extracted_files:

                if not File.objects(name=str(extracted_file).split("/")[0] + "/").first():
                    if not str(extracted_file).split("/")[0] + "/" in copied_folders:
                        save_path = os.path.join('public', extracted_file)
                        shutil.move(extracted_file, save_path)

                        uploaded_file = File(name=extracted_file, by_user=user.name, path=save_path, size=file.size,
                                             category=file.category, content_rating=file.content_rating, price=file.price)
                        uploaded_file.save()

                        user.files.append(uploaded_file)
                        user.save()

                        copied_folders.append(str(extracted_file))

            removed_folders = []
            for extracted_file in extracted_files:
                if not str(extracted_file).split("/")[0] + "/" in removed_folders:
                    if os.path.exists(extracted_file):
                        if os.path.isdir(extracted_file):
                            shutil.rmtree(extracted_file)
                        else:
                            os.remove(extracted_file)

                    removed_folders.append(str(extracted_file))
            for extracted_file in extracted_files:
                print("started determining category")
                dict_counts = {category: 0 for category in word_dict}

                category_won = recursive_read_file(f"public/{extracted_file}", dict_counts)
                print("final count: ", category_won)

    except Exception as e:
        print(e)
        print("removing content")
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if os.path.exists(unzipped_file_name):
            unzipped_file_path = os.path.join('public', unzipped_file_name)
        if os.path.exists(unzipped_file_path):
            shutil.rmtree(unzipped_file_path)

        # Return an error message
        return {
            "message": "An error occurred while processing the file"
        }


def recursive_read_file(folder_path, count):
    if os.path.isfile(folder_path):
        if read_file(folder_path, count, word_dict):
            read_file(folder_path, count, word_dict)
    else:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                recursive_read_file(item_path, count)
            elif os.path.isfile(item_path):
                if read_file(item_path, count, word_dict):
                    read_file(item_path, count, word_dict)

    # print("finalcount: ", max(dict_counts, key=lambda k: dict_counts[k]))

    return max(count, key=lambda k: count[k])


def read_file(file_path, category_counts,  keywords):
    try:
        # print("trying")
        text = textract.process(file_path).decode('utf-8', errors='ignore')
        # print(text)
        for category, category_keywords in keywords.items():
            for keyword in category_keywords:

                # Use fuzzy matching to find all occurrences of the keyword in the text
                # for word in text.split(" "):

                score = fuzz.partial_ratio(keyword, text, score_cutoff=80)

                if score > 80:
                    category_counts[category] += 1
                # Increment the category count for each match

        # return max(category_counts, key=category_counts.get)
        # return category_counts
    except Exception as e:
        print(e)
        print("can't read")
        return False
