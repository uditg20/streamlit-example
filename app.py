#!/usr/bin/env python3
from flask import Flask, render_template_string, request, jsonify
import json

app = Flask(__name__)

# Product data with images
PRODUCTS = {
    "blue jeans": [
        {"id": 1, "name": "Classic Slim Fit Blue Jeans", "price": "$79", "img": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=500&fit=crop"},
        {"id": 2, "name": "High-Waisted Straight Leg", "price": "$89", "img": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&h=500&fit=crop"},
        {"id": 3, "name": "Relaxed Fit Boyfriend Jeans", "price": "$69", "img": "https://images.unsplash.com/photo-1475178626620-a4d074967452?w=400&h=500&fit=crop"},
        {"id": 4, "name": "Skinny Stretch Denim", "price": "$65", "img": "https://images.unsplash.com/photo-1582552938357-32b906df40cb?w=400&h=500&fit=crop"},
    ],
    "white sneakers": [
        {"id": 5, "name": "Classic White Leather Sneakers", "price": "$120", "img": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=500&fit=crop"},
        {"id": 6, "name": "Minimalist Canvas Sneakers", "price": "$75", "img": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&h=500&fit=crop"},
        {"id": 7, "name": "Platform White Sneakers", "price": "$95", "img": "https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=400&h=500&fit=crop"},
        {"id": 8, "name": "Retro White Trainers", "price": "$110", "img": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400&h=500&fit=crop"},
    ],
    "leather jacket": [
        {"id": 9, "name": "Classic Black Biker Jacket", "price": "$299", "img": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=500&fit=crop"},
        {"id": 10, "name": "Vintage Brown Leather", "price": "$350", "img": "https://images.unsplash.com/photo-1520975954732-35dd22299614?w=400&h=500&fit=crop"},
        {"id": 11, "name": "Moto Style Jacket", "price": "$275", "img": "https://images.unsplash.com/photo-1521223890158-f9f7c3d5d504?w=400&h=500&fit=crop"},
        {"id": 12, "name": "Cropped Leather Jacket", "price": "$245", "img": "https://images.unsplash.com/photo-1559551409-dadc959f76b8?w=400&h=500&fit=crop"},
    ],
    "black dress": [
        {"id": 13, "name": "Little Black Dress", "price": "$149", "img": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=500&fit=crop"},
        {"id": 14, "name": "Black Midi Dress", "price": "$129", "img": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400&h=500&fit=crop"},
        {"id": 15, "name": "Black Maxi Dress", "price": "$159", "img": "https://images.unsplash.com/photo-1539008835657-9e8e9680c956?w=400&h=500&fit=crop"},
        {"id": 16, "name": "Black Cocktail Dress", "price": "$189", "img": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=400&h=500&fit=crop"},
    ],
}

# Outfit ideas with images
OUTFIT_IDEAS = {
    "blue jeans": [
        {
            "name": "Casual Weekend",
            "img": "https://images.unsplash.com/photo-1552374196-1ab2a1c593e8?w=600&h=800&fit=crop",
            "items": [
                {"name": "White T-Shirt", "img": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=200&h=250&fit=crop"},
                {"name": "Blue Jeans", "img": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=200&h=250&fit=crop"},
                {"name": "White Sneakers", "img": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=200&h=250&fit=crop"},
                {"name": "Denim Jacket", "img": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=200&h=250&fit=crop"},
            ]
        },
        {
            "name": "Smart Casual",
            "img": "https://images.unsplash.com/photo-1507680434567-5739c80be1ac?w=600&h=800&fit=crop",
            "items": [
                {"name": "Oxford Shirt", "img": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=200&h=250&fit=crop"},
                {"name": "Dark Jeans", "img": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=200&h=250&fit=crop"},
                {"name": "Loafers", "img": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=200&h=250&fit=crop"},
                {"name": "Navy Blazer", "img": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=200&h=250&fit=crop"},
            ]
        },
        {
            "name": "Street Style",
            "img": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=600&h=800&fit=crop",
            "items": [
                {"name": "Graphic Tee", "img": "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=200&h=250&fit=crop"},
                {"name": "Ripped Jeans", "img": "https://images.unsplash.com/photo-1475178626620-a4d074967452?w=200&h=250&fit=crop"},
                {"name": "High-Top Sneakers", "img": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=200&h=250&fit=crop"},
                {"name": "Bomber Jacket", "img": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=200&h=250&fit=crop"},
            ]
        },
    ],
    "white sneakers": [
        {
            "name": "Athleisure Chic",
            "img": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600&h=800&fit=crop",
            "items": [
                {"name": "Gray Hoodie", "img": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=200&h=250&fit=crop"},
                {"name": "Black Joggers", "img": "https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=200&h=250&fit=crop"},
                {"name": "White Sneakers", "img": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=200&h=250&fit=crop"},
                {"name": "Baseball Cap", "img": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=200&h=250&fit=crop"},
            ]
        },
        {
            "name": "Summer Vibes",
            "img": "https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=600&h=800&fit=crop",
            "items": [
                {"name": "Linen Shirt", "img": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=200&h=250&fit=crop"},
                {"name": "Chino Shorts", "img": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=200&h=250&fit=crop"},
                {"name": "White Sneakers", "img": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=200&h=250&fit=crop"},
                {"name": "Sunglasses", "img": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=200&h=250&fit=crop"},
            ]
        },
        {
            "name": "Minimalist Look",
            "img": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=600&h=800&fit=crop",
            "items": [
                {"name": "Black Turtleneck", "img": "https://images.unsplash.com/photo-1608234808654-2a8875faa7fd?w=200&h=250&fit=crop"},
                {"name": "Tailored Trousers", "img": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=200&h=250&fit=crop"},
                {"name": "White Sneakers", "img": "https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=200&h=250&fit=crop"},
                {"name": "Camel Coat", "img": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=200&h=250&fit=crop"},
            ]
        },
    ],
    "leather jacket": [
        {
            "name": "Rock & Roll",
            "img": "https://images.unsplash.com/photo-1548624313-0396c75e4b1a?w=600&h=800&fit=crop",
            "items": [
                {"name": "Band T-Shirt", "img": "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=200&h=250&fit=crop"},
                {"name": "Black Skinny Jeans", "img": "https://images.unsplash.com/photo-1582552938357-32b906df40cb?w=200&h=250&fit=crop"},
                {"name": "Chelsea Boots", "img": "https://images.unsplash.com/photo-1638247025967-b4e38f787b76?w=200&h=250&fit=crop"},
                {"name": "Leather Jacket", "img": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=200&h=250&fit=crop"},
            ]
        },
        {
            "name": "Date Night",
            "img": "https://images.unsplash.com/photo-1485968579169-a6e9a7d39c80?w=600&h=800&fit=crop",
            "items": [
                {"name": "Silk Camisole", "img": "https://images.unsplash.com/photo-1564257631407-4deb1f99d992?w=200&h=250&fit=crop"},
                {"name": "Black Trousers", "img": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=200&h=250&fit=crop"},
                {"name": "Heeled Boots", "img": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=200&h=250&fit=crop"},
                {"name": "Leather Jacket", "img": "https://images.unsplash.com/photo-1521223890158-f9f7c3d5d504?w=200&h=250&fit=crop"},
            ]
        },
        {
            "name": "Casual Cool",
            "img": "https://images.unsplash.com/photo-1544441893-675973e31985?w=600&h=800&fit=crop",
            "items": [
                {"name": "White Henley", "img": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=200&h=250&fit=crop"},
                {"name": "Blue Jeans", "img": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=200&h=250&fit=crop"},
                {"name": "White Sneakers", "img": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=200&h=250&fit=crop"},
                {"name": "Brown Leather Jacket", "img": "https://images.unsplash.com/photo-1520975954732-35dd22299614?w=200&h=250&fit=crop"},
            ]
        },
    ],
    "black dress": [
        {
            "name": "Elegant Evening",
            "img": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=600&h=800&fit=crop",
            "items": [
                {"name": "Black Dress", "img": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=200&h=250&fit=crop"},
                {"name": "Strappy Heels", "img": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=200&h=250&fit=crop"},
                {"name": "Gold Clutch", "img": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=200&h=250&fit=crop"},
                {"name": "Statement Earrings", "img": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=200&h=250&fit=crop"},
            ]
        },
        {
            "name": "Casual Day",
            "img": "https://images.unsplash.com/photo-1485462537746-965f33f7f6a7?w=600&h=800&fit=crop",
            "items": [
                {"name": "Black Midi Dress", "img": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=200&h=250&fit=crop"},
                {"name": "White Sneakers", "img": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=200&h=250&fit=crop"},
                {"name": "Denim Jacket", "img": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=200&h=250&fit=crop"},
                {"name": "Crossbody Bag", "img": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=200&h=250&fit=crop"},
            ]
        },
        {
            "name": "Office Chic",
            "img": "https://images.unsplash.com/photo-1487222477894-8943e31ef7b2?w=600&h=800&fit=crop",
            "items": [
                {"name": "Black Sheath Dress", "img": "https://images.unsplash.com/photo-1539008835657-9e8e9680c956?w=200&h=250&fit=crop"},
                {"name": "Nude Pumps", "img": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=200&h=250&fit=crop"},
                {"name": "Structured Blazer", "img": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=200&h=250&fit=crop"},
                {"name": "Leather Tote", "img": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=200&h=250&fit=crop"},
            ]
        },
    ],
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
        
        .container { max-width: 1400px; margin: 0 auto; padding: 2rem; }
        
        /* Header */
        .header {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
            border-radius: 24px;
            margin-bottom: 2rem;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .header h1 {
            font-family: 'Playfair Display', serif;
            font-size: 2.5rem;
            background: linear-gradient(135deg, #fff 0%, #a78bfa 50%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .header p { color: rgba(255,255,255,0.7); margin-top: 0.5rem; }
        
        /* Search */
        .search-box {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 2rem;
        }
        
        .search-input {
            width: 400px;
            padding: 1rem 1.5rem;
            font-size: 1rem;
            border: 2px solid rgba(255,255,255,0.2);
            border-radius: 50px;
            background: rgba(255,255,255,0.05);
            color: white;
            outline: none;
        }
        
        .search-input:focus { border-color: #a78bfa; }
        .search-input::placeholder { color: rgba(255,255,255,0.4); }
        
        .search-btn {
            padding: 1rem 2rem;
            font-size: 1rem;
            font-weight: 600;
            border: none;
            border-radius: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .search-btn:hover { transform: translateY(-2px); }
        
        /* Quick picks */
        .quick-picks {
            display: flex;
            gap: 0.5rem;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 2rem;
        }
        
        .quick-btn {
            padding: 0.5rem 1rem;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 20px;
            background: rgba(255,255,255,0.05);
            color: rgba(255,255,255,0.8);
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .quick-btn:hover { background: rgba(167, 139, 250, 0.2); border-color: #a78bfa; }
        
        /* Section Title */
        .section-title {
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            margin: 2rem 0 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        /* Products Grid */
        .products-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }
        
        .product-card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            overflow: hidden;
            transition: all 0.3s;
            cursor: pointer;
        }
        
        .product-card:hover {
            transform: translateY(-5px);
            border-color: #a78bfa;
            box-shadow: 0 10px 40px rgba(167, 139, 250, 0.2);
        }
        
        .product-img {
            width: 100%;
            height: 300px;
            object-fit: cover;
        }
        
        .product-info {
            padding: 1rem;
        }
        
        .product-name {
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .product-price {
            color: #a78bfa;
            font-weight: 600;
            font-size: 1.1rem;
        }
        
        /* Outfit Ideas Grid */
        .outfits-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2rem;
        }
        
        .outfit-card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            overflow: hidden;
            transition: all 0.3s;
        }
        
        .outfit-card:hover {
            transform: translateY(-5px);
            border-color: #f472b6;
            box-shadow: 0 10px 40px rgba(244, 114, 182, 0.2);
        }
        
        .outfit-main-img {
            width: 100%;
            height: 400px;
            object-fit: cover;
        }
        
        .outfit-info {
            padding: 1.5rem;
        }
        
        .outfit-name {
            font-family: 'Playfair Display', serif;
            font-size: 1.4rem;
            color: #f472b6;
            margin-bottom: 1rem;
        }
        
        .outfit-items {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 0.5rem;
        }
        
        .outfit-item {
            text-align: center;
        }
        
        .outfit-item img {
            width: 100%;
            height: 80px;
            object-fit: cover;
            border-radius: 8px;
            border: 2px solid transparent;
            transition: all 0.2s;
        }
        
        .outfit-item img:hover {
            border-color: #a78bfa;
        }
        
        .outfit-item span {
            display: block;
            font-size: 0.7rem;
            color: rgba(255,255,255,0.6);
            margin-top: 0.3rem;
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
        
        /* Results container */
        .results { display: none; }
        .results.active { display: block; }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            border-top: 1px solid rgba(255,255,255,0.1);
            color: rgba(255,255,255,0.4);
        }
        
        /* Divider */
        .divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            margin: 2rem 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>👗 AI Outfit Stylist</h1>
            <p>Search for any clothing item and get outfit inspiration with pictures</p>
        </div>
        
        <div class="search-box">
            <input type="text" class="search-input" id="searchInput" placeholder="Search for clothing items...">
            <button class="search-btn" onclick="search()">🔍 Search</button>
        </div>
        
        <div class="quick-picks">
            <span style="color: rgba(255,255,255,0.5);">Popular:</span>
            <button class="quick-btn" onclick="quickSearch('blue jeans')">👖 Blue Jeans</button>
            <button class="quick-btn" onclick="quickSearch('white sneakers')">👟 White Sneakers</button>
            <button class="quick-btn" onclick="quickSearch('leather jacket')">🧥 Leather Jacket</button>
            <button class="quick-btn" onclick="quickSearch('black dress')">👗 Black Dress</button>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Finding products and outfit ideas...</p>
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
                alert('Please enter a search term!');
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
            
            // Products HTML
            let productsHtml = data.products.map(p => `
                <div class="product-card">
                    <img src="${p.img}" alt="${p.name}" class="product-img" loading="lazy">
                    <div class="product-info">
                        <div class="product-name">${p.name}</div>
                        <div class="product-price">${p.price}</div>
                    </div>
                </div>
            `).join('');
            
            // Outfits HTML
            let outfitsHtml = data.outfits.map(o => `
                <div class="outfit-card">
                    <img src="${o.img}" alt="${o.name}" class="outfit-main-img" loading="lazy">
                    <div class="outfit-info">
                        <div class="outfit-name">✨ ${o.name}</div>
                        <div class="outfit-items">
                            ${o.items.map(item => `
                                <div class="outfit-item">
                                    <img src="${item.img}" alt="${item.name}" loading="lazy">
                                    <span>${item.name}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `).join('');
            
            resultsDiv.innerHTML = `
                <h2 class="section-title">🛍️ Search Results for "${query}"</h2>
                <div class="products-grid">${productsHtml}</div>
                
                <div class="divider"></div>
                
                <h2 class="section-title">💡 Outfit Ideas</h2>
                <p style="color: rgba(255,255,255,0.6); margin-bottom: 1.5rem;">Complete looks featuring ${query}</p>
                <div class="outfits-grid">${outfitsHtml}</div>
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
    
    # Find matching products
    products = []
    outfits = []
    
    for key in PRODUCTS:
        if key in query or query in key:
            products = PRODUCTS[key]
            outfits = OUTFIT_IDEAS.get(key, [])
            break
    
    # Fallback matches
    if not products:
        if 'jean' in query or 'denim' in query or 'pant' in query:
            products = PRODUCTS['blue jeans']
            outfits = OUTFIT_IDEAS['blue jeans']
        elif 'sneaker' in query or 'shoe' in query or 'trainer' in query:
            products = PRODUCTS['white sneakers']
            outfits = OUTFIT_IDEAS['white sneakers']
        elif 'leather' in query or 'jacket' in query or 'coat' in query:
            products = PRODUCTS['leather jacket']
            outfits = OUTFIT_IDEAS['leather jacket']
        elif 'dress' in query or 'gown' in query:
            products = PRODUCTS['black dress']
            outfits = OUTFIT_IDEAS['black dress']
        else:
            # Default to jeans
            products = PRODUCTS['blue jeans']
            outfits = OUTFIT_IDEAS['blue jeans']
    
    return jsonify({
        "products": products,
        "outfits": outfits
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
