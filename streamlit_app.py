import streamlit as st
import json
import os

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="AI Outfit Stylist",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Demo data
DEMO_SUGGESTIONS = {
    "blue jeans": {
        "search_item_description": "Classic blue denim jeans - the ultimate wardrobe staple that pairs with virtually anything and transitions effortlessly from day to night.",
        "complete_outfits": [
            {
                "outfit_name": "Casual Cool",
                "description": "An effortlessly stylish everyday look that's perfect for running errands or grabbing coffee with friends.",
                "items": [
                    {"category": "tops", "item": "White Crew Neck T-Shirt", "details": "100% cotton, relaxed fit in crisp white", "why_it_works": "The classic white tee creates a clean, timeless contrast with blue denim"},
                    {"category": "shoes", "item": "White Leather Sneakers", "details": "Minimalist design, clean white leather", "why_it_works": "Keeps the look casual while adding a polished, fresh element"},
                    {"category": "accessories", "item": "Brown Leather Belt", "details": "Medium width, silver buckle", "why_it_works": "Adds a touch of sophistication and breaks up the blue-white palette"},
                    {"category": "outerwear", "item": "Denim Jacket (Light Wash)", "details": "Classic cut in a lighter shade than your jeans", "why_it_works": "Creates a Canadian tuxedo effect when done right with contrasting denim shades"}
                ],
                "styling_tips": "Cuff your jeans slightly to show off your sneakers and add visual interest. Tuck in the front of your t-shirt for a more intentional look."
            },
            {
                "outfit_name": "Smart Casual",
                "description": "Elevated denim styling perfect for a nice dinner or casual Friday at the office.",
                "items": [
                    {"category": "tops", "item": "Light Blue Oxford Shirt", "details": "Button-down collar, slim fit, cotton", "why_it_works": "The blue-on-blue creates a sophisticated tonal look"},
                    {"category": "shoes", "item": "Tan Suede Loafers", "details": "Penny loafer style in warm tan suede", "why_it_works": "Elevates the jeans while maintaining comfort and warmth in the color palette"},
                    {"category": "accessories", "item": "Leather Watch", "details": "Brown leather strap, classic dial", "why_it_works": "Adds a refined touch that signals attention to detail"},
                    {"category": "outerwear", "item": "Navy Blazer", "details": "Unstructured cotton blend, gold buttons", "why_it_works": "Instantly elevates any jeans outfit while staying comfortable"}
                ],
                "styling_tips": "Roll up your shirt sleeves once or twice for a relaxed vibe. Make sure your jeans are dark wash and well-fitted for this elevated look."
            },
            {
                "outfit_name": "Weekend Explorer",
                "description": "A rugged yet stylish outfit for outdoor adventures or weekend getaways.",
                "items": [
                    {"category": "tops", "item": "Flannel Shirt", "details": "Red and black buffalo check, brushed cotton", "why_it_works": "Adds texture and warmth while creating visual interest with the pattern"},
                    {"category": "shoes", "item": "Brown Leather Boots", "details": "Lace-up work boot style, Goodyear welted", "why_it_works": "Rugged durability that complements the casual, outdoorsy vibe"},
                    {"category": "accessories", "item": "Canvas Backpack", "details": "Waxed canvas in olive green", "why_it_works": "Functional and stylish, the earthy tone complements the warm flannel"},
                    {"category": "outerwear", "item": "Quilted Vest", "details": "Navy or olive, lightweight insulation", "why_it_works": "Adds warmth and layers without restricting movement"}
                ],
                "styling_tips": "Leave the flannel untucked and unbuttoned with a plain tee underneath. Cuff your jeans to show off your boots."
            }
        ],
        "color_palette": ["White", "Navy", "Tan/Camel", "Burgundy", "Forest Green", "Gray"],
        "avoid": ["Matching blue denim top (unless contrasting shades)", "Overly distressed pieces for formal settings", "Baggy fits that overwhelm your frame", "Clashing bold patterns"],
        "celebrity_inspiration": "Ryan Gosling - known for his effortless ability to dress up or down classic blue jeans with impeccable style",
        "pro_tip": "Invest in quality denim that fits perfectly. The right pair of jeans should hug your body without restricting movement, and the wash should be versatile enough to dress up or down."
    },
    "white sneakers": {
        "search_item_description": "Crisp white sneakers - the versatile footwear essential that adds a fresh, modern touch to any outfit.",
        "complete_outfits": [
            {
                "outfit_name": "Athleisure Chic",
                "description": "The perfect blend of comfort and style for the modern trendsetter.",
                "items": [
                    {"category": "tops", "item": "Oversized Gray Hoodie", "details": "Premium cotton blend, relaxed fit", "why_it_works": "Creates a cozy, effortless vibe that pairs perfectly with crisp white sneakers"},
                    {"category": "bottoms", "item": "Black Joggers", "details": "Tapered fit with ribbed cuffs", "why_it_works": "The tapered silhouette keeps things sleek while staying comfortable"},
                    {"category": "accessories", "item": "Black Baseball Cap", "details": "Minimalist design, adjustable strap", "why_it_works": "Adds a sporty edge that ties the athleisure look together"},
                    {"category": "outerwear", "item": "Black Bomber Jacket", "details": "Lightweight nylon, ribbed trim", "why_it_works": "Elevates the casual outfit while maintaining the sporty aesthetic"}
                ],
                "styling_tips": "Keep your sneakers pristine and clean for maximum impact. The contrast between black pieces and white sneakers creates a striking visual."
            },
            {
                "outfit_name": "Summer Fresh",
                "description": "A light, breezy look perfect for warm weather outings.",
                "items": [
                    {"category": "tops", "item": "Linen Camp Collar Shirt", "details": "Light blue, relaxed fit, short sleeve", "why_it_works": "The breathable fabric and relaxed cut scream effortless summer style"},
                    {"category": "bottoms", "item": "Khaki Chino Shorts", "details": "7-inch inseam, slim fit", "why_it_works": "Classic shorts that show off your white sneakers beautifully"},
                    {"category": "accessories", "item": "Woven Leather Belt", "details": "Braided brown leather", "why_it_works": "Adds texture and a touch of sophistication to the casual look"},
                    {"category": "accessories", "item": "Sunglasses", "details": "Classic wayfarer style, tortoise shell", "why_it_works": "Essential summer accessory that completes the polished casual vibe"}
                ],
                "styling_tips": "Go sockless or wear no-show socks for the cleanest look. A simple tuck of the shirt can elevate the entire outfit."
            },
            {
                "outfit_name": "Minimalist Monday",
                "description": "Clean lines and neutral tones for the modern minimalist.",
                "items": [
                    {"category": "tops", "item": "Black Fitted T-Shirt", "details": "Premium cotton, crew neck", "why_it_works": "The stark black-and-white contrast creates a bold, clean aesthetic"},
                    {"category": "bottoms", "item": "Dark Wash Slim Jeans", "details": "Slight stretch, no distressing", "why_it_works": "Dark denim grounds the outfit while keeping it versatile"},
                    {"category": "accessories", "item": "Minimalist Watch", "details": "White dial, black leather strap", "why_it_works": "Echoes the black-and-white theme with understated elegance"},
                    {"category": "outerwear", "item": "Camel Overcoat", "details": "Wool blend, single-breasted", "why_it_works": "Adds warmth and sophistication, the camel tone bridges black and white beautifully"}
                ],
                "styling_tips": "Less is more with this look. Let the quality of each piece speak for itself, and keep accessories minimal."
            }
        ],
        "color_palette": ["Black", "Navy", "Gray", "Beige", "Light Blue", "Olive"],
        "avoid": ["Overly busy patterns that compete with clean sneakers", "Worn or dirty sneakers - keep them pristine", "Too many bright colors at once", "Formal dress shoes with casual sneaker-style outfits"],
        "celebrity_inspiration": "Zendaya - masters the art of making white sneakers work with everything from casual to red carpet adjacent looks",
        "pro_tip": "Invest in a good sneaker cleaning kit and clean your white sneakers regularly. Nothing ruins an outfit faster than dingy white shoes. Consider having a 'going out' pair and an 'everyday' pair."
    },
    "leather jacket": {
        "search_item_description": "The iconic leather jacket - a timeless statement piece that instantly adds edge and sophistication to any outfit.",
        "complete_outfits": [
            {
                "outfit_name": "Rock & Roll Rebel",
                "description": "Channel your inner rockstar with this effortlessly cool ensemble.",
                "items": [
                    {"category": "tops", "item": "Vintage Band T-Shirt", "details": "Slightly worn-in, relaxed fit", "why_it_works": "Adds authentic rock vibes and personality to the leather jacket look"},
                    {"category": "bottoms", "item": "Black Skinny Jeans", "details": "Stretch denim, slight distressing", "why_it_works": "Creates a sleek silhouette that complements the jacket's edge"},
                    {"category": "shoes", "item": "Black Chelsea Boots", "details": "Leather, pointed toe, stacked heel", "why_it_works": "The perfect rock-inspired footwear that elongates the leg"},
                    {"category": "accessories", "item": "Silver Chain Necklace", "details": "Medium weight, simple design", "why_it_works": "Adds just the right amount of metal to complete the rocker aesthetic"}
                ],
                "styling_tips": "Leave the jacket unzipped for a casual, effortless vibe. Push up the sleeves slightly for added cool factor."
            },
            {
                "outfit_name": "Date Night Edge",
                "description": "Sophisticated with a hint of danger - perfect for making an impression.",
                "items": [
                    {"category": "tops", "item": "Black Silk Camisole", "details": "V-neck, delicate straps", "why_it_works": "The feminine silk balances the masculine leather for perfect contrast"},
                    {"category": "bottoms", "item": "High-Waisted Trousers", "details": "Wide leg, black crepe fabric", "why_it_works": "Elevates the look while maintaining the sleek color palette"},
                    {"category": "shoes", "item": "Strappy Heeled Sandals", "details": "Black leather, 3-inch heel", "why_it_works": "Adds elegance and height while staying in the leather family"},
                    {"category": "accessories", "item": "Gold Hoop Earrings", "details": "Medium size, polished finish", "why_it_works": "Warm gold tones soften the all-black look and add glamour"}
                ],
                "styling_tips": "Apply a bold red lip to add a pop of color. Keep the rest of your makeup minimal and let the outfit do the talking."
            },
            {
                "outfit_name": "Casual Sunday",
                "description": "Relaxed yet put-together for low-key weekend adventures.",
                "items": [
                    {"category": "tops", "item": "White Henley Shirt", "details": "Long sleeve, waffle knit", "why_it_works": "The textured white creates beautiful contrast with dark leather"},
                    {"category": "bottoms", "item": "Medium Wash Straight Jeans", "details": "Classic fit, no distressing", "why_it_works": "Keeps things casual while letting the jacket be the star"},
                    {"category": "shoes", "item": "White Leather Sneakers", "details": "Clean, minimalist design", "why_it_works": "Grounds the outfit in casual territory while staying polished"},
                    {"category": "accessories", "item": "Crossbody Bag", "details": "Tan leather, simple design", "why_it_works": "Adds functionality and a warm tone to break up the cool palette"}
                ],
                "styling_tips": "Cuff your jeans once to show off your sneakers. Add a beanie in cooler weather for extra style points."
            }
        ],
        "color_palette": ["Black", "White", "Burgundy", "Charcoal", "Tan", "Dark Green"],
        "avoid": ["Too many competing leather pieces", "Overly formal items that clash with the jacket's edge", "Bright neon colors that fight the leather's vibe", "Baggy silhouettes that overwhelm the jacket's structure"],
        "celebrity_inspiration": "Hailey Bieber - effortlessly styles leather jackets from street style to elevated casual with impeccable taste",
        "pro_tip": "Condition your leather jacket regularly to keep it supple and prevent cracking. A well-maintained leather jacket actually looks better with age and develops a beautiful patina over time."
    }
}

# Custom CSS for stunning UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Header */
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        border-radius: 24px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    
    .main-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fff 0%, #a78bfa 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: rgba(255,255,255,0.7);
        font-weight: 300;
    }
    
    /* Search Container */
    .search-section {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
    }
    
    .search-label {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: rgba(255,255,255,0.9);
        margin-bottom: 1rem;
        display: block;
    }
    
    /* Results Header */
    .results-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f472b6 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .results-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.5;
    }
    
    .results-header h2 {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: white;
        margin: 0;
        position: relative;
        z-index: 1;
    }
    
    .results-header p {
        font-family: 'Inter', sans-serif;
        color: rgba(255,255,255,0.9);
        margin: 0.5rem 0 0 0;
        position: relative;
        z-index: 1;
    }
    
    /* Outfit Card */
    .outfit-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .outfit-card:hover {
        background: rgba(255,255,255,0.08);
        border-color: rgba(167, 139, 250, 0.3);
        transform: translateY(-2px);
    }
    
    .outfit-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        color: #a78bfa;
        margin-bottom: 0.5rem;
    }
    
    .outfit-description {
        font-family: 'Inter', sans-serif;
        color: rgba(255,255,255,0.7);
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Item Card */
    .item-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.2rem;
        height: 100%;
        transition: all 0.2s ease;
    }
    
    .item-card:hover {
        background: rgba(255,255,255,0.06);
        border-color: rgba(244, 114, 182, 0.3);
    }
    
    .category-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-family: 'Inter', sans-serif;
    }
    
    .badge-tops { background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white; }
    .badge-bottoms { background: linear-gradient(135deg, #8b5cf6, #6d28d9); color: white; }
    .badge-shoes { background: linear-gradient(135deg, #f59e0b, #d97706); color: white; }
    .badge-accessories { background: linear-gradient(135deg, #10b981, #059669); color: white; }
    .badge-outerwear { background: linear-gradient(135deg, #ec4899, #db2777); color: white; }
    
    .item-name {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: white;
        margin: 0.8rem 0 0.4rem 0;
    }
    
    .item-details {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: rgba(255,255,255,0.6);
        margin-bottom: 0.5rem;
    }
    
    .item-why {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: #a78bfa;
        font-style: italic;
    }
    
    /* Styling Tip */
    .styling-tip {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%);
        border: 1px solid rgba(251, 191, 36, 0.2);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-top: 1rem;
    }
    
    .styling-tip-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        color: #fbbf24;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .styling-tip-text {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: rgba(255,255,255,0.8);
        margin-top: 0.3rem;
    }
    
    /* Color Palette */
    .color-section {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .section-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
        color: rgba(255,255,255,0.5);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 1rem;
    }
    
    .color-chip {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: rgba(255,255,255,0.1);
        border-radius: 25px;
        margin: 0.25rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Avoid Section */
    .avoid-section {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
    }
    
    .avoid-item {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: rgba(255,255,255,0.8);
        padding: 0.3rem 0;
    }
    
    /* Inspiration Section */
    .inspiration-section {
        background: linear-gradient(135deg, rgba(167, 139, 250, 0.1) 0%, rgba(244, 114, 182, 0.1) 100%);
        border: 1px solid rgba(167, 139, 250, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
    }
    
    /* Pro Tip */
    .pro-tip {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .pro-tip-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
        color: #10b981;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .pro-tip-text {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
        line-height: 1.6;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    
    .footer p {
        font-family: 'Inter', sans-serif;
        color: rgba(255,255,255,0.4);
        font-size: 0.9rem;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stTextInput label {
        color: rgba(255,255,255,0.8) !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-radius: 30px !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 30px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.75rem 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #a78bfa !important;
        box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.2) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.4) !important;
    }
    
    /* Select Box Styling */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        color: white !important;
    }
    
    /* Quick Search Buttons */
    .quick-search-btn {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        margin: 0.25rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: rgba(255,255,255,0.8);
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .quick-search-btn:hover {
        background: rgba(167, 139, 250, 0.2);
        border-color: rgba(167, 139, 250, 0.4);
    }
</style>
""", unsafe_allow_html=True)


def get_demo_suggestions(item: str) -> dict:
    """Return demo suggestions for common items."""
    item_lower = item.lower().strip()
    
    # Check for matches
    for key in DEMO_SUGGESTIONS:
        if key in item_lower or item_lower in key:
            return DEMO_SUGGESTIONS[key]
    
    # Check for partial matches
    if "jean" in item_lower or "denim" in item_lower:
        return DEMO_SUGGESTIONS["blue jeans"]
    if "sneaker" in item_lower or "trainer" in item_lower:
        return DEMO_SUGGESTIONS["white sneakers"]
    if "leather" in item_lower or "jacket" in item_lower:
        return DEMO_SUGGESTIONS["leather jacket"]
    
    # Return a generic suggestion
    return DEMO_SUGGESTIONS["blue jeans"]


def get_outfit_suggestions(item: str, style: str, occasion: str, season: str, api_key: str = None):
    """Generate outfit suggestions using OpenAI API or demo data."""
    
    if not api_key:
        return get_demo_suggestions(item)
    
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        
        prompt = f"""You are an expert fashion stylist. A customer searched for: "{item}"
Style: {style}, Occasion: {occasion}, Season: {season}

Provide outfit suggestions in this JSON format:
{{
    "search_item_description": "Brief stylish description",
    "complete_outfits": [
        {{
            "outfit_name": "Creative name",
            "description": "Overall look description",
            "items": [
                {{"category": "tops/bottoms/shoes/accessories/outerwear", "item": "Item name", "details": "Details", "why_it_works": "Why it pairs well"}}
            ],
            "styling_tips": "How to style"
        }}
    ],
    "color_palette": ["Colors that complement"],
    "avoid": ["Things to avoid"],
    "celebrity_inspiration": "Style icon",
    "pro_tip": "Expert tip"
}}

Provide 3 different outfits. Respond with valid JSON only."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert fashion stylist. Respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        
        return json.loads(content.strip())
    except Exception as e:
        st.warning(f"Using demo data. API error: {str(e)}")
        return get_demo_suggestions(item)


def display_item_card(item: dict):
    """Display a single item card."""
    category = item['category'].lower()
    badge_class = f"badge-{category}" if category in ['tops', 'bottoms', 'shoes', 'accessories', 'outerwear'] else "badge-accessories"
    
    icons = {"tops": "👕", "bottoms": "👖", "shoes": "👟", "accessories": "👜", "outerwear": "🧥"}
    icon = icons.get(category, "✨")
    
    st.markdown(f"""
    <div class="item-card">
        <span class="category-badge {badge_class}">{icon} {item['category']}</span>
        <div class="item-name">{item['item']}</div>
        <div class="item-details">{item['details']}</div>
        <div class="item-why">💡 {item['why_it_works']}</div>
    </div>
    """, unsafe_allow_html=True)


def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>👗 AI Outfit Stylist</h1>
        <p>Your personal AI-powered fashion advisor ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        api_key = st.text_input(
            "OpenAI API Key (optional)",
            type="password",
            help="Enter your OpenAI API key for live AI suggestions, or leave blank for demo mode",
            placeholder="sk-..."
        )
        
        if not api_key:
            st.info("🎭 Running in demo mode with sample data")
        
        st.markdown("---")
        st.markdown("### 🎨 Style Preferences")
        
        style = st.selectbox(
            "Your Style",
            ["Classic & Timeless", "Trendy & Fashion-Forward", "Casual & Relaxed", 
             "Minimalist & Clean", "Bold & Eclectic", "Bohemian & Free-Spirited"]
        )
        
        occasion = st.selectbox(
            "Occasion",
            ["Everyday Casual", "Work/Office", "Date Night", "Weekend Brunch",
             "Special Event", "Vacation", "Night Out"]
        )
        
        season = st.selectbox(
            "Season",
            ["Year-Round", "Spring", "Summer", "Fall/Autumn", "Winter"]
        )
        
        st.markdown("---")
        st.markdown("""
        ### 💡 Try Searching For
        - Blue jeans
        - White sneakers
        - Leather jacket
        - Black dress
        - Blazer
        """)
    
    # Main search area
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<p class="search-label">🔍 What clothing item are you looking for?</p>', unsafe_allow_html=True)
        search_item = st.text_input(
            "",
            placeholder="e.g., blue jeans, white sneakers, leather jacket...",
            label_visibility="collapsed",
            key="search_input"
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            search_button = st.button("✨ Get Outfit Ideas", use_container_width=True)
    
    # Process search
    if search_button and search_item:
        with st.spinner("✨ Our AI stylist is curating the perfect outfits for you..."):
            suggestions = get_outfit_suggestions(search_item, style, occasion, season, api_key)
        
        if suggestions:
            # Results header
            st.markdown(f"""
            <div class="results-header">
                <h2>🛍️ {search_item.title()}</h2>
                <p>{suggestions.get('search_item_description', '')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Color palette
            if 'color_palette' in suggestions:
                st.markdown("""<div class="color-section">
                    <div class="section-title">🎨 Complementary Colors</div>""", unsafe_allow_html=True)
                colors_html = "".join([f'<span class="color-chip">{c}</span>' for c in suggestions['color_palette']])
                st.markdown(f"{colors_html}</div>", unsafe_allow_html=True)
            
            # Complete outfits
            st.markdown("### 👔 Complete Outfit Ideas")
            
            for i, outfit in enumerate(suggestions.get('complete_outfits', [])):
                with st.expander(f"✨ Look {i+1}: {outfit['outfit_name']}", expanded=(i==0)):
                    st.markdown(f"""
                    <div class="outfit-card">
                        <div class="outfit-description">{outfit['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display items in grid
                    cols = st.columns(min(len(outfit['items']), 4))
                    for j, item in enumerate(outfit['items']):
                        with cols[j % len(cols)]:
                            display_item_card(item)
                    
                    # Styling tip
                    st.markdown(f"""
                    <div class="styling-tip">
                        <div class="styling-tip-label">👠 Styling Tip</div>
                        <div class="styling-tip-text">{outfit['styling_tips']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Bottom sections
            col1, col2 = st.columns(2)
            
            with col1:
                if 'avoid' in suggestions:
                    st.markdown("""<div class="avoid-section">
                        <div class="section-title">🚫 What to Avoid</div>""", unsafe_allow_html=True)
                    for item in suggestions['avoid']:
                        st.markdown(f'<div class="avoid-item">• {item}</div>', unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                if 'celebrity_inspiration' in suggestions:
                    st.markdown(f"""<div class="inspiration-section">
                        <div class="section-title">🌟 Style Inspiration</div>
                        <p style="color: white; font-family: 'Inter', sans-serif;">{suggestions['celebrity_inspiration']}</p>
                    </div>""", unsafe_allow_html=True)
            
            # Pro tip
            if 'pro_tip' in suggestions:
                st.markdown(f"""
                <div class="pro-tip">
                    <div class="pro-tip-label">💎 Pro Stylist Tip</div>
                    <div class="pro-tip-text">{suggestions['pro_tip']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    elif search_button and not search_item:
        st.warning("Please enter a clothing item to search for!")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>Made with ❤️ by AI Outfit Stylist | Powered by OpenAI</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
