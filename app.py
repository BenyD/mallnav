from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Update database path to use absolute path
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'malls.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Mall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    parking_info = db.Column(db.String(200), nullable=True)
    food_court_location = db.Column(db.String(200), nullable=True)
    food_court_hours = db.Column(db.String(100), nullable=True)
    contact_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    shops = db.relationship('Shop', backref='mall', lazy=True)

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    directions = db.Column(db.String(500), nullable=False)
    opening_hours = db.Column(db.String(100), nullable=True)
    contact = db.Column(db.String(50), nullable=True)
    special_offers = db.Column(db.String(500), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    mall_id = db.Column(db.Integer, db.ForeignKey('mall.id'), nullable=False)

# Routes
@app.route('/')
def index():
    try:
        malls = Mall.query.all()
        logger.info(f"Found {len(malls)} malls")
        for mall in malls:
            shops = Shop.query.filter_by(mall_id=mall.id).all()
            logger.info(f"Mall {mall.name} has {len(shops)} shops")
        return render_template('index.html', malls=malls)
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        return str(e), 500

@app.route('/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    floor = request.args.get('floor', '')
    
    # Start with all shops
    shops_query = Shop.query
    
    # Apply filters
    if query:
        shops_query = shops_query.filter(Shop.name.ilike(f'%{query}%'))
    if category:
        shops_query = shops_query.filter_by(category=category)
    if floor:
        shops_query = shops_query.filter_by(floor=int(floor))
    
    shops = shops_query.all()
    return render_template('search_results.html', shops=shops, query=query, category=category, floor=floor)

@app.route('/mall/<int:mall_id>')
def mall_shops(mall_id):
    try:
        mall = Mall.query.get_or_404(mall_id)
        shops = Shop.query.filter_by(mall_id=mall_id).all()
        categories = db.session.query(Shop.category).distinct().all()
        categories = [cat[0] for cat in categories]
        logger.info(f"Found {len(shops)} shops for mall {mall.name}")
        return render_template('mall.html', mall=mall, shops=shops, categories=categories)
    except Exception as e:
        logger.error(f"Error in mall_shops route: {str(e)}")
        return str(e), 500

@app.route('/shop/<int:shop_id>')
def shop_details(shop_id):
    try:
        shop = Shop.query.get_or_404(shop_id)
        return render_template('shop.html', shop=shop)
    except Exception as e:
        logger.error(f"Error in shop_details route: {str(e)}")
        return str(e), 500

# Initialize database with sample data
def init_db():
    with app.app_context():
        logger.info("Creating database tables...")
        db.create_all()
        
        # Check if data already exists
        mall_count = Mall.query.count()
        logger.info(f"Current mall count: {mall_count}")
        shop_count = Shop.query.count()
        logger.info(f"Current shop count: {shop_count}")
        
        if mall_count == 0 and shop_count == 0:
            logger.info("Initializing database with sample data...")
            try:
                # Create malls with additional information
                malls = [
                    Mall(name="Vivira Mall", 
                         address="123 Mount Road, Chennai",
                         parking_info="Parking available in basement and rooftop"),
                    Mall(name="BSR Mall", 
                         address="456 Anna Salai, Chennai",
                         parking_info="Multi-level parking available"),
                    Mall(name="Express Avenue Mall", 
                         address="789 Express Avenue, Chennai",
                         parking_info="Underground parking with 1000+ slots"),
                    Mall(name="Marina Mall", 
                         address="321 Marina Beach Road, Chennai",
                         parking_info="Valet parking available"),
                    Mall(name="Phoenix Mall", 
                         address="654 Velachery Main Road, Chennai",
                         parking_info="Multi-level parking with EV charging")
                ]
                
                for mall in malls:
                    db.session.add(mall)
                
                logger.info("Added malls to session")
                db.session.commit()
                logger.info("Committed malls to database")
                
                # Create shops for each mall with additional information
                all_shops = []
                
                # Create shops for Vivira Mall (mall_id=1)
                vivira_shops = [
                    Shop(name="Zara", floor=2, category="Fashion", 
                         directions="Take the main escalator to the second floor. The store is on your right after the food court.",
                         opening_hours="10:00 AM - 10:00 PM",
                         contact="044-12345678",
                         mall_id=1),
                    Shop(name="H&M", floor=1, category="Fashion",
                         directions="Enter through the main entrance and take the first left. The store is on your right.",
                         mall_id=1),
                    Shop(name="Starbucks", floor=3, category="Food & Beverage",
                         directions="Take the elevator to the third floor. The store is near the cinema entrance.",
                         mall_id=1),
                    Shop(name="Lifestyle", floor=2, category="Department Store",
                         directions="Take the escalator to the second floor. The store entrance is directly in front of you.",
                         mall_id=1),
                    Shop(name="Pantaloons", floor=1, category="Fashion",
                         directions="From the main entrance, walk straight ahead. The store is at the end of the corridor.",
                         mall_id=1),
                    Shop(name="Domino's Pizza", floor=3, category="Food & Beverage",
                         directions="Take the elevator to the third floor. Turn right and walk to the food court.",
                         mall_id=1),
                    Shop(name="Crossword", floor=2, category="Books & Stationery",
                         directions="Take the escalator to the second floor, turn left. The store is next to the restrooms.",
                         mall_id=1),
                    Shop(name="Samsung", floor=1, category="Electronics",
                         directions="Enter through the main entrance and take the second right. The store is opposite to H&M.",
                         mall_id=1),
                    Shop(name="MAC Cosmetics", floor=2, category="Beauty",
                         directions="On the second floor, next to Zara. Take the main escalator and turn right.",
                         mall_id=1),
                    Shop(name="PVR Cinemas", floor=3, category="Entertainment",
                         directions="Take the elevator to the third floor. The cinema entrance is straight ahead.",
                         mall_id=1)
                ]
                all_shops.extend(vivira_shops)
                
                # Create shops for BSR Mall (mall_id=2)
                bsr_shops = [
                    Shop(name="Puma", floor=1, category="Sports",
                         directions="Enter through the main entrance and take the first right. The store is on your left.",
                         mall_id=2),
                    Shop(name="McDonald's", floor=2, category="Food & Beverage",
                         directions="Take the escalator to the second floor. The restaurant is in the food court area.",
                         mall_id=2),
                    Shop(name="Shoppers Stop", floor=2, category="Department Store",
                         directions="Take the escalator to the second floor. The store occupies the entire right wing.",
                         mall_id=2),
                    Shop(name="Marks & Spencer", floor=1, category="Fashion",
                         directions="From the main entrance, take the left corridor. The store is at the end.",
                         mall_id=2),
                    Shop(name="Reliance Digital", floor=3, category="Electronics",
                         directions="Take the elevator to the third floor. The store is opposite to the elevator.",
                         mall_id=2),
                    Shop(name="KFC", floor=2, category="Food & Beverage",
                         directions="Second floor food court, next to McDonald's.",
                         mall_id=2),
                    Shop(name="Westside", floor=1, category="Fashion",
                         directions="Ground floor, right wing. Follow the signs from the main entrance.",
                         mall_id=2),
                    Shop(name="Sephora", floor=2, category="Beauty",
                         directions="Second floor, near the central atrium. Take the main escalator and turn left.",
                         mall_id=2),
                    Shop(name="Hamleys", floor=3, category="Toys",
                         directions="Third floor, next to the play area. Take the panoramic elevator.",
                         mall_id=2),
                    Shop(name="Timezone", floor=3, category="Entertainment",
                         directions="Third floor, follow the gaming sounds. Next to the food court.",
                         mall_id=2)
                ]
                all_shops.extend(bsr_shops)
                
                # Create shops for Express Avenue Mall (mall_id=3)
                express_avenue_shops = [
                    Shop(name="Apple Store", floor=1, category="Electronics",
                         directions="Ground floor main atrium. Can't miss the iconic Apple logo.",
                         mall_id=3),
                    Shop(name="Forever 21", floor=2, category="Fashion",
                         directions="Second floor, take the central escalator and turn right.",
                         mall_id=3),
                    Shop(name="Burger King", floor=3, category="Food & Beverage",
                         directions="Third floor food court, first outlet on the left.",
                         mall_id=3),
                    Shop(name="Croma", floor=2, category="Electronics",
                         directions="Second floor, east wing. Follow the digital displays.",
                         mall_id=3),
                    Shop(name="Nike", floor=1, category="Sports",
                         directions="Ground floor, sports section. Near the south entrance.",
                         mall_id=3),
                    Shop(name="Pizza Hut", floor=3, category="Food & Beverage",
                         directions="Food court area, opposite to Burger King.",
                         mall_id=3),
                    Shop(name="Miniso", floor=2, category="Lifestyle",
                         directions="Second floor, near the washrooms. Look for the red logo.",
                         mall_id=3),
                    Shop(name="Chili's", floor=3, category="Food & Beverage",
                         directions="Third floor, separate dining area outside food court.",
                         mall_id=3),
                    Shop(name="Max Fashion", floor=1, category="Fashion",
                         directions="Ground floor, west wing. Large store front visible from entrance.",
                         mall_id=3),
                    Shop(name="INOX", floor=4, category="Entertainment",
                         directions="Top floor, dedicated elevator access available.",
                         mall_id=3)
                ]
                all_shops.extend(express_avenue_shops)
                
                # Create shops for Marina Mall (mall_id=4)
                marina_shops = [
                    Shop(name="Adidas", floor=1, category="Sports",
                         directions="Ground floor, main sports section near entrance.",
                         mall_id=4),
                    Shop(name="Subway", floor=2, category="Food & Beverage",
                         directions="Food court area, first shop on entering.",
                         mall_id=4),
                    Shop(name="Big Bazaar", floor=3, category="Department Store",
                         directions="Entire third floor, access via main elevator.",
                         mall_id=4),
                    Shop(name="Bata", floor=1, category="Footwear",
                         directions="Ground floor, opposite to Adidas.",
                         mall_id=4),
                    Shop(name="Baskin Robbins", floor=2, category="Food & Beverage",
                         directions="Second floor, ice cream corner near play area.",
                         mall_id=4),
                    Shop(name="Titan", floor=1, category="Accessories",
                         directions="Ground floor, luxury section near escalator.",
                         mall_id=4),
                    Shop(name="FabIndia", floor=2, category="Fashion",
                         directions="Second floor, ethnic wear section.",
                         mall_id=4),
                    Shop(name="Archies", floor=1, category="Gifts",
                         directions="Ground floor, near the central fountain.",
                         mall_id=4),
                    Shop(name="Café Coffee Day", floor=2, category="Food & Beverage",
                         directions="Second floor, separate seating area with sea view.",
                         mall_id=4),
                    Shop(name="Game Zone", floor=3, category="Entertainment",
                         directions="Third floor, next to Big Bazaar entrance.",
                         mall_id=4)
                ]
                all_shops.extend(marina_shops)
                
                # Create shops for Phoenix Mall (mall_id=5)
                phoenix_shops = [
                    Shop(name="Under Armour", floor=1, category="Sports",
                         directions="Ground floor, premium sports section.",
                         mall_id=5),
                    Shop(name="Taco Bell", floor=3, category="Food & Beverage",
                         directions="Food court, Mexican section.",
                         mall_id=5),
                    Shop(name="Central", floor=2, category="Department Store",
                         directions="Second floor, main wing. Multiple entries available.",
                         mall_id=5),
                    Shop(name="Rolex Boutique", floor=1, category="Luxury",
                         directions="Ground floor, luxury wing with dedicated entrance.",
                         mall_id=5),
                    Shop(name="Bath & Body Works", floor=2, category="Beauty",
                         directions="Second floor, fragrance section near escalator.",
                         mall_id=5),
                    Shop(name="Dyson", floor=1, category="Electronics",
                         directions="Ground floor, premium electronics section.",
                         mall_id=5),
                    Shop(name="Nykaa Luxe", floor=2, category="Beauty",
                         directions="Second floor, opposite to Bath & Body Works.",
                         mall_id=5),
                    Shop(name="Theobroma", floor=3, category="Food & Beverage",
                         directions="Third floor, dessert section in food court.",
                         mall_id=5),
                    Shop(name="Tommy Hilfiger", floor=1, category="Fashion",
                         directions="Ground floor, international brands section.",
                         mall_id=5),
                    Shop(name="AGS Cinemas", floor=4, category="Entertainment",
                         directions="Top floor, exclusive elevator access.",
                         mall_id=5)
                ]
                all_shops.extend(phoenix_shops)
                
                # Add all shops to session and commit
                for shop in all_shops:
                    db.session.add(shop)
                
                logger.info("Added all shops to session")
                db.session.commit()
                logger.info("Committed all shops to database")
                
            except Exception as e:
                logger.error(f"Error initializing database: {str(e)}")
                db.session.rollback()
                raise
        else:
            logger.info("Database already contains data")

if __name__ == '__main__':
    logger.info("Starting application...")
    init_db()
    app.run(debug=True)
