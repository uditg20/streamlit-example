#!/usr/bin/env python3
from flask import Flask, render_template_string, request, jsonify
import json
import os

app = Flask(__name__)

# Demo data
DEMO_DATA = {
    "blue jeans": {
        "description": "Classic blue denim jeans - the ultimate wardrobe staple that pairs with virtually anything.",
        "colors": ["White", "Navy", "Tan", "Burgundy", "Forest Green", "Gray"],
        "outfits": [
            {
                "name": "Casual Cool",
                "desc": "Effortlessly stylish for everyday wear",
                "items": [
                    {"cat": "Top", "icon": "👕", "name": "White Crew Neck T-Shirt", "detail": "100% cotton, relaxed fit", "why": "Clean contrast with blue denim"},
                    {"cat": "Shoes", "icon": "👟", "name": "White Leather Sneakers", "detail": "Minimalist design", "why": "Keeps it casual yet polished"},
                    {"cat": "Layer", "icon": "🧥", "name": "Denim Jacket (Light Wash)", "detail": "Contrasting shade", "why": "Canadian tuxedo done right"},
                    {"cat": "Accessory", "icon": "👜", "name": "Brown Leather Belt", "detail": "Silver buckle", "why": "Adds sophistication"}
                ],
                "tip": "Cuff your jeans to show off sneakers. Tuck in the front of your tee."
            },
            {
                "name": "Smart Casual",
                "desc": "Elevated look for dinner or casual office",
                "items": [
                    {"cat": "Top", "icon": "👔", "name": "Light Blue Oxford Shirt", "detail": "Button-down, slim fit", "why": "Blue-on-blue tonal sophistication"},
                    {"cat": "Shoes", "icon": "👞", "name": "Tan Suede Loafers", "detail": "Penny loafer style", "why": "Elevates while staying comfortable"},
                    {"cat": "Layer", "icon": "🧥", "name": "Navy Blazer", "detail": "Unstructured cotton blend", "why": "Instantly elevates any jeans"},
                    {"cat": "Accessory", "icon": "⌚", "name": "Leather Watch", "detail": "Brown strap, classic dial", "why": "Refined attention to detail"}
                ],
                "tip": "Roll up sleeves for a relaxed vibe. Stick to dark wash jeans."
            },
            {
                "name": "Weekend Explorer",
                "desc": "Rugged yet stylish for outdoor adventures",
                "items": [
                    {"cat": "Top", "icon": "👕", "name": "Flannel Shirt", "detail": "Red & black buffalo check", "why": "Texture and warmth with visual interest"},
                    {"cat": "Shoes", "icon": "🥾", "name": "Brown Leather Boots", "detail": "Lace-up work boot style", "why": "Rugged durability"},
                    {"cat": "Layer", "icon": "🧥", "name": "Quilted Vest", "detail": "Navy or olive", "why": "Warmth without bulk"},
                    {"cat": "Accessory", "icon": "🎒", "name": "Canvas Backpack", "detail": "Waxed canvas, olive", "why": "Functional and stylish"}
                ],
                "tip": "Leave flannel unbuttoned with a plain tee underneath. Cuff jeans to show boots."
            }
        ],
        "avoid": ["Matching blue denim top", "Overly distressed for formal settings", "Baggy fits", "Clashing bold patterns"],
        "celeb": "Ryan Gosling - effortless denim style master",
        "protip": "Invest in quality denim that fits perfectly. The right jeans should hug without restricting."
    },
    "white sneakers": {
        "description": "Crisp white sneakers - versatile footwear that adds a fresh, modern touch to any outfit.",
        "colors": ["Black", "Navy", "Gray", "Beige", "Light Blue", "Olive"],
        "outfits": [
            {
                "name": "Athleisure Chic",
                "desc": "Perfect blend of comfort and style",
                "items": [
                    {"cat": "Top", "icon": "👕", "name": "Oversized Gray Hoodie", "detail": "Premium cotton blend", "why": "Cozy, effortless vibe"},
                    {"cat": "Bottom", "icon": "👖", "name": "Black Joggers", "detail": "Tapered fit, ribbed cuffs", "why": "Sleek yet comfortable"},
                    {"cat": "Layer", "icon": "🧥", "name": "Black Bomber Jacket", "detail": "Lightweight nylon", "why": "Elevates the sporty aesthetic"},
                    {"cat": "Accessory", "icon": "🧢", "name": "Black Baseball Cap", "detail": "Minimalist design", "why": "Ties the sporty look together"}
                ],
                "tip": "Keep sneakers pristine. Black + white contrast creates striking visual."
            },
            {
                "name": "Summer Fresh",
                "desc": "Light, breezy look for warm weather",
                "items": [
                    {"cat": "Top", "icon": "👕", "name": "Linen Camp Collar Shirt", "detail": "Light blue, short sleeve", "why": "Breathable summer style"},
                    {"cat": "Bottom", "icon": "🩳", "name": "Khaki Chino Shorts", "detail": "7-inch inseam, slim fit", "why": "Shows off sneakers beautifully"},
                    {"cat": "Accessory", "icon": "🕶️", "name": "Wayfarer Sunglasses", "detail": "Tortoise shell", "why": "Essential summer accessory"},
                    {"cat": "Accessory", "icon": "👜", "name": "Woven Leather Belt", "detail": "Braided brown leather", "why": "Adds texture and sophistication"}
                ],
                "tip": "Go sockless or wear no-show socks. Try a simple front tuck."
            },
            {
                "name": "Minimalist Monday",
                "desc": "Clean lines and neutral tones",
                "items": [
                    {"cat": "Top", "icon": "👕", "name": "Black Fitted T-Shirt", "detail": "Premium cotton, crew neck", "why": "Bold black-white contrast"},
                    {"cat": "Bottom", "icon": "👖", "name": "Dark Wash Slim Jeans", "detail": "No distressing", "why": "Grounds the outfit"},
                    {"cat": "Layer", "icon": "🧥", "name": "Camel Overcoat", "detail": "Wool blend", "why": "Bridges black and white beautifully"},
                    {"cat": "Accessory", "icon": "⌚", "name": "Minimalist Watch", "detail": "White dial, black strap", "why": "Echoes the black-white theme"}
                ],
                "tip": "Less is more. Let quality pieces speak for themselves."
            }
        ],
        "avoid": ["Overly busy patterns", "Dirty/worn sneakers", "Too many bright colors", "Formal shoes vibes"],
        "celeb": "Zendaya - makes white sneakers work with everything",
        "protip": "Get a sneaker cleaning kit. Keep a 'going out' pair and an 'everyday' pair."
    },
    "leather jacket": {
        "description": "The iconic leather jacket - a timeless statement piece that instantly adds edge and sophistication.",
        "colors": ["Black", "White", "Burgundy", "Charcoal", "Tan", "Dark Green"],
        "outfits": [
            {
                "name": "Rock & Roll Rebel",
                "desc": "Channel your inner rockstar",
                "items": [
                    {"cat": "Top", "icon": "👕", "name": "Vintage Band T-Shirt", "detail": "Slightly worn-in", "why": "Authentic rock vibes"},
                    {"cat": "Bottom", "icon": "👖", "name": "Black Skinny Jeans", "detail": "Slight distressing", "why": "Sleek silhouette with edge"},
                    {"cat": "Shoes", "icon": "👢", "name": "Black Chelsea Boots", "detail": "Pointed toe, stacked heel", "why": "Perfect rocker footwear"},
                    {"cat": "Accessory", "icon": "📿", "name": "Silver Chain Necklace", "detail": "Medium weight", "why": "Right amount of metal"}
                ],
                "tip": "Leave jacket unzipped. Push up sleeves for added cool factor."
            },
            {
                "name": "Date Night Edge",
                "desc": "Sophisticated with a hint of danger",
                "items": [
                    {"cat": "Top", "icon": "👚", "name": "Black Silk Camisole", "detail": "V-neck, delicate straps", "why": "Feminine balance to masculine leather"},
                    {"cat": "Bottom", "icon": "👖", "name": "High-Waisted Trousers", "detail": "Wide leg, black crepe", "why": "Elevates while staying sleek"},
                    {"cat": "Shoes", "icon": "👠", "name": "Strappy Heeled Sandals", "detail": "Black leather, 3-inch", "why": "Adds elegance in the leather family"},
                    {"cat": "Accessory", "icon": "💍", "name": "Gold Hoop Earrings", "detail": "Medium, polished", "why": "Warm gold softens all-black"}
                ],
                "tip": "Bold red lip adds a pop of color. Keep makeup minimal otherwise."
            },
            {
                "name": "Casual Sunday",
                "desc": "Relaxed yet put-together",
                "items": [
                    {"cat": "Top", "icon": "👕", "name": "White Henley Shirt", "detail": "Long sleeve, waffle knit", "why": "Textured white contrasts dark leather"},
                    {"cat": "Bottom", "icon": "👖", "name": "Medium Wash Straight Jeans", "detail": "Classic fit", "why": "Casual, lets jacket be the star"},
                    {"cat": "Shoes", "icon": "👟", "name": "White Leather Sneakers", "detail": "Clean, minimalist", "why": "Grounds in casual territory"},
                    {"cat": "Accessory", "icon": "👜", "name": "Tan Crossbody Bag", "detail": "Simple leather", "why": "Warm tone breaks cool palette"}
                ],
                "tip": "Cuff jeans once to show sneakers. Add a beanie in cooler weather."
            }
        ],
        "avoid": ["Too many leather pieces", "Overly formal items", "Bright neon colors", "Baggy silhouettes"],
        "celeb": "Hailey Bieber - effortless leather jacket styling",
        "protip": "Condition leather regularly. A well-maintained jacket develops beautiful patina over time."
    }
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Outfit Stylist</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
            min-height: 100vh;
            color: white;
        }
        
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
        
        /* Header */
        .header {
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
            border-radius: 24px;
            margin-bottom: 2rem;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .header h1 {
            font-family: 'Playfair Display', serif;
            font-size: 3rem;
            background: linear-gradient(135deg, #fff 0%, #a78bfa 50%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        
        .header p { color: rgba(255,255,255,0.7); font-size: 1.1rem; }
        
        /* Search */
        .search-box {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .search-box label {
            display: block;
            margin-bottom: 1rem;
            font-size: 1.1rem;
            color: rgba(255,255,255,0.9);
        }
        
        .search-input {
            width: 100%;
            max-width: 500px;
            padding: 1rem 1.5rem;
            font-size: 1.1rem;
            border: 2px solid rgba(255,255,255,0.2);
            border-radius: 50px;
            background: rgba(255,255,255,0.05);
            color: white;
            outline: none;
            transition: all 0.3s;
        }
        
        .search-input:focus {
            border-color: #a78bfa;
            box-shadow: 0 0 20px rgba(167, 139, 250, 0.3);
        }
        
        .search-input::placeholder { color: rgba(255,255,255,0.4); }
        
        .search-btn {
            margin-top: 1rem;
            padding: 1rem 3rem;
            font-size: 1.1rem;
            font-weight: 600;
            border: none;
            border-radius: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
        }
        
        .search-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 30px rgba(102, 126, 234, 0.6);
        }
        
        /* Quick picks */
        .quick-picks {
            margin-top: 1.5rem;
        }
        
        .quick-picks span { color: rgba(255,255,255,0.5); margin-right: 0.5rem; }
        
        .quick-btn {
            padding: 0.5rem 1rem;
            margin: 0.25rem;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 20px;
            background: rgba(255,255,255,0.05);
            color: rgba(255,255,255,0.8);
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .quick-btn:hover {
            background: rgba(167, 139, 250, 0.2);
            border-color: rgba(167, 139, 250, 0.4);
        }
        
        /* Results */
        .results { display: none; }
        .results.active { display: block; }
        
        .results-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f472b6 100%);
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
        }
        
        .results-header h2 {
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
        }
        
        .results-header p {
            margin-top: 0.5rem;
            opacity: 0.9;
        }
        
        /* Colors */
        .colors-section {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .section-label {
            font-size: 0.75rem;
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
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 25px;
            margin: 0.25rem;
            font-size: 0.9rem;
        }
        
        /* Outfit Cards */
        .outfit-card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: all 0.3s;
        }
        
        .outfit-card:hover {
            background: rgba(255,255,255,0.08);
            border-color: rgba(167, 139, 250, 0.3);
        }
        
        .outfit-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
        }
        
        .outfit-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.4rem;
            color: #a78bfa;
        }
        
        .outfit-desc {
            color: rgba(255,255,255,0.6);
            margin-top: 0.25rem;
            font-size: 0.95rem;
        }
        
        .toggle-icon {
            font-size: 1.5rem;
            transition: transform 0.3s;
        }
        
        .outfit-card.open .toggle-icon { transform: rotate(180deg); }
        
        .outfit-content {
            display: none;
            margin-top: 1.5rem;
        }
        
        .outfit-card.open .outfit-content { display: block; }
        
        .items-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .item-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 1.2rem;
            transition: all 0.2s;
        }
        
        .item-card:hover {
            background: rgba(255,255,255,0.06);
            border-color: rgba(244, 114, 182, 0.3);
        }
        
        .item-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
        
        .item-cat {
            display: inline-block;
            padding: 0.2rem 0.6rem;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }
        
        .item-name {
            font-weight: 600;
            margin-bottom: 0.3rem;
        }
        
        .item-detail {
            font-size: 0.85rem;
            color: rgba(255,255,255,0.6);
            margin-bottom: 0.5rem;
        }
        
        .item-why {
            font-size: 0.8rem;
            color: #a78bfa;
            font-style: italic;
        }
        
        .styling-tip {
            background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%);
            border: 1px solid rgba(251, 191, 36, 0.2);
            border-radius: 12px;
            padding: 1rem;
        }
        
        .styling-tip strong { color: #fbbf24; }
        
        /* Bottom sections */
        .bottom-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }
        
        .avoid-section {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
        }
        
        .avoid-section ul { list-style: none; }
        .avoid-section li { padding: 0.3rem 0; }
        .avoid-section li::before { content: "✕ "; color: #ef4444; }
        
        .celeb-section {
            background: linear-gradient(135deg, rgba(167, 139, 250, 0.1) 0%, rgba(244, 114, 182, 0.1) 100%);
            border: 1px solid rgba(167, 139, 250, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
        }
        
        .pro-tip {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
            border: 1px solid rgba(16, 185, 129, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            margin-top: 1.5rem;
        }
        
        .pro-tip strong { color: #10b981; }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            border-top: 1px solid rgba(255,255,255,0.1);
            color: rgba(255,255,255,0.4);
        }
        
        /* Loading */
        .loading {
            display: none;
            text-align: center;
            padding: 3rem;
        }
        
        .loading.active { display: block; }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 3px solid rgba(255,255,255,0.1);
            border-top-color: #a78bfa;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }
        
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>👗 AI Outfit Stylist</h1>
            <p>Your personal AI-powered fashion advisor ✨</p>
        </div>
        
        <div class="search-box">
            <label>🔍 What clothing item are you looking for?</label>
            <input type="text" class="search-input" id="searchInput" placeholder="e.g., blue jeans, white sneakers, leather jacket...">
            <br>
            <button class="search-btn" onclick="search()">✨ Get Outfit Ideas</button>
            
            <div class="quick-picks">
                <span>Try:</span>
                <button class="quick-btn" onclick="quickSearch('blue jeans')">Blue Jeans</button>
                <button class="quick-btn" onclick="quickSearch('white sneakers')">White Sneakers</button>
                <button class="quick-btn" onclick="quickSearch('leather jacket')">Leather Jacket</button>
            </div>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>✨ Our AI stylist is curating the perfect outfits for you...</p>
        </div>
        
        <div class="results" id="results"></div>
        
        <div class="footer">
            <p>Made with ❤️ by AI Outfit Stylist</p>
        </div>
    </div>
    
    <script>
        function quickSearch(term) {
            document.getElementById('searchInput').value = term;
            search();
        }
        
        function search() {
            const query = document.getElementById('searchInput').value.trim();
            if (!query) {
                alert('Please enter a clothing item!');
                return;
            }
            
            document.getElementById('loading').classList.add('active');
            document.getElementById('results').classList.remove('active');
            
            fetch('/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query })
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('loading').classList.remove('active');
                displayResults(query, data);
            })
            .catch(err => {
                document.getElementById('loading').classList.remove('active');
                alert('Error: ' + err.message);
            });
        }
        
        function displayResults(query, data) {
            const resultsDiv = document.getElementById('results');
            
            let colorsHtml = data.colors.map(c => `<span class="color-chip">${c}</span>`).join('');
            
            let outfitsHtml = data.outfits.map((outfit, i) => `
                <div class="outfit-card ${i === 0 ? 'open' : ''}" onclick="this.classList.toggle('open')">
                    <div class="outfit-header">
                        <div>
                            <div class="outfit-title">✨ ${outfit.name}</div>
                            <div class="outfit-desc">${outfit.desc}</div>
                        </div>
                        <span class="toggle-icon">▼</span>
                    </div>
                    <div class="outfit-content">
                        <div class="items-grid">
                            ${outfit.items.map(item => `
                                <div class="item-card">
                                    <div class="item-icon">${item.icon}</div>
                                    <span class="item-cat">${item.cat}</span>
                                    <div class="item-name">${item.name}</div>
                                    <div class="item-detail">${item.detail}</div>
                                    <div class="item-why">💡 ${item.why}</div>
                                </div>
                            `).join('')}
                        </div>
                        <div class="styling-tip">
                            <strong>👠 Styling Tip:</strong> ${outfit.tip}
                        </div>
                    </div>
                </div>
            `).join('');
            
            let avoidHtml = data.avoid.map(a => `<li>${a}</li>`).join('');
            
            resultsDiv.innerHTML = `
                <div class="results-header">
                    <h2>🛍️ ${query.charAt(0).toUpperCase() + query.slice(1)}</h2>
                    <p>${data.description}</p>
                </div>
                
                <div class="colors-section">
                    <div class="section-label">🎨 Complementary Colors</div>
                    ${colorsHtml}
                </div>
                
                <h3 style="margin-bottom: 1rem; font-family: 'Playfair Display', serif;">👔 Complete Outfit Ideas</h3>
                ${outfitsHtml}
                
                <div class="bottom-grid">
                    <div class="avoid-section">
                        <div class="section-label">🚫 What to Avoid</div>
                        <ul>${avoidHtml}</ul>
                    </div>
                    <div class="celeb-section">
                        <div class="section-label">🌟 Style Inspiration</div>
                        <p>${data.celeb}</p>
                    </div>
                </div>
                
                <div class="pro-tip">
                    <strong>💎 Pro Stylist Tip:</strong> ${data.protip}
                </div>
            `;
            
            resultsDiv.classList.add('active');
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
        }
        
        // Enter key support
        document.getElementById('searchInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') search();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query', '').lower().strip()
    
    # Find matching data
    result = None
    for key in DEMO_DATA:
        if key in query or query in key:
            result = DEMO_DATA[key]
            break
    
    # Fallback matches
    if not result:
        if 'jean' in query or 'denim' in query:
            result = DEMO_DATA['blue jeans']
        elif 'sneaker' in query or 'trainer' in query or 'shoe' in query:
            result = DEMO_DATA['white sneakers']
        elif 'leather' in query or 'jacket' in query:
            result = DEMO_DATA['leather jacket']
        else:
            result = DEMO_DATA['blue jeans']  # Default
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
